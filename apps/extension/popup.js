/**
 * URLSentinel Extension Popup Controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  const verdictText = document.getElementById('verdictText');
  const targetDomain = document.getElementById('targetDomain');
  const riskScore = document.getElementById('riskScore');
  const gaugeFill = document.getElementById('gaugeFill');
  const shieldIndicator = document.getElementById('shieldIndicator');
  const deepScanBtn = document.getElementById('deepScanBtn');

  const sslStatus = document.getElementById('sslStatus');
  const sslDesc = document.getElementById('sslDesc');
  const brandStatus = document.getElementById('brandStatus');
  const brandDesc = document.getElementById('brandDesc');
  const feedStatus = document.getElementById('feedStatus');
  const feedDesc = document.getElementById('feedDesc');

  let currentUrl = '';

  // Fetch security evaluation from background service worker
  try {
    chrome.runtime.sendMessage({ action: 'GET_TAB_SECURITY_STATUS' }, (response) => {
      if (!response || response.status === 'NO_ACTIVE_TAB') {
        verdictText.textContent = 'No Active Website';
        targetDomain.textContent = 'Open any web page to monitor';
        return;
      }

      currentUrl = response.url || '';
      try {
        const parsed = new URL(currentUrl);
        targetDomain.textContent = parsed.hostname;

        // SSL Indicator
        if (parsed.protocol === 'https:') {
          sslStatus.textContent = 'SECURE';
          sslStatus.className = 'signal-status status-ok';
          sslDesc.textContent = 'TLS encrypted connection';
        } else {
          sslStatus.textContent = 'UNENCRYPTED';
          sslStatus.className = 'signal-status status-warn';
          sslDesc.textContent = 'Plaintext HTTP connection';
        }
      } catch {
        targetDomain.textContent = currentUrl;
      }

      const verdict = response.verdict || 'UNKNOWN';
      const score = typeof response.risk_score === 'number' ? response.risk_score : 0;
      riskScore.textContent = `${score}/100`;
      gaugeFill.style.width = `${score}%`;

      // Render verdict states
      if (verdict === 'MALICIOUS') {
        verdictText.textContent = 'Malicious Threat Detected';
        verdictText.style.color = '#ef4444';
        shieldIndicator.style.background = 'rgba(239, 68, 68, 0.15)';
        shieldIndicator.style.borderColor = 'rgba(239, 68, 68, 0.4)';
        shieldIndicator.style.color = '#ef4444';
        gaugeFill.style.backgroundColor = '#ef4444';

        brandStatus.textContent = 'FAILED';
        brandStatus.className = 'signal-status status-danger';
        brandDesc.textContent = response.summary || 'Known malicious phishing marker';

        feedStatus.textContent = 'THREAT';
        feedStatus.className = 'signal-status status-danger';
        feedDesc.textContent = 'Identified in active attack campaign';

      } else if (verdict === 'SUSPICIOUS') {
        verdictText.textContent = 'Suspicious Indicators Found';
        verdictText.style.color = '#f59e0b';
        shieldIndicator.style.background = 'rgba(245, 158, 11, 0.15)';
        shieldIndicator.style.borderColor = 'rgba(245, 158, 11, 0.4)';
        shieldIndicator.style.color = '#f59e0b';
        gaugeFill.style.backgroundColor = '#f59e0b';

        brandStatus.textContent = 'ANOMALY';
        brandStatus.className = 'signal-status status-warn';
        brandDesc.textContent = 'Structural anomalies or lookalike pattern';

      } else if (verdict === 'BENIGN') {
        verdictText.textContent = 'No Known Threats Found';
        verdictText.style.color = '#10b981';
        shieldIndicator.style.background = 'rgba(16, 185, 129, 0.15)';
        shieldIndicator.style.borderColor = 'rgba(16, 185, 129, 0.4)';
        shieldIndicator.style.color = '#10b981';
        gaugeFill.style.backgroundColor = '#10b981';

      } else {
        verdictText.textContent = 'Standard Protection Active';
        verdictText.style.color = '#94a3b8';
        shieldIndicator.style.background = 'rgba(148, 163, 184, 0.15)';
        shieldIndicator.style.borderColor = 'rgba(148, 163, 184, 0.3)';
        shieldIndicator.style.color = '#94a3b8';
        gaugeFill.style.backgroundColor = '#94a3b8';
      }
    });
  } catch (err) {
    verdictText.textContent = 'Protection Active';
    targetDomain.textContent = 'Local monitor operational';
  }

  // Deep diagnostic trigger button
  deepScanBtn.addEventListener('click', () => {
    if (currentUrl) {
      const webScanUrl = `http://localhost:3000/?url=${encodeURIComponent(currentUrl)}`;
      chrome.tabs.create({ url: webScanUrl });
    }
  });
});

