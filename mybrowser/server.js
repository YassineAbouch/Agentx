import express from "express";
import { chromium } from "playwright";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json());

// Servir les fichiers statiques
app.use(express.static(path.join(__dirname, 'public')));
app.use('/screenshots', express.static(path.join(__dirname, 'screenshots')));
app.use('/pdfs', express.static(path.join(__dirname, 'pdfs')));

let browser, page;

// Configuration
const CONFIG = {
  headless: true, // Mode headless - pas de fenêtre Chromium visible
  timeout: 30000, // Réduit de 45s à 30s
  allowedDomains: [], // Empty = all domains allowed. Add domains to whitelist
  maxScreenshots: 50,
  userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
};

// Ensure browser and page are initialized
async function ensure() {
  if (!browser) {
    browser = await chromium.launch({ 
      headless: CONFIG.headless,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--disable-dev-shm-usage',
        '--no-sandbox'
      ]
    });
  }
  if (!page) {
    const context = await browser.newContext({
      userAgent: CONFIG.userAgent,
      viewport: { width: 1920, height: 1080 },
      locale: 'fr-FR',
      timezoneId: 'Europe/Paris'
    });
    page = await context.newPage();
    
    // Bloquer les ressources inutiles pour accélérer
    await page.route('**/*', (route) => {
      const resourceType = route.request().resourceType();
      // Bloquer les vidéos et fonts lourdes, garder les images pour l'extraction
      if (['media', 'font'].includes(resourceType)) {
        route.abort();
      } else {
        route.continue();
      }
    });
  }
}

// Domain whitelist check
function isAllowedDomain(url) {
  if (CONFIG.allowedDomains.length === 0) return true;
  try {
    const hostname = new URL(url).hostname;
    return CONFIG.allowedDomains.some(d => hostname.includes(d));
  } catch {
    return false;
  }
}

// ============================================================================
// NAVIGATION
// ============================================================================

app.post("/open", async (req, res) => {
  try {
    await ensure();
    const { url, waitUntil = "domcontentloaded" } = req.body;
    
    if (!url) {
      return res.status(400).json({ ok: false, error: "URL required" });
    }
    
    if (!isAllowedDomain(url)) {
      return res.status(403).json({ ok: false, error: "Domain not allowed" });
    }
    
    await page.goto(url, { waitUntil, timeout: CONFIG.timeout });
    
    res.json({ 
      ok: true, 
      title: await page.title(), 
      url: page.url() 
    });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/nav/back", async (req, res) => {
  try {
    await ensure();
    await page.goBack({ waitUntil: "domcontentloaded", timeout: 20000 });
    res.json({ ok: true, url: page.url() });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/nav/forward", async (req, res) => {
  try {
    await ensure();
    await page.goForward({ waitUntil: "domcontentloaded", timeout: 20000 });
    res.json({ ok: true, url: page.url() });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/reload", async (req, res) => {
  try {
    await ensure();
    await page.reload({ waitUntil: "domcontentloaded", timeout: 20000 });
    res.json({ ok: true, url: page.url() });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// INTERACTIONS
// ============================================================================

app.post("/click", async (req, res) => {
  try {
    await ensure();
    const { selector, timeout = 20000 } = req.body;
    
    if (!selector) {
      return res.status(400).json({ ok: false, error: "Selector required" });
    }
    
    await page.click(selector, { timeout });
    res.json({ ok: true, url: page.url() });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/type", async (req, res) => {
  try {
    await ensure();
    const { selector, text, clear = true, delay = 50 } = req.body;
    
    if (!selector || text === undefined) {
      return res.status(400).json({ ok: false, error: "Selector and text required" });
    }
    
    if (clear) {
      await page.fill(selector, "");
    }
    await page.type(selector, text, { delay });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/scroll", async (req, res) => {
  try {
    await ensure();
    const { y = 800, x = 0 } = req.body;
    await page.mouse.wheel(x, y);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/wait", async (req, res) => {
  try {
    await ensure();
    const { selector, timeout = 30000 } = req.body;
    
    if (!selector) {
      return res.status(400).json({ ok: false, error: "Selector required" });
    }
    
    await page.waitForSelector(selector, { timeout });
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/hover", async (req, res) => {
  try {
    await ensure();
    const { selector } = req.body;
    
    if (!selector) {
      return res.status(400).json({ ok: false, error: "Selector required" });
    }
    
    await page.hover(selector);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// CONTENT EXTRACTION
// ============================================================================

app.get("/content/text", async (req, res) => {
  try {
    await ensure();
    const text = await page.innerText("body");
    res.json({ ok: true, text, length: text.length });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.get("/content/html", async (req, res) => {
  try {
    await ensure();
    const html = await page.content();
    res.json({ ok: true, html, length: html.length });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/extract", async (req, res) => {
  try {
    await ensure();
    const { selector, mode = "text" } = req.body;
    
    if (!selector) {
      return res.status(400).json({ ok: false, error: "Selector required" });
    }
    
    let result;
    if (mode === "text") {
      result = await page.innerText(selector);
    } else if (mode === "html") {
      const element = await page.$(selector);
      result = element ? await element.innerHTML() : null;
    } else if (mode === "attribute") {
      const { attribute } = req.body;
      result = await page.getAttribute(selector, attribute);
    } else {
      return res.status(400).json({ ok: false, error: "Invalid mode" });
    }
    
    res.json({ ok: true, result });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.get("/links", async (req, res) => {
  try {
    await ensure();
    const { limit = 200 } = req.query;
    
    const links = await page.$$eval("a[href]", (as, limit) =>
      as.slice(0, limit).map(a => ({
        text: (a.innerText || "").trim().slice(0, 120),
        href: a.href,
        title: a.title || ""
      })),
      parseInt(limit)
    );
    
    res.json({ ok: true, count: links.length, links });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.get("/title", async (req, res) => {
  try {
    await ensure();
    const title = await page.title();
    res.json({ ok: true, title, url: page.url() });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// SCREENSHOTS & MEDIA
// ============================================================================

app.get("/screenshot", async (req, res) => {
  try {
    await ensure();
    const { fullPage = true } = req.query;
    const path = `screenshots/shot-${Date.now()}.png`;
    
    await page.screenshot({ path, fullPage: fullPage === 'true' });
    res.json({ ok: true, path });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.get("/pdf", async (req, res) => {
  try {
    await ensure();
    const path = `pdfs/page-${Date.now()}.pdf`;
    await page.pdf({ path, format: 'A4' });
    res.json({ ok: true, path });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// COOKIES & STORAGE
// ============================================================================

app.get("/cookies", async (req, res) => {
  try {
    await ensure();
    const cookies = await page.context().cookies();
    res.json({ ok: true, cookies });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/cookies/set", async (req, res) => {
  try {
    await ensure();
    const { cookies } = req.body;
    
    if (!Array.isArray(cookies)) {
      return res.status(400).json({ ok: false, error: "Cookies must be an array" });
    }
    
    await page.context().addCookies(cookies);
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/cookies/clear", async (req, res) => {
  try {
    await ensure();
    await page.context().clearCookies();
    res.json({ ok: true });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// UTILITY & STATUS
// ============================================================================

app.get("/status", async (req, res) => {
  try {
    const isReady = browser && page;
    res.json({ 
      ok: true, 
      ready: isReady,
      url: isReady ? page.url() : null,
      title: isReady ? await page.title() : null
    });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.post("/close", async (req, res) => {
  try {
    if (page) await page.close();
    if (browser) await browser.close();
    page = null;
    browser = null;
    res.json({ ok: true, message: "Browser closed" });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

app.get("/eval", async (req, res) => {
  try {
    await ensure();
    const { code } = req.query;
    
    if (!code) {
      return res.status(400).json({ ok: false, error: "Code required" });
    }
    
    const result = await page.evaluate(code);
    res.json({ ok: true, result });
  } catch (e) {
    res.status(500).json({ ok: false, error: String(e) });
  }
});

// ============================================================================
// SERVER
// ============================================================================

const PORT = process.env.PORT || 3000;

app.listen(PORT, () => {
  console.log("=" .repeat(60));
  console.log("🌐 Browser Controller Server");
  console.log("=" .repeat(60));
  console.log(`✓ Server running on http://localhost:${PORT}`);
  console.log(`✓ Headless mode: ${CONFIG.headless}`);
  console.log(`✓ Domain whitelist: ${CONFIG.allowedDomains.length > 0 ? CONFIG.allowedDomains.join(', ') : 'All domains allowed'}`);
  console.log("=" .repeat(60));
  console.log("\n📝 Available endpoints:");
  console.log("  Navigation:");
  console.log("    POST /open          - Open URL");
  console.log("    POST /nav/back      - Go back");
  console.log("    POST /nav/forward   - Go forward");
  console.log("    POST /reload        - Reload page");
  console.log("\n  Interactions:");
  console.log("    POST /click         - Click element");
  console.log("    POST /type          - Type text");
  console.log("    POST /scroll        - Scroll page");
  console.log("    POST /wait          - Wait for selector");
  console.log("    POST /hover         - Hover element");
  console.log("\n  Content:");
  console.log("    GET  /content/text  - Get page text");
  console.log("    GET  /content/html  - Get page HTML");
  console.log("    POST /extract       - Extract by selector");
  console.log("    GET  /links         - Get all links");
  console.log("    GET  /title         - Get page title");
  console.log("\n  Media:");
  console.log("    GET  /screenshot    - Take screenshot");
  console.log("    GET  /pdf           - Generate PDF");
  console.log("\n  Cookies:");
  console.log("    GET  /cookies       - Get cookies");
  console.log("    POST /cookies/set   - Set cookies");
  console.log("    POST /cookies/clear - Clear cookies");
  console.log("\n  Utility:");
  console.log("    GET  /status        - Check status");
  console.log("    POST /close         - Close browser");
  console.log("    GET  /eval          - Execute JS");
  console.log("=" .repeat(60));
});

// Graceful shutdown
process.on('SIGINT', async () => {
  console.log('\n\n🛑 Shutting down...');
  if (page) await page.close();
  if (browser) await browser.close();
  process.exit(0);
});
