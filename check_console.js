const puppeteer = require("puppeteer-core");
const fs = require("fs");

const BASE = "http://localhost:8080";

const fleet = JSON.parse(fs.readFileSync("/tmp/fleet.json"));
const destinations = JSON.parse(fs.readFileSync("/tmp/destinations.json"));

const staticPages = [
  "/", "/yachts/", "/prices/", "/about/", "/contact/",
  "/faq/", "/booking-terms/", "/privacy-policy/",
  "/day-charters/", "/destinations/",
  "/404.html",
];

const yachtPages = fleet.map(y => `/yachts/${y.slug}/`);
const destPages = destinations.map(d => `/destinations/${d.slug}/`);

// Sample a subset of yacht pages (all 49 would be slow) plus all static + all destinations.
const sampleYachts = [yachtPages[0], yachtPages[10], yachtPages[24], yachtPages[48]];

const allPages = [...staticPages, ...destPages, ...sampleYachts];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: "/usr/bin/google-chrome",
    headless: "new",
    args: ["--no-sandbox", "--disable-gpu"],
  });

  let totalIssues = 0;

  for (const path of allPages) {
    const page = await browser.newPage();
    const issues = [];

    page.on("console", (msg) => {
      const type = msg.type();
      if (type === "error" || type === "warning") {
        issues.push(`[console.${type}] ${msg.text()}`);
      }
    });
    page.on("pageerror", (err) => issues.push(`[pageerror] ${err.message}`));
    page.on("requestfailed", (req) => {
      issues.push(`[requestfailed] ${req.url()} (${req.failure()?.errorText})`);
    });
    page.on("response", (res) => {
      if (res.status() >= 400) {
        issues.push(`[http ${res.status()}] ${res.url()}`);
      }
    });

    try {
      await page.goto(BASE + path, { waitUntil: "networkidle0", timeout: 15000 });
    } catch (e) {
      issues.push(`[navigation error] ${e.message}`);
    }

    if (issues.length) {
      console.log(`\n=== ${path} ===`);
      issues.forEach(i => console.log("  " + i));
      totalIssues += issues.length;
    }
    await page.close();
  }

  console.log(`\nChecked ${allPages.length} pages. Total issues: ${totalIssues}`);
  await browser.close();
  process.exit(totalIssues > 0 ? 1 : 0);
})();
