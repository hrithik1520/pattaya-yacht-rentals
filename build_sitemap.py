#!/usr/bin/env python3
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
SITE_URL = "https://pattayayachtrentals.com"

with open("/tmp/fleet.json") as f:
    FLEET = json.load(f)
with open("/tmp/destinations.json") as f:
    DESTINATIONS = json.load(f)

STATIC_PAGES = [
    ("/", "1.0"),
    ("/yachts/", "0.9"),
    ("/prices/", "0.7"),
    ("/day-charters/", "0.8"),
    ("/destinations/", "0.8"),
    ("/about/", "0.5"),
    ("/contact/", "0.6"),
    ("/faq/", "0.6"),
    ("/booking-terms/", "0.3"),
    ("/privacy-policy/", "0.3"),
]

urls = list(STATIC_PAGES)
urls += [(f"/yachts/{y['slug']}/", "0.8") for y in FLEET]
urls += [(f"/destinations/{d['slug']}/", "0.7") for d in DESTINATIONS]

entries = "\n".join(
    f'  <url>\n    <loc>{SITE_URL}{path}</loc>\n    <priority>{priority}</priority>\n  </url>'
    for path, priority in urls
)

sitemap = f'''<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{entries}
</urlset>
'''

with open(os.path.join(BASE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write(sitemap)

print(f"Wrote sitemap.xml with {len(urls)} URLs")
