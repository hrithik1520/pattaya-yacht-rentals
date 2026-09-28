#!/usr/bin/env python3
"""Static site generator for yacht + destination detail pages.
Reads /tmp/fleet.json and /tmp/destinations.json (exported from js/data.js and
js/destinations.js) and emits real static HTML files with unique per-page
title/meta description/canonical/OG/twitter tags, one H1, visible breadcrumbs,
BreadcrumbList + Product/Place JSON-LD, and real alt text on every image.
"""
import json, os, html

BASE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://pattayayachtrentals.com"  # placeholder domain until a real one is confirmed
BUSINESS_NAME = "Pattaya Yacht Rentals"
PHONE = "+66653159096"
PHONE_DISPLAY = "+66 65 315 9096"
EMAIL = "info@yacht-charters-phuket.com"
ADDRESS_STREET = "Ao Po Grand Marina"
ADDRESS_LOCALITY = "Phuket"
ADDRESS_POSTAL = "83110"
ADDRESS_COUNTRY = "TH"

with open("/tmp/fleet.json") as f:
    FLEET = json.load(f)
with open("/tmp/destinations.json") as f:
    DESTINATIONS = json.load(f)

HEAD_LIBS = """<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/tailwind.css">
<link rel="stylesheet" href="/css/style.css">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">"""

def esc(s):
    return html.escape(str(s), quote=True)

def local_business_jsonld():
    return {
        "@context": "https://schema.org",
        "@type": "TravelAgency",
        "name": BUSINESS_NAME,
        "url": SITE_URL,
        "telephone": PHONE,
        "email": EMAIL,
        "image": f"{SITE_URL}/images/og-default.jpg",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": ADDRESS_STREET,
            "addressLocality": ADDRESS_LOCALITY,
            "postalCode": ADDRESS_POSTAL,
            "addressCountry": ADDRESS_COUNTRY,
        },
        "sameAs": [],
    }

def breadcrumb_jsonld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": url}
            for i, (name, url) in enumerate(items)
        ],
    }

def breadcrumb_html(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{esc(name)}</span>')
        else:
            parts.append(f'<a href="{url}" class="hover:underline">{esc(name)}</a> / ')
    return "".join(parts)

def page_shell(*, title, description, canonical, og_image, body, extra_jsonld=None, robots=None):
    jsonld_blocks = [local_business_jsonld()]
    if extra_jsonld:
        jsonld_blocks.extend(extra_jsonld)
    jsonld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(j)}</script>' for j in jsonld_blocks
    )
    robots_tag = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{canonical}">
{robots_tag}<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{og_image}">
<meta property="og:site_name" content="{esc(BUSINESS_NAME)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(title)}">
<meta name="twitter:description" content="{esc(description)}">
<meta name="twitter:image" content="{og_image}">
{HEAD_LIBS}
{jsonld_html}
</head>
<body>
<div id="site-header"></div>
{body}
<div id="site-footer"></div>
<script src="/js/data.js"></script>
<script src="/js/destinations.js"></script>
<script src="/js/layout.js"></script>
<script>mountLayout("");</script>
</body>
</html>
"""

# ---------- Yacht pages ----------

def render_yacht(y):
    slug = y["slug"]
    name = y["name"]
    canonical = f"{SITE_URL}/yachts/{slug}/"
    title = f"{name} Yacht Charter | Up to {y['maxGuests']} Guests"
    description = f"Explore {name}, a {y['type']} for up to {y['maxGuests']} guests. See facilities, trip options and inclusions; request a current quote."
    og_image = f"{SITE_URL}{y['image']}" if y.get("image") else f"{SITE_URL}/images/og-default.jpg"

    gallery = y.get("gallery") or ([y["image"]] if y.get("image") else [])
    thumbs_html = "\n".join(
        f'<button class="thumb-btn aspect-square rounded-lg overflow-hidden border {"border-teal" if i == 0 else "border-transparent"}" data-src="{src}">'
        f'<img src="{src}" class="w-full h-full object-cover" alt="{esc(name)} — photo {i+1} of {len(gallery)}" loading="lazy" width="200" height="200"></button>'
        for i, src in enumerate(gallery)
    )

    breadcrumb_items = [("Home", f"{SITE_URL}/"), ("Yachts", f"{SITE_URL}/yachts.html"), (name, canonical)]

    product_jsonld = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": description,
        "image": [f"{SITE_URL}{g}" for g in gallery] or [og_image],
        "brand": {"@type": "Brand", "name": y["type"]},
        "offers": {
            "@type": "Offer",
            "priceCurrency": y["currency"],
            "price": y["priceCurrent"],
            "availability": "https://schema.org/InStoreOnly",
            "url": canonical,
        },
    }

    hero_img = gallery[0] if gallery else "/images/og-default.jpg"
    banner_img = gallery[1] if len(gallery) > 1 else hero_img

    body = f"""
<section class="hero-full" style="min-height:56vh;background-image:url('{banner_img}')">
  <div class="hero-full-inner max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pb-10 pt-28 text-cream">
    <nav class="text-sm text-cream/60" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
    <h1 class="font-serif text-3xl sm:text-5xl mt-2">{esc(name)} <span class="italic-accent">—</span> a private charter for your group</h1>
    <p class="mt-3 text-cream/85 max-w-2xl">Bring up to {y['maxGuests']} guests aboard {esc(name)} ({esc(y['type'])}) for a relaxed island day or celebration. Charters depart from Ao Po Grand Marina, Phuket. Tell us your date and group size and we'll confirm the best route and final price.</p>
  </div>
</section>

<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
  <div class="aspect-[16/9] rounded-2xl overflow-hidden bg-navy">
    <img id="heroImg" src="{hero_img}" class="w-full h-full object-cover" alt="{esc(name)} — {esc(y['type'])} yacht charter, main view" width="1600" height="900">
  </div>
  <div id="thumbRow" class="grid grid-cols-4 sm:grid-cols-8 gap-2 mt-3">
{thumbs_html}
  </div>
  <p class="text-xs text-navy/50 mt-2">Photos of this specific vessel. Confirm current condition and layout before your charter.</p>
</section>
<script>
  document.querySelectorAll(".thumb-btn").forEach(btn => {{
    btn.addEventListener("click", () => {{
      document.getElementById("heroImg").src = btn.dataset.src;
      document.querySelectorAll(".thumb-btn").forEach(b => b.classList.replace("border-teal", "border-transparent"));
      btn.classList.replace("border-transparent", "border-teal");
    }});
  }});
</script>

<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 grid lg:grid-cols-3 gap-10 pb-16">
  <div class="lg:col-span-2 space-y-10">
    <div>
      <h2 class="font-serif text-2xl text-navy mb-4">At a glance</h2>
      <div class="grid grid-cols-2 sm:grid-cols-3 gap-4 text-sm">
        <div class="card p-3"><p class="text-navy/50 text-xs">Max guests</p><p class="font-semibold text-navy">{y['maxGuests']}</p></div>
        <div class="card p-3"><p class="text-navy/50 text-xs">Cabins</p><p class="font-semibold text-navy">{y['cabins']}</p></div>
        <div class="card p-3"><p class="text-navy/50 text-xs">Length</p><p class="font-semibold text-navy">{esc(y['length'])}</p></div>
        <div class="card p-3"><p class="text-navy/50 text-xs">Top speed</p><p class="font-semibold text-navy">{y['topSpeed']} knots</p></div>
        <div class="card p-3"><p class="text-navy/50 text-xs">Departure</p><p class="font-semibold text-navy">Ao Po Grand Marina</p></div>
        <div class="card p-3"><p class="text-navy/50 text-xs">Type</p><p class="font-semibold text-navy">{esc(y['type'])}</p></div>
      </div>
    </div>
    <div>
      <h2 class="font-serif text-2xl text-navy mb-3">Pick a trip length</h2>
      <div class="grid sm:grid-cols-3 gap-4">
        <div class="card p-4"><p class="font-semibold text-navy">4 hours</p><p class="text-sm text-navy/60 mt-1">Cruising and a single stop.</p></div>
        <div class="card p-4"><p class="font-semibold text-navy">6 hours</p><p class="text-sm text-navy/60 mt-1">More time for swimming.</p></div>
        <div class="card p-4"><p class="font-semibold text-navy">8 hours</p><p class="text-sm text-navy/60 mt-1">A full island day.</p></div>
      </div>
      <p class="text-xs text-navy/50 mt-3">Confirm which durations this specific vessel offers before booking.</p>
    </div>
    <div class="grid sm:grid-cols-2 gap-8">
      <div>
        <h2 class="font-serif text-xl text-navy mb-3">Included with this boat</h2>
        <ul class="text-sm text-navy/70 space-y-2 list-disc list-inside">
          <li>Captain and crew</li>
          <li>Fuel for the confirmed route</li>
          <li>Life jackets and safety equipment</li>
        </ul>
      </div>
      <div>
        <h2 class="font-serif text-xl text-navy mb-3">Extra costs &amp; choices</h2>
        <ul class="text-sm text-navy/70 space-y-2 list-disc list-inside">
          <li>Catering and drinks &mdash; ask for menu</li>
          <li>Water toys &mdash; where available</li>
          <li>Overtime beyond confirmed hours</li>
        </ul>
      </div>
    </div>
    <div>
      <h2 class="font-serif text-xl text-navy mb-3">Before you confirm</h2>
      <p class="text-sm text-navy/70">Review deposit, balance date and weather/cancellation terms in our <a href="/booking-terms.html" class="text-teal underline">booking terms</a> before paying.</p>
    </div>
    <div>
      <h2 class="font-serif text-xl text-navy mb-3">Frequently asked questions</h2>
      <div class="space-y-3">
        <details class="card p-4"><summary class="font-semibold text-sm flex justify-between">Is {esc(name)} available on my date?<span class="chev">&#9662;</span></summary><p class="text-sm text-navy/70 mt-2">Send your date and we'll confirm availability before quoting.</p></details>
        <details class="card p-4"><summary class="font-semibold text-sm flex justify-between">How many guests can come?<span class="chev">&#9662;</span></summary><p class="text-sm text-navy/70 mt-2">This yacht is licensed for up to {y['maxGuests']} guests.</p></details>
        <details class="card p-4"><summary class="font-semibold text-sm flex justify-between">Where do we board?<span class="chev">&#9662;</span></summary><p class="text-sm text-navy/70 mt-2">Charters depart from Ao Po Grand Marina, Phuket; exact instructions are confirmed with your booking.</p></details>
      </div>
    </div>
  </div>

  <aside class="lg:sticky lg:top-20 h-fit">
    <div class="card p-6">
      <p class="font-serif text-xl text-navy">{esc(name)}</p>
      <p class="text-teal font-semibold mt-1">From {'$' if y['currency'] == 'USD' else '฿'}{y['priceCurrent']:,}</p>
      <p class="text-xs text-navy/50">Ask for current rate &mdash; conditions apply</p>
      <a href="/contact.html?boat={slug}" class="btn-primary w-full text-center block mt-4">Check availability for my date</a>
      <a href="/yachts.html" class="btn-secondary w-full text-center block mt-2">Show me similar yachts</a>
    </div>
  </aside>
</section>
"""
    return page_shell(
        title=title, description=description, canonical=canonical, og_image=og_image,
        body=body, extra_jsonld=[breadcrumb_jsonld(breadcrumb_items), product_jsonld],
    )

# ---------- Destination pages ----------

def render_destination(d, all_dests):
    slug = d["slug"]
    name = d["name"]
    canonical = f"{SITE_URL}/destinations/{slug}/"
    title = f"{name} Yacht Charter | Phuket Destinations"
    description = f"Plan a private yacht trip to {name} from Phuket. {d['tagline']}"
    og_image = f"{SITE_URL}{d['image']}" if d.get("image") else f"{SITE_URL}/images/og-default.jpg"
    breadcrumb_items = [("Home", f"{SITE_URL}/"), ("Destinations", f"{SITE_URL}/destinations/index.html"), (name, canonical)]

    place_jsonld = {
        "@context": "https://schema.org",
        "@type": "TouristDestination",
        "name": name,
        "description": d["intro"],
        "url": canonical,
    }
    if d.get("image"):
        place_jsonld["image"] = og_image

    others = [x for x in all_dests if x["slug"] != slug][:6]
    other_cards = "\n".join(
        f'<a href="/destinations/{x["slug"]}/" class="card p-4 hover:-translate-y-1 transition">'
        f'<p class="font-semibold text-navy text-sm">{esc(x["name"])}</p>'
        f'<p class="text-xs text-navy/60 mt-1">{esc(x["tagline"])}</p></a>'
        for x in others
    )

    if d.get("image"):
        hero = f"""
<section class="hero-full" style="min-height:52vh;background-image:url('{d['image']}')">
  <div class="hero-full-inner max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pb-10 pt-28 text-cream">
    <nav class="text-sm text-cream/60" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
    <h1 class="font-serif text-4xl mt-2">{esc(name)}</h1>
    <p class="mt-3 text-cream/80 max-w-2xl">{esc(d['tagline'])}</p>
    <a href="/contact.html?destination={slug}" class="btn-pill-white inline-flex mt-6">Find yachts for this route <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>"""
        credit = d.get("imageCredit")
        if credit:
            hero += f"""
<p class="text-xs text-navy/40 max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 pt-2">Photo: {esc(credit['name'])} ({esc(credit['license'])}), <a href="{credit['url']}" class="underline" target="_blank" rel="noopener">source</a></p>"""
    else:
        hero = f"""
<section class="bg-navy text-cream">
  <div class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-14">
    <nav class="text-sm text-cream/60" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>
    <h1 class="font-serif text-4xl mt-2">{esc(name)}</h1>
    <p class="mt-3 text-cream/80 max-w-2xl">{esc(d['tagline'])}</p>
    <a href="/contact.html?destination={slug}" class="btn-pill-white inline-flex mt-6">Find yachts for this route <span aria-hidden="true">&rarr;</span></a>
  </div>
</section>"""

    body = f"""
{hero}

<section class="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-14 space-y-10">
  <div>
    <h2 class="font-serif text-2xl text-navy mb-3">About this route</h2>
    <p class="text-navy/70">{esc(d['intro'])}</p>
  </div>
  <div class="grid sm:grid-cols-2 gap-6">
    <div class="card p-5">
      <p class="text-xs uppercase tracking-wide text-teal font-semibold">Good for</p>
      <p class="text-navy/80 mt-2 text-sm">{esc(d['goodFor'])}</p>
    </div>
    <div class="card p-5">
      <p class="text-xs uppercase tracking-wide text-teal font-semibold">Travel time</p>
      <p class="text-navy/80 mt-2 text-sm">{esc(d['travelTime'])}</p>
    </div>
  </div>
  <div>
    <h2 class="font-serif text-2xl text-navy mb-3">Check before confirming</h2>
    <p class="text-navy/70">Ask which vessel suits this route, whether it's a half-day, full-day or overnight trip, what's included, and whether route-related fees apply. The captain and operator confirm the final itinerary based on conditions on the day.</p>
  </div>
  <div class="grid sm:grid-cols-3 gap-4 text-sm text-center">
    <a href="/yachts.html" class="card p-4 hover:-translate-y-1 transition">Compare yachts</a>
    <a href="/day-charters.html" class="card p-4 hover:-translate-y-1 transition">Day charter planning</a>
    <a href="/contact.html?destination={slug}" class="card p-4 hover:-translate-y-1 transition !bg-teal !text-white">Ask about this route</a>
  </div>
  <div>
    <h2 class="font-serif text-xl text-navy mb-4">Other destinations</h2>
    <div class="grid sm:grid-cols-3 gap-4">
{other_cards}
    </div>
  </div>
</section>
"""
    return page_shell(
        title=title, description=description, canonical=canonical, og_image=og_image,
        body=body, extra_jsonld=[breadcrumb_jsonld(breadcrumb_items), place_jsonld],
    )

def main():
    for y in FLEET:
        out_dir = os.path.join(BASE, "yachts", y["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_yacht(y))

    for d in DESTINATIONS:
        out_dir = os.path.join(BASE, "destinations", d["slug"])
        os.makedirs(out_dir, exist_ok=True)
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_destination(d, DESTINATIONS))

    print(f"Generated {len(FLEET)} yacht pages and {len(DESTINATIONS)} destination pages.")

if __name__ == "__main__":
    main()
