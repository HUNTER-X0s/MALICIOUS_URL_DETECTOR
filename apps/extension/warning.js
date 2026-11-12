/**
 * URLSentinel Warning Interstitial Controller
 */

document.addEventListener('DOMContentLoaded', () => {
  const params = new URLSearchParams(window.location.search);
  const targetUrl = params.get('url') || 'Unknown destination';
  const score = params.get('score') || '95';
  const reason = params.get('reason') || 'Known malicious phishing or malware site';

  document.getElementById('blockedUrl').textContent = targetUrl;
  document.getElementById('threatReason').textContent = reason;
  document.getElementById('riskBadge').textContent = `Risk ${score}/100`;

  // Return to Safety
  document.getElementById('returnSafeBtn').addEventListener('click', () => {
    if (window.history.length > 1) {
      window.history.back();
    } else {
      window.close();
    }
  });

  // Toggle Override Panel
  const toggleOverrideBtn = document.getElementById('toggleOverrideBtn');
  const overridePanel = document.getElementById('overridePanel');

  toggleOverrideBtn.addEventListener('click', () => {
    overridePanel.classList.toggle('hidden');
  });

  // Confirm Proceed Anyway (Deliberate bypass)
  document.getElementById('confirmProceedBtn').addEventListener('click', () => {
    if (confirm('Are you absolutely certain? This website is verified as high-risk.')) {
      window.location.href = targetUrl;
    }
  });

  // Report False Positive
  document.getElementById('reportFpBtn').addEventListener('click', () => {
    const reportUrl = `http://localhost:3000/report?url=${encodeURIComponent(targetUrl)}`;
    window.open(reportUrl, '_blank');
  });
});

