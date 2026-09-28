#!/usr/bin/env python3
"""Inject canonical/OG/twitter meta + LocalBusiness JSON-LD + visible breadcrumbs
into the existing hand-written static pages (everything except the generated
/yachts/<slug>/ and /destinations/<slug>/ pages, which already have this)."""
import re, os, json

BASE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://pattayayachtrentals.com"
BUSINESS_NAME = "Pattaya Yacht Rentals"
PHONE = "+66653159096"
EMAIL = "info@yacht-charters-phuket.com"

LOCAL_BUSINESS = {
    "@context": "https://schema.org",
    "@type": "TravelAgency",
    "name": BUSINESS_NAME,
    "url": SITE_URL,
    "telephone": PHONE,
    "email": EMAIL,
    "image": f"{SITE_URL}/images/og-default.jpg",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Ao Po Grand Marina",
        "addressLocality": "Phuket",
        "postalCode": "83110",
        "addressCountry": "TH",
    },
    "sameAs": [],
}

# path -> (canonical path, breadcrumb list of (name, url) or None to skip breadcrumb)
PAGES = {
    "index.html": ("/", None),
    "yachts.html": ("/yachts.html", [("Home", "/"), ("Yachts", "/yachts.html")]),
    "prices.html": ("/prices.html", [("Home", "/"), ("Prices & Planning", "/prices.html")]),
    "about.html": ("/about.html", [("Home", "/"), ("About", "/about.html")]),
    "contact.html": ("/contact.html", [("Home", "/"), ("Contact", "/contact.html")]),
    "faq.html": ("/faq.html", [("Home", "/"), ("FAQ", "/faq.html")]),
    "booking-terms.html": ("/booking-terms.html", [("Home", "/"), ("Booking Terms", "/booking-terms.html")]),
    "privacy-policy.html": ("/privacy-policy.html", [("Home", "/"), ("Privacy Policy", "/privacy-policy.html")]),
    "day-charters.html": ("/day-charters.html", [("Home", "/"), ("Day Charters", "/day-charters.html")]),
    "destinations/index.html": ("/destinations/index.html", [("Home", "/"), ("Destinations", "/destinations/index.html")]),
}

def breadcrumb_html(items):
    parts = []
    for i, (name, url) in enumerate(items):
        if i == len(items) - 1:
            parts.append(f'<span aria-current="page">{name}</span>')
        else:
            parts.append(f'<a href="{url}" class="hover:underline">{name}</a> / ')
    return "".join(parts)

def breadcrumb_jsonld(items):
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": name, "item": SITE_URL + url}
            for i, (name, url) in enumerate(items)
        ],
    }

def process(rel_path, canonical_path, breadcrumb_items):
    full_path = os.path.join(BASE, rel_path)
    with open(full_path, encoding="utf-8") as f:
        content = f.read()

    if 'rel="canonical"' in content:
        print(f"SKIP (already has canonical): {rel_path}")
        return

    title_m = re.search(r"<title>(.*?)</title>", content, re.S)
    desc_m = re.search(r'<meta name="description" content="(.*?)">', content, re.S)
    title = title_m.group(1).strip() if title_m else BUSINESS_NAME
    description = desc_m.group(1).strip() if desc_m else ""
    canonical = SITE_URL + canonical_path

    jsonld_blocks = [LOCAL_BUSINESS]
    if breadcrumb_items:
        jsonld_blocks.append(breadcrumb_jsonld(breadcrumb_items))
    jsonld_html = "\n".join(
        f'<script type="application/ld+json">{json.dumps(j)}</script>' for j in jsonld_blocks
    )

    meta_block = f"""<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/images/og-default.jpg">
<meta property="og:site_name" content="{BUSINESS_NAME}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE_URL}/images/og-default.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
{jsonld_html}
"""

    # Insert right after the description meta tag (or after <title> if no description)
    anchor = desc_m.group(0) if desc_m else title_m.group(0)
    content = content.replace(anchor, anchor + "\n" + meta_block, 1)

    # Insert a visible breadcrumb line right before the first <h1 in the page body,
    # but only if one isn't already present and the page has a hero section.
    if breadcrumb_items and "aria-label=\"Breadcrumb\"" not in content:
        h1_match = re.search(r'(<h1[^>]*>)', content)
        if h1_match:
            nav_html = f'<nav class="text-sm text-cream/60 mb-2" aria-label="Breadcrumb">{breadcrumb_html(breadcrumb_items)}</nav>\n    '
            content = content[:h1_match.start()] + nav_html + content[h1_match.start():]

    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Updated: {rel_path}")

def main():
    for rel_path, (canonical_path, breadcrumb_items) in PAGES.items():
        process(rel_path, canonical_path, breadcrumb_items)

if __name__ == "__main__":
    main()
