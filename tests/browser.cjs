// Integration coverage for real WebGL, input ownership, activities and saves.
const assert = require('node:assert/strict');
const { chromium } = require('playwright');
const { spawn, execFile } = require('node:child_process');
const { promisify } = require('node:util');
const fs = require('node:fs/promises');
const path = require('node:path');
const root = path.resolve(__dirname, '..');
const url = process.env.TEST_URL || 'http://127.0.0.1:8765';
const assets = new Map();
const failures = [];
const run = promisify(execFile);
let server, browser;

async function prepare(page) {
  page.on('pageerror', error => failures.push(error.message));
  // Optional bridge for managed environments whose Chromium lacks proxy CA trust.
  // curl retains the environment's proxy and certificate verification.
  if (process.env.TEST_CURL_PROXY === '1') await page.route('https://**/*', async route => {
    const address = route.request().url();
    try {
      if (!assets.has(address)) assets.set(address, run('curl', ['-fsSL', '--max-time', '30', address], {encoding:'buffer', maxBuffer:8*1024*1024}).then(result => result.stdout));
      const body = await assets.get(address);
      const contentType = address.includes('fonts.googleapis') ? 'text/css' : address.includes('gstatic') ? 'font/woff2' : 'application/javascript';
      await route.fulfill({body, contentType});
    } catch (error) { failures.push(`Asset ${address}: ${error.message}`); await route.abort(); }
  });
  await page.goto(url, {waitUntil:'networkidle'});
  await page.waitForFunction(() => typeof state !== 'undefined' && state.activeZone === 'throw');
}
async function check(page, fn, expected, message) { assert.deepEqual(await page.evaluate(fn), expected, message); }
async function screenshot(page, name) { await page.screenshot({path:path.join(root, 'test-results', name + '.png')}); }
async function inView(page, selector) {
  const result = await page.locator(selector).evaluate(el => {
    const r = el.getBoundingClientRect();
    const visible = getComputedStyle(el).visibility !== 'hidden' && r.width > 0 && r.height > 0;
    const hit = document.elementFromPoint(r.x + r.width/2, r.y + r.height/2);
    return {visible, inside:r.left >= 0 && r.right <= innerWidth + 1 && r.top >= 0 && r.bottom <= innerHeight + 1, clickable:el.contains(hit)};
  });
  assert.deepEqual(result, {visible:true,inside:true,clickable:true}, selector);
}
async function desktopFlow() {
  const page = await browser.newPage({viewport:{width:1440,height:900}});
  await prepare(page);
  await inView(page, '#throwActionBtn');
  await screenshot(page, 'desktop-throw');
  await page.locator('#stationNav button').nth(1).click();
  await check(page, () => [state.isPullingUp, state.activeZone], [true, 'pullup']);
  await page.keyboard.press('Space');
  assert.ok(await page.evaluate(() => state.pullUpXp > 0));
  await page.evaluate(() => { lastPullUpRep = -Infinity; state.pullUpXp = 4; pullUpRepTime = 0; doCalculusPullUpRep(); });
  await check(page, () => [state.pullUpLevel, state.pullUpXp], [2,1], 'Perfect rep carries XP through level-up');
  await page.keyboard.down('Space');
  const xp = await page.evaluate(() => state.pullUpXp);
  await page.keyboard.down('Space');
  assert.equal(await page.evaluate(() => state.pullUpXp), xp, 'Key repeat must not award XP');
  await page.keyboard.up('Space');
  await page.locator('#stationNav button').nth(2).click();
  await check(page, () => [state.isPullingUp, state.activeZone, currentModal], [false,'shop','shopModal']);
  const start = await page.evaluate(() => ({...state.playerPos}));
  await page.keyboard.press('w');
  await check(page, () => ({...state.playerPos}), start, 'Modal must block movement');
  await page.keyboard.press('Shift+Tab');
  await check(page, () => document.querySelector('#shopModal').contains(document.activeElement), true);
  await page.keyboard.press('Escape');
  await check(page, () => currentModal, null);
  await page.locator('#stationNav button').nth(2).click();
  await check(page, () => currentModal, 'shopModal', 'Same-station shortcut reopens shop');
  await page.keyboard.press('Escape');
  await page.locator('#stationNav button').nth(0).click();
  await page.locator('#throwActionBtn').click();
  await page.evaluate(() => walkToStation('pullup'));
  await check(page, () => state.activeZone, 'throw', 'Cannot teleport during wind-up');
  await page.waitForFunction(() => state.activeThrow?.phase === 'reveal', {timeout:30000});
  await check(page, () => [getComputedStyle(document.getElementById('labelsContainer')).visibility, trajectoryLineMesh.visible, rampArrow.visible], ['hidden',false,false], 'Catch showcase hides world HUD clutter');
  await screenshot(page, 'desktop-catch');
  await page.locator('#catchTapPrompt').click();
  await check(page, () => [state.activeThrow, state.inventory.length], [null,1], 'Collect button awards exactly one pet');
  await page.evaluate(() => { skipThrowAnimation(); });
  await check(page, () => state.inventory.length, 1);
  if (await page.evaluate(() => !!currentModal)) await page.keyboard.press('Escape');
  await page.locator('#demoModeBtn').click();
  await check(page, () => new Set(state.inventory.map(p => p.animalId)).size, 18, 'Demo previews all species');
  const saved = await page.evaluate(() => localStorage.getItem(SAVE_KEY));
  await page.evaluate(() => { state.cash += 123; saveGame(); });
  await check(page, () => localStorage.getItem(SAVE_KEY), saved, 'Demo must not overwrite save');
  for (const modal of ['shopModal','sellModal','animalsModal','indexModal','leaderboardModal','calcLabModal','settingsModal']) {
    await page.evaluate(id => openModal(id), modal);
    await inView(page, `#${modal} button[aria-label="Close panel"]`);
    await screenshot(page, 'desktop-' + modal);
    await page.keyboard.press('Escape');
  }
  await page.evaluate(() => { openModal('shopModal'); selectFood('apple'); });
  await check(page, () => state.equippedFoodId, 'apple');
  await page.keyboard.press('Escape');
  await page.evaluate(() => { openModal('animalsModal'); toggleEquipAnimal(state.inventory[0].uid); });
  await check(page, () => state.inventory.filter(p => p.equipped).length, 19);
  await page.keyboard.press('Escape');
  await page.evaluate(() => { openModal('sellModal'); sellAllUnequipped(); });
  await check(page, () => state.inventory.length, 19);
  await page.keyboard.press('Escape');
  await page.locator('#demoModeBtn').click();
  await check(page, () => [state.inventory.length, state.equippedFoodId], [1,'carrot'], 'Exit demo restores inventory and bait');
  await page.evaluate(() => { state.settings.musicVol = 0; state.settings.sfxVol = 0; setGraphicsQuality('low'); });
  await page.reload({waitUntil:'networkidle'});
  await page.waitForFunction(() => state.activeZone === 'throw');
  await check(page, () => [state.inventory.length, state.settings.graphics, renderer.shadowMap.enabled, state.settings.musicVol], [1,'low',false,0]);
  await page.locator('#stationNav button').nth(1).click();
  await check(page, () => [audio.musicGain.gain.value, audio.sfxGain.gain.value], [0,0], 'Saved mute stays muted on first gesture');
  await page.keyboard.press('Escape');
  await check(page, () => state.isPullingUp, false);
  await page.evaluate(() => { keys.w = true; window.dispatchEvent(new Event('blur')); });
  await check(page, () => Object.keys(keys).length, 0);

  await page.locator('#stationNav button').nth(0).click();
  await check(page, () => state.activeZone, 'throw');

  // Right-click handling: prevent context menu, allow right-click camera orbit, and prevent stuck walking
  const canvas = page.locator('#webglContainer');
  const contextMenuPrevented = await canvas.evaluate(el => {
    const ev = new MouseEvent('contextmenu', { bubbles: true, cancelable: true, button: 2 });
    return !el.dispatchEvent(ev);
  });
  assert.equal(contextMenuPrevented, true, 'Right click context menu must be prevented');

  const initialYaw = await page.evaluate(() => camYaw);
  const box = await canvas.boundingBox();
  await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2);
  await page.mouse.down({ button: 'right' });
  await page.mouse.move(box.x + box.width / 2 + 50, box.y + box.height / 2, { steps: 5 });
  await page.mouse.up({ button: 'right' });
  const newYaw = await page.evaluate(() => camYaw);
  assert.notEqual(newYaw, initialYaw, 'Right-drag must orbit the camera');

  await canvas.click({ position: { x: 50, y: 50 } });
  await page.keyboard.down('w');
  assert.equal(await page.evaluate(() => !!keys['w']), true, 'Key W is active');
  await page.mouse.click(box.x + box.width / 2, box.y + box.height / 2, { button: 'right' });
  await page.keyboard.up('w');
  assert.equal(await page.evaluate(() => !!keys['w']), false, 'Key W released after right-click without sticking');

  await page.close();
  console.log('PASS desktop activities, modal focus, catch, demo isolation, settings and keyboard');
}
async function mobileFlow(width, height) {
  const page = await browser.newPage({viewport:{width,height},isMobile:true,hasTouch:true,deviceScaleFactor:2});
  await prepare(page);
  await inView(page, '#throwActionBtn');
  await inView(page, '#calcMinimizedBar button');
  await inView(page, '#joystickZone');
  for (let i=0;i<5;i++) await inView(page, `#stationNav button:nth-child(${i+1})`);
  await check(page, () => [renderer.getPixelRatio(), renderer.shadowMap.enabled], [1,false]);
  await screenshot(page, `mobile-${width}x${height}-throw`);
  // Two real concurrent touch pointers, one for walking and one for camera orbit.
  const joy = await page.locator('#joystickZone').boundingBox();
  const session = await page.context().newCDPSession(page);
  const j = {x:joy.x+joy.width/2, y:joy.y+joy.height/2, id:1};
  const c = {x:width/2, y:height/2, id:2};
  await session.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[j]});
  await session.send('Input.dispatchTouchEvent', {type:'touchStart', touchPoints:[j,c]});
  await session.send('Input.dispatchTouchEvent', {type:'touchMove', touchPoints:[{...j,x:j.x+25},{...c,x:c.x+35}]});
  await check(page, () => joystickActive && joystickDir.x > .5 && camYaw < 0, true, 'Independent simultaneous movement and camera');
  await session.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[{...j,x:j.x+25}]});
  await check(page, () => joystickActive, false, 'Joystick releases independently');
  await session.send('Input.dispatchTouchEvent', {type:'touchEnd',touchPoints:[]});
  await check(page, () => cameraPointer, null);
  await page.locator('#stationNav button').nth(0).tap();
  await page.locator('#calcMinimizedBar button').tap();
  await check(page, () => oscCanvas.width > 0 && oscCanvas.height > 0, true);
  await inView(page, '#pauseWaveBtn');
  await screenshot(page, `mobile-${width}x${height}-calculus`);
  await page.locator('#calcExpandedPanel button[title="Minimize Oscilloscope"]').tap();
  await page.locator('#stationNav button').nth(1).tap();
  await inView(page, '#pullUpActionBtn');
  await check(page, () => getComputedStyle(document.getElementById('calcMinimizedBar')).visibility, 'hidden');
  await screenshot(page, `mobile-${width}x${height}-training`);
  await page.locator('#pullUpActionBtn').tap();
  assert.ok(await page.evaluate(() => state.pullUpXp > 0));
  await page.locator('#stationNav button').nth(2).tap();
  await check(page, () => [currentModal, state.isPullingUp], ['shopModal',false]);
  await screenshot(page, `mobile-${width}x${height}-shop`);
  await page.locator('#shopModal button[aria-label="Close panel"]').tap();
  for (const id of ['settingsModal','animalsModal','sellModal','indexModal','calcLabModal','leaderboardModal']) {
    await page.evaluate(id => openModal(id), id);
    await inView(page, `#${id} button[aria-label="Close panel"]`);
    await screenshot(page, `mobile-${width}x${height}-${id}`);
    await page.locator(`#${id} button[aria-label="Close panel"]`).tap();
  }
  await page.locator('#stationNav button').nth(0).tap();
  await page.locator('#throwActionBtn').tap();
  await page.waitForFunction(() => state.activeThrow?.phase === 'reveal');
  await inView(page, '#catchTapPrompt');
  await screenshot(page, `mobile-${width}x${height}-catch`);
  await page.locator('#catchTapPrompt').tap();
  await check(page, () => state.inventory.length, 1);
  await page.close();
  console.log(`PASS ${width}x${height} touch, layout, activities and catch`);
}
(async () => {
  await fs.mkdir(path.join(root,'test-results'), {recursive:true});
  if (!process.env.TEST_URL) {
    const http = require('node:http');
    const mimeTypes = {
      '.html': 'text/html; charset=utf-8',
      '.js': 'application/javascript; charset=utf-8',
      '.cjs': 'application/javascript; charset=utf-8',
      '.css': 'text/css; charset=utf-8',
      '.png': 'image/png',
      '.jpg': 'image/jpeg',
      '.json': 'application/json',
      '.woff2': 'font/woff2'
    };
    server = http.createServer(async (req, res) => {
      try {
        const reqPath = decodeURI(req.url.split('?')[0]);
        const rel = reqPath === '/' ? 'index.html' : reqPath.replace(/^\/+/, '');
        const filePath = path.join(root, rel);
        if (!filePath.startsWith(root)) { res.writeHead(403); return res.end(); }
        const data = await fs.readFile(filePath);
        const ext = path.extname(filePath).toLowerCase();
        res.writeHead(200, { 'Content-Type': mimeTypes[ext] || 'application/octet-stream' });
        res.end(data);
      } catch (e) {
        res.writeHead(404);
        res.end();
      }
    });
    await new Promise((resolve, reject) => {
      server.listen(8765, '127.0.0.1', () => resolve());
      server.on('error', reject);
    });
  }
  browser=await chromium.launch({executablePath:process.env.CHROMIUM_PATH || undefined,headless:true,args:['--no-sandbox','--enable-unsafe-swiftshader']});
  if (process.env.TEST_SCOPE !== 'mobile') await desktopFlow();
  for(const [w,h] of [[390,844],[360,640],[844,390],[768,1024]]) await mobileFlow(w,h);
  assert.deepEqual(failures, [], 'No browser runtime or dependency errors');
  console.log('All browser checks passed. Screenshots in test-results/.');
})().catch(error => { console.error(error); process.exitCode=1; }).finally(async()=>{ await browser?.close(); if (server?.close) await new Promise(r => server.close(r)); else server?.kill?.(); });
