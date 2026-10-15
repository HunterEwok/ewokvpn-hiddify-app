// Renders a list of SVG files to PNG: node render_many.js jobs.json  ([{svg, out, size}])
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const b = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
  for (const j of jobs) {
    const p = await b.newPage({ viewport: { width: j.size, height: j.size } });
    const svg = fs.readFileSync(j.svg, 'utf8').replace(/width="\d+" height="\d+"/, `width="${j.size}" height="${j.size}"`);
    await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
    await p.waitForTimeout(150);
    await p.screenshot({ path: j.out, omitBackground: true });
    await p.close();
  }
  await b.close();
})();
