/**
 * URLSentinel Background Service Worker (Manifest V3)
 * Provides real-time navigation evaluation, local verdict caching, and warning interception.
 */

const API_BASE_URL = 'http://localhost:8000/api/v1';
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours

// Local known bad patterns for instant zero-latency blocking
const INSTANT_BLOCK_PATTERNS = [
  /micros0ft/i,
  /paypa1/i,
  /rnicrosoft/i,
  /g00gle/i,
  /apple-id-verify\./i,
  /secure-chase-update\./i,
];

/**
 * Update the extension icon badge to reflect security status.
 */
function updateBadge(tabId, verdict, score) {
  if (!tabId) return;

  switch (verdict) {
    case 'MALICIOUS':
      chrome.action.setBadgeText({ tabId, text: '!' });
      chrome.action.setBadgeBackgroundColor({ tabId, color: '#ef4444' });
      break;
    case 'SUSPICIOUS':
      chrome.action.setBadgeText({ tabId, text: 'WARN' });
      chrome.action.setBadgeBackgroundColor({ tabId, color: '#f59e0b' });
      break;
    case 'BENIGN':
      chrome.action.setBadgeText({ tabId, text: 'SAFE' });
      chrome.action.setBadgeBackgroundColor({ tabId, color: '#10b981' });
      break;
    default:
      chrome.action.setBadgeText({ tabId, text: '' });
      break;
  }
}

/**
 * Check if a URL is cached locally and still fresh.
 */
async function getCachedVerdict(url) {
  try {
    const data = await chrome.storage.local.get(url);
    if (data[url]) {
      const entry = data[url];
      if (Date.now() - entry.timestamp < CACHE_TTL_MS) {
        return entry.verdict;
      }
    }
  } catch (err) {
    console.error('Storage retrieval failed:', err);
  }
  return null;
}

/**
 * Store a verdict in local storage with current timestamp.
 */
async function setCachedVerdict(url, verdict) {
  try {
    await chrome.storage.local.set({
      [url]: {
        verdict,
        timestamp: Date.now(),
      },
    });
  } catch (err) {
    console.error('Storage write failed:', err);
  }
}

/**
 * Evaluate a URL against URLSentinel detection API.
 */
async function scanUrl(url) {
  // 1. Instant heuristic check
  for (const pattern of INSTANT_BLOCK_PATTERNS) {
    if (pattern.test(url)) {
      return {
        verdict: 'MALICIOUS',
        risk_score: 95,
        summary: 'Matches verified deceptive phishing domain signature.',
        reason: 'Brand Impersonation / Typosquatting',
      };
    }
  }

  // 2. Check local storage cache
  const cached = await getCachedVerdict(url);
  if (cached) {
    return cached;
  }

  // 3. Query URLSentinel local API
  try {
    const response = await fetch(`${API_BASE_URL}/scan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    if (response.ok) {
      const result = await response.json();
      await setCachedVerdict(url, result);
      return result;
    }
  } catch (err) {
    // If API unavailable, fallback gracefully to UNKNOWN
    console.warn('URLSentinel API unreachable, using local safety fallbacks:', err);
  }

  return {
    verdict: 'UNKNOWN',
    risk_score: 0,
    summary: 'Offline / standard protection active.',
  };
}

/**
 * Intercept navigation before web request leaves browser.
 */
chrome.webNavigation.onBeforeNavigate.addListener(async (details) => {
  // Only inspect top-level frame navigation
  if (details.frameId !== 0) return;

  const url = details.url;
  // Ignore browser internal schemes
  if (url.startsWith('chrome://') || url.startsWith('chrome-extension://') || url.startsWith('about:')) {
    return;
  }

  const result = await scanUrl(url);

  if (result.verdict === 'MALICIOUS') {
    // Block navigation and redirect to warning interstitial
    const warningUrl = chrome.runtime.getURL(
      `warning.html?url=${encodeURIComponent(url)}&score=${result.risk_score || 95}&reason=${encodeURIComponent(
        result.summary || 'Known malicious phishing or malware site'
      )}`
    );
    chrome.tabs.update(details.tabId, { url: warningUrl });
  } else {
    updateBadge(details.tabId, result.verdict, result.risk_score);
  }
});

/**
 * Handle messages from popup UI.
 */
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'GET_TAB_SECURITY_STATUS') {
    chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
      if (tabs.length === 0) {
        sendResponse({ status: 'NO_ACTIVE_TAB' });
        return;
      }

      const activeUrl = tabs[0].url;
      if (!activeUrl || activeUrl.startsWith('chrome://')) {
        sendResponse({ verdict: 'SYSTEM', url: activeUrl });
        return;
      }

      const result = await scanUrl(activeUrl);
      updateBadge(tabs[0].id, result.verdict, result.risk_score);
      sendResponse({ ...result, url: activeUrl });
    });
    return true; // Keep message channel open for async response
  }
});

