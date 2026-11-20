const puppeteer = require('z:/URLSentinel/node_modules/puppeteer-core');

(async () => {
    try {
        const browser = await puppeteer.launch({
            executablePath: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            headless: 'new',
            args: ['--no-sandbox', '--disable-setuid-sandbox', '--window-size=1440,1100']
        });
        const page = await browser.newPage();
        await page.setViewport({ width: 1440, height: 1100 });
        
        console.log('Navigating to homepage...');
        await page.goto('http://localhost:3000', { waitUntil: 'networkidle2' });
        
        // Find input box
        const inputSelector = 'input';
        await page.waitForSelector(inputSelector, { timeout: 5000 });
        await page.type(inputSelector, 'http://paypa1-account-update.xyz/login');
        
        // Find scan button or press Enter
        await page.keyboard.press('Enter');
        
        console.log('Waiting 5s for scan analysis and verdict render...');
        await new Promise(r => setTimeout(r, 5000));
        
        const ssPath = 'z:/URLSentinel/URLSentinel_PPD_Report/screenshots/live_scanner_verdict.png';
        await page.screenshot({ path: ssPath, fullPage: false });
        console.log('Verdict screenshot captured successfully:', ssPath);

        // Capture Swagger API docs
        console.log('Navigating to Swagger docs...');
        await page.goto('http://127.0.0.1:8000/docs', { waitUntil: 'networkidle2' });
        await new Promise(r => setTimeout(r, 2000));
        const apiSsPath = 'z:/URLSentinel/URLSentinel_PPD_Report/screenshots/live_api_swagger_docs.png';
        await page.screenshot({ path: apiSsPath, fullPage: false });
        console.log('Swagger screenshot captured successfully:', apiSsPath);

        await browser.close();
        console.log('All screenshots completed.');
    } catch (e) {
        console.error('Puppeteer capture error:', e);
    }
})();
