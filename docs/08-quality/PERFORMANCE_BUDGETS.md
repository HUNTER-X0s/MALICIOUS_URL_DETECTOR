# Performance budget policy

Do not promise “lag-free”. Establish measurable user-journey budgets and optimize against real devices/networks. Suggested web Core Web Vitals field goals: LCP <=2.5 seconds, INP <200ms, CLS <0.1 at the 75th percentile, subject to current official guidance. Measure RUM and lab data separately.

Define route budgets for JS/CSS/images/fonts, API p50/p95/p99, scan queue time, verdict time, extension CPU/memory/network overhead, cold/warm cache and failure rates. Include low-end mobile, weak network, keyboard/screen-reader and high latency. Set thresholds after baseline; fail CI on statistically meaningful regressions. Do not cache verdicts beyond freshness/expiry policy.
