# Pattaya Yacht Rentals

Static marketing + lead-generation site for a private yacht charter business. Visitors browse the fleet by guest count/type, read destination guides, and submit a charter enquiry; nothing is a live booking engine — every quote is confirmed by the team before payment.

**Live locally at:** `http://localhost:8080/` (see [Local development](#local-development)) — **not yet deployed or pushed anywhere.**

## Stack

Plain HTML + vanilla JS + Tailwind CSS (compiled locally, no CDN, no framework). No backend — the "database" is two JS arrays (`js/data.js`, `js/destinations.js`) read by both the browser and the Python build scripts that generate static pages from them.

- **Styling:** Tailwind CSS v3, compiled to a single purged `css/tailwind.css` (no runtime JS, no source map) + `css/style.css` for hand-written components (buttons, cards, hero, marquee).
- **Fonts:** DM Serif Display (headings) + Manrope (body), loaded from Google Fonts.
- **Build tooling:** Node/npm (Tailwind CLI, Puppeteer for verification) + Python 3 (page generation, image processing). Neither is needed to *view* the site, only to regenerate it after a data/content change.

## Project structure

```
index.html, yachts.html, prices.html, about.html, contact.html,
faq.html, booking-terms.html, privacy-policy.html, 404.html   → hand-written top-level pages
experiences/                                                   → experience landing pages (hand-written)
destinations/index.html                                        → destinations hub (hand-written)
destinations/<slug>/index.html                                 → one page per destination (generated)
yachts/<slug>/index.html                                        → one page per boat (generated)
js/data.js            → the fleet: source of truth for every boat's price/specs/photos
js/destinations.js    → the 9 real Phuket routes the fleet serves
js/layout.js          → shared header/footer/mobile-nav, injected on every page
css/tailwind-input.css → Tailwind entry point → compiled to css/tailwind.css (don't hand-edit the output)
css/style.css          → hand-written components (buttons, cards, hero-full, marquee, dark-card)
images/<slug>/NN.webp  → real downloaded/optimized photos per boat (8 each, max 1600px wide)
build_pages.py         → generates yachts/<slug>/ and destinations/<slug>/ from data.js + destinations.js
build_sitemap.py       → generates sitemap.xml from the same data
inject_seo.py          → one-time script that added canonical/OG/JSON-LD to the hand-written pages
check_console.js       → headless-Chrome audit: console errors, failed requests, 4xx/5xx across every page
```

## Local development

```bash
python3 -m http.server 8080   # from the project root
```

Then open `http://localhost:8080/`. That's it — no build step required just to browse.

## Making changes

**Editing a boat's price/specs/photos, or adding a destination:**
1. Edit `js/data.js` or `js/destinations.js` directly (or edit the CSV + rerun the export — see below).
2. Regenerate the static pages and sitemap:
   ```bash
   node -e "const fs=require('fs');fs.writeFileSync('/tmp/fleet.json',JSON.stringify(new Function(fs.readFileSync('js/data.js','utf8')+';return FLEET;')(),null,2))"
   node -e "const fs=require('fs');fs.writeFileSync('/tmp/destinations.json',JSON.stringify(new Function(fs.readFileSync('js/destinations.js','utf8')+';return DESTINATIONS;')(),null,2))"
   npm run build:pages
   ```

**Editing a hand-written page's copy/layout:** just edit the `.html` file directly, no rebuild needed.

**Editing colors/spacing/adding a new Tailwind utility class:** edit `tailwind.config.js` if needed, then:
```bash
npm run build:css
```

**After any content or design change, verify nothing broke:**
```bash
npm run check   # headless Chrome: console errors, failed requests, HTTP 4xx/5xx across every page
```

## Image pipeline

Photos were sourced from the operator's own live fleet listings (the business this site represents actually operates/partners with these boats — see conversation history for how each batch was verified before download). Each boat gets up to 8 photos, downloaded, EXIF-corrected, downscaled to a max width of 1600px, and converted to WebP (~78 quality) — see the git history / prior build scripts for the exact pipeline if you need to add more boats later.

`images/azimut-55ft/` and `images/Satisfaction-65ft/` are leftover raw uploads for two boats not in the current fleet data (no verified price/specs yet) — safe to delete or wire in once you have real numbers for them.

## SEO / production readiness

- Every page (73 total: 49 yacht + 9 destination + 14 hand-written + 404) has a unique `<title>`, meta description, canonical tag, OG/Twitter card, exactly one `<h1>`, and real `alt` text — baked into static HTML, not injected by JS.
- `TravelAgency`/`LocalBusiness`, `BreadcrumbList`, and per-yacht `Product` JSON-LD schema throughout.
- `sitemap.xml`, `robots.txt`, `llms.txt`, custom `404.html`, full favicon set, and a generated 1200×630 social share image all present at the site root.
- Verified with headless Chrome (`check_console.js`): 0 console errors, 0 failed requests, 0 4xx/5xx across every page.

## Known placeholders — resolve before going live

- **Domain:** canonical/OG URLs currently point to `https://www.pattayayachtrentals.com` (not a real, confirmed domain). Find/replace the `SITE_URL` constant in `build_pages.py` and `inject_seo.py` once you have one, then rerun both.
- **Booking terms & privacy policy:** written honestly but without invented numbers (deposit %, refund windows, legal entity name) — these need real input from the business/legal counsel, then a manual edit to `booking-terms.html` / `privacy-policy.html`.
- **Brand/location mismatch:** the site is branded "Pattaya Yacht Rentals" but the fleet and destinations are Phuket-based (a deliberate interim decision — see conversation history). Resolve before launch: either rebrand fully to Phuket, or clarify the Pattaya connection.
- **8 boats with no photos yet** (`image: ""` in `js/data.js`) — CSV had no source photo for these; add real photos when available rather than reusing another boat's.

## Deployment

Nothing has been pushed or deployed — this is local-only by request. It's a static site, so any static host (Netlify, Vercel, GitHub Pages, S3+CloudFront, etc.) works: upload everything except `node_modules/`, `package-lock.json`, and the `.py`/`.js` build scripts aren't required at runtime either (only the generated output matters).
