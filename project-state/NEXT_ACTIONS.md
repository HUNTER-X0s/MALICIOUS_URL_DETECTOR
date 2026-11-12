# Next Actions

**Context:** Production hardening, FORTRESS v2.0 UI/UX overhaul, Redis persistence, feed scheduler cron, and browser extension packaging completed and fully verified.

## Operational & Next Milestones

1. **Production Docker Deployment**:
   - Run `docker compose up --build -d` on production target host with valid domain certificates.
   - Configure Let's Encrypt / Certbot TLS reverse proxy in `nginx/nginx.conf` for production HTTPS.

2. **Chrome Web Store Submission**:
   - Upload `dist/urlsentinel-extension-v1.0.0.zip` to Google Chrome Developer Dashboard.
   - Use copy from `apps/extension/STORE_LISTING.md` for store description, categories (Security / Productivity), and privacy disclosure.

3. **Ongoing Feed Ingestion Monitoring**:
   - Monitor `_LAST_FEED_SYNC` and `/api/v1/stats` endpoint to verify live feed synchronization metrics from URLhaus and OpenPhish.
