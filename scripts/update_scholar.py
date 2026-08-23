#!/usr/bin/env python3
import html
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

PROFILE_URL = "https://scholar.google.com/citations?user=vpClRiIAAAAJ&hl=en&pagesize=100"
ROOT = Path(__file__).resolve().parents[1]


def clean(value):
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


request = urllib.request.Request(
    PROFILE_URL,
    headers={"User-Agent": "Mozilla/5.0 (compatible; publication-sync/1.0)"},
)
with urllib.request.urlopen(request, timeout=30) as response:
    page = response.read().decode("utf-8")

rows = re.findall(r'<tr class="gsc_a_tr">(.*?)</tr>', page, re.DOTALL)
publications = []
for row in rows:
    title_match = re.search(
        r'<a(?=[^>]*class="gsc_a_at")(?=[^>]*href="([^"]+)")[^>]*>(.*?)</a>',
        row,
        re.DOTALL,
    )
    metadata = re.findall(r'<div class="gs_gray">(.*?)</div>', row, re.DOTALL)
    year_match = re.search(r'<span class="gsc_a_h[^>]*>(.*?)</span>', row, re.DOTALL)
    if not title_match:
        continue
    year = clean(year_match.group(1)) if year_match else ""
    venue = clean(metadata[1]) if len(metadata) > 1 else ""
    if year:
        venue = re.sub(rf",?\s*{re.escape(year)}$", "", venue)
    publications.append({
        "title": clean(title_match.group(2)),
        "authors": clean(metadata[0]) if metadata else "",
        "venue": venue,
        "year": year,
        "url": urllib.parse.urljoin("https://scholar.google.com", html.unescape(title_match.group(1))),
    })

if not publications:
    raise RuntimeError("Google Scholar returned no publications; keeping the existing data.")

publications.sort(key=lambda item: item["year"], reverse=True)
(ROOT / "publications.json").write_text(
    json.dumps(publications, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
