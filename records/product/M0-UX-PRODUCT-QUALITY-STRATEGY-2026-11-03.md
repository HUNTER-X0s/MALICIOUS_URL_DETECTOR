# URLSentinel — UX and Product Quality Strategy (M0)

**Date:** 2026-11-03  
**Reference:** `docs/07-ux/TRUST_CENTRED_UX_PRINCIPLES.md`, `docs/07-ux/DESIGN_RESEARCH_AND_SYSTEM.md`, `docs/08-quality/ACCESSIBILITY_POLICY.md`

---

## 1. Core UX philosophy

URLSentinel's user experience must earn trust through **evidence, clarity, and honesty** — not visual reassurance or false security theater.

### Non-negotiable UX invariants
- Never use a green badge, checkmark, or "Safe" label without appropriate limitations displayed
- UNKNOWN is a first-class visible state — not hidden, not styled as benign
- Every verdict must show: what was checked, what was not checked, when it was checked, how confident the assessment is
- Warnings must be clear and calm — not manipulative, panic-inducing, or designed to maximize "engagement"
- HTTPS presence does not make a URL safe — the UI must never imply this
- Plain-language explanations for non-technical users; technical details optional behind disclosure

---

## 2. Primary user journeys

### Journey 1: URL scan (anonymous, web app)
1. User arrives at home page (clear purpose, URL input prominent)
2. User pastes or types URL + clicks Scan
3. Loading state: "Checking..." with progress indication (not fake animations)
4. Result page: verdict with evidence summary
5. If UNKNOWN: explain what is missing; recommend caution; option to re-check later
6. If MALICIOUS: clear warning; explain reason; recommend action; back button prominent
7. If SUSPICIOUS: explain signals; balanced guidance; not panic-inducing
8. If BENIGN: show what was checked; state limitations; no "100% Safe" messaging
9. Option to report false positive

### Journey 2: Extension real-time protection
1. User navigates to URL
2. Extension checks local cache (< 5ms) → fast path (< 500ms) → deep path (async)
3. Normal site: no friction (essentially zero UX impact)
4. Suspicious site: security badge changes; popup notification available
5. Malicious/DANGEROUS site: full-page warning interstitial before navigation
6. Warning shows: threat type (plain language), evidence, Go Back (primary), Proceed (secondary, requires deliberate action), View Full Report, Report False Positive
7. User reports false positive → confirmation + review promise

### Journey 3: Understanding a warning (non-expert user)
1. Extension blocks navigation to suspected phishing page
2. User sees: "This website may be trying to steal your password"
3. Explanation: "It closely resembles [brand name]'s website but was registered recently. A security database reported it as suspicious."
4. Actions: Go Back (styled as safe/primary), Learn More About This Warning, Report a Mistake
5. Proceed option visible but de-emphasized; requires deliberate click and confirmation step
6. No countdown timers, no fear imagery, no manipulative copy

---

## 3. Design system requirements

### Visual direction criteria (must be validated by research in M1)
Any design direction must be evaluated against:
- **Trust:** Does it feel credible and professional for a security product?
- **Clarity:** Can a non-expert understand the verdict in < 3 seconds?
- **Accessibility:** Does it work with high contrast, screen readers, keyboard navigation?
- **Distinctiveness:** Is it recognizable and coherent, not generic?
- **Performance:** Does it render fast on mid-range mobile devices?

### Semantic token requirements (minimum)
- Verdict state colors: MALICIOUS (red with sufficient contrast), SUSPICIOUS (amber), UNKNOWN (grey/neutral), BENIGN (muted green — NOT bright check mark green)
- All verdict states must work with text labels, not color alone
- Status indicators must pass WCAG 1.4.1 (not color as sole distinguisher)

### Typography
- Primary font: legible, accessible, no display-only font for body copy
- Size scale: minimum 16px body; 14px secondary; 12px minimum for any UI element
- Line height: ≥ 1.5 for body copy
- Warning text: high contrast on both light and dark backgrounds

---

## 4. Responsive design requirements

| Viewport | Target experience |
|---|---|
| 320px (very small mobile) | Core function works; no horizontal scroll; verdict legible |
| 375px (standard mobile) | Comfortable reading; scan form usable with thumbs |
| 768px (tablet) | Two-column layout possible for evidence display |
| 1280px (laptop) | Full feature set; side-by-side evidence and verdict |
| 1920px (desktop/wide) | Balanced layout; no excessive whitespace or awkward stretching |

---

## 5. Accessibility requirements

**Target:** WCAG 2.2 Level AA  
**Hard requirements:**
- All text: minimum 4.5:1 contrast ratio (3:1 for large text)
- Keyboard navigable: all interactive elements reachable by Tab
- Focus visible: clear focus indicator on all focusable elements
- Screen reader compatible: semantic HTML, ARIA roles, alt text for icons
- Color + text: never use color as the only indicator (verdict states must have text label)
- Motion: respect `prefers-reduced-motion`; no autoplaying animations that cannot be paused

**Testing required:**
- Automated: axe-core in CI (will flag ~30–40% of real issues)
- Manual: screen reader spot-check with NVDA (Windows) and VoiceOver (macOS)
- Keyboard: complete tab order test on all major flows
- Contrast: manual check with colour contrast analyser

---

## 6. SEO and discoverability

**Web app:**
- Technical SEO: meta title, description, canonical, Open Graph, Twitter card
- Sitemap and robots.txt configured
- Scan result pages: `noindex` by default (user privacy + no scraped content indexing)
- Core Web Vitals: LCP ≤ 2.5s, INP < 200ms, CLS < 0.1 measured at P75
- Useful, original educational content (security guides) can be indexed and add SEO value
- Schema.org markup for organization and article content where appropriate
- No guaranteed rankings; no SEO manipulation

**Browser extension:**
- Chrome Web Store: honest listing, accurate screenshots, real description
- No keyword stuffing, fake reviews, or misleading permission requests
- Store listing reviewed and approved by owner before submission

---

## 7. Trust communication principles

| Situation | Communication principle |
|---|---|
| Malicious URL | Clear, calm warning; explain threat type; recommend action; no panic copy |
| Suspicious URL | Balanced concern; explain signals; user decides with information |
| Unknown / insufficient evidence | Honest uncertainty; explain what's missing; recommend caution |
| Benign assessment | Show evidence checked; state limitations; no "100% Safe" |
| Provider unavailable | Show UNKNOWN or PARTIAL; explain why; no misleading confidence |
| False positive | Fast, non-judgmental report flow; acknowledge and confirm |
| Security education | Plain language; useful, actionable; no fear-mongering |

---

## 8. Quality acceptance criteria (UX)

- Comprehension test: a sample of 5 non-expert users can correctly identify the verdict and recommended action within 30 seconds of seeing the result page
- Accessibility: axe-core finds zero critical/serious issues; keyboard navigation complete; screen reader verification for warning flow
- Performance: Lighthouse CI ≥ 80 (measured); Core Web Vitals in "good" threshold on representative hardware
- Responsive: zero horizontal overflow at 320px; all content reachable at all tested viewports
- Warning UX: "Go Back" button is the primary action (more prominent than "Proceed"); "Proceed" requires deliberate action

