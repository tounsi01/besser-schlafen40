"""
Regenerate sitemap index + sitemap-pages.xml + sitemap-articles.xml.
Writes to public/ and project root (same filenames) for flexible deploys.
"""
from __future__ import annotations

from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
ARTIKEL = ROOT / "artikel"
PUBLIC = ROOT / "public"

BASE = "https://www.besser-schlafen40.de"
TODAY = date.today().isoformat()


def url_entry(loc: str, lastmod: str, changefreq: str | None, priority: str | None) -> str:
    parts = [f"    <loc>{escape(loc)}</loc>", f"    <lastmod>{lastmod}</lastmod>"]
    if changefreq:
        parts.append(f"    <changefreq>{changefreq}</changefreq>")
    if priority:
        parts.append(f"    <priority>{priority}</priority>")
    return "  <url>\n" + "\n".join(parts) + "\n  </url>\n"


def build_pages() -> str:
    """Non-article URLs: home, tools, legal, blog."""
    pages: list[tuple[str, str, str | None, str | None]] = [
        (f"{BASE}/", TODAY, "weekly", "1.0"),
        (f"{BASE}/artikel-uebersicht.html", TODAY, "weekly", "0.9"),
        (f"{BASE}/quiz/", TODAY, "monthly", "0.85"),
        (f"{BASE}/neowake.html", TODAY, "monthly", "0.85"),
        (f"{BASE}/blog/", TODAY, "weekly", "0.8"),
        (f"{BASE}/impressum.html", TODAY, "yearly", "0.4"),
        (f"{BASE}/datenschutz.html", TODAY, "yearly", "0.4"),
        (f"{BASE}/affiliate-disclosure.html", TODAY, "yearly", "0.35"),
    ]
    body = "".join(url_entry(loc, lm, cf, pr) for loc, lm, cf, pr in pages)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}"
        "</urlset>\n"
    )


def build_articles() -> str:
    files = sorted(
        p
        for p in ARTIKEL.glob("*.html")
        if p.name != "_vorlage-requete-seo.html"
    )
    parts: list[str] = []
    for p in files:
        try:
            mtime = date.fromtimestamp(p.stat().st_mtime).isoformat()
        except OSError:
            mtime = TODAY
        loc = f"{BASE}/artikel/{p.name}"
        pr = "0.95" if p.name == "schlafstoerungen-ab-40.html" else "0.8"
        parts.append(url_entry(loc, mtime, "weekly", pr))
    body = "".join(parts)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{body}"
        "</urlset>\n"
    )


def build_index() -> str:
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{BASE}/sitemap-pages.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
  <sitemap>
    <loc>{BASE}/sitemap-articles.xml</loc>
    <lastmod>{TODAY}</lastmod>
  </sitemap>
</sitemapindex>
"""


def write_both(name: str, content: str) -> None:
    (PUBLIC / name).write_text(content, encoding="utf-8")
    (ROOT / name).write_text(content, encoding="utf-8")


def main() -> None:
    PUBLIC.mkdir(parents=True, exist_ok=True)
    write_both("sitemap-pages.xml", build_pages())
    write_both("sitemap-articles.xml", build_articles())
    idx = build_index()
    (PUBLIC / "sitemap.xml").write_text(idx, encoding="utf-8")
    (ROOT / "sitemap.xml").write_text(idx, encoding="utf-8")
    print("OK: sitemap.xml, sitemap-pages.xml, sitemap-articles.xml (public/ + root)")


if __name__ == "__main__":
    main()
