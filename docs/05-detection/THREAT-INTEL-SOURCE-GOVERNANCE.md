# Threat-intelligence source governance

Before integrating a source, assess: permitted commercial use; redistribution/storage rules; attribution; API quotas; rate limits; freshness/latency; geographic/language coverage; URL/domain/IP scope; confidence/labels; false positives; outage SLA; privacy; cost; vendor lock-in; caching rights; deletion/retention; data processing terms; and incident contacts.

Maintain a provider registry with legal approval, contracts, key ownership, purpose, data fields, retention, quota, health, fallback and shutdown plan. Provider absence is not a clean bill of health. Do not use non-commercial API tiers for commercial production. Distinguish malware-distribution feeds from phishing feeds and general URL reputation. Never scrape paid/private APIs or bypass limits.
