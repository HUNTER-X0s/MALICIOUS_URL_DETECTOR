# Browser and device compatibility matrix

Antigravity must decide supported versions using current official vendor support data and customer research. At minimum evaluate Chrome, Microsoft Edge and Firefox independently. Safari is a separate future decision, not implied by Chromium compatibility.

For each browser/version record: install/update/uninstall, manifest/API differences, permissions, background/service-worker lifecycle, content-script behavior, tab/navigation events, SPA behavior, storage, messaging, incognito/private browsing consent, offline state, popup/warning UI, keyboard/screen reader, performance overhead, CSP and store-policy review.

For website test matrix include small phones (including 320 CSS px width), mainstream phones, tablet portrait/landscape, laptop, desktop, 1440p+, ultrawide, touch, mouse, keyboard, zoom/text scaling, high DPI, reduced motion and dark/light modes if supported. Use responsive content-driven layouts; do not assume a fixed set of device widths is exhaustive.

Track supported, tested, partially tested and unsupported states separately. A green CI result on Chromium is not evidence of Firefox compatibility.
