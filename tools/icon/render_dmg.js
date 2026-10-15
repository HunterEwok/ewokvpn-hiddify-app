const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  const p = await b.newPage({ viewport: { width: 1200, height: 656 } });
  await p.setContent(`<html><body style="margin:0">${fs.readFileSync(process.argv[2],'utf8')}</body></html>`);
  await p.waitForTimeout(200);
  await p.screenshot({ path: process.argv[3] });
  await b.close();
})();
