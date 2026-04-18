from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"C:\Users\a1_im\Documents\besser-schlafen40")
ARTICLE_DIR = ROOT / "artikel"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def extract(pattern: str, text: str, flags: int = re.I | re.S) -> str:
    m = re.search(pattern, text, flags)
    return m.group(1).strip() if m else ""


def count_links_to_target(files: list[Path], target_slug: str) -> int:
    total = 0
    rx = re.compile(r'href="([^"]+)"', re.I)
    for p in files:
        text = read_text(p)
        for href in rx.findall(text):
            if href.endswith(target_slug) or href == f"/artikel/{target_slug}":
                total += 1
    return total


def main() -> None:
    html_files = sorted([p for p in ROOT.rglob("*.html") if "besser-schlafen40\\besser-schlafen40\\" not in str(p)])
    article_files = sorted([p for p in ARTICLE_DIR.glob("*.html") if p.is_file()])

    title_missing = []
    meta_missing = []
    h1_missing = []
    canonical_non_www = []
    faq_count = 0
    noindex_follow = []
    noindex_other = []
    title_lengths = []
    meta_lengths = []
    duplicate_titles = Counter()
    duplicate_desc = Counter()
    link_targets = Counter()

    href_rx = re.compile(r'href="([^"]+)"', re.I)
    for p in html_files:
        text = read_text(p)
        rel = p.relative_to(ROOT).as_posix()
        title = extract(r"<title>(.*?)</title>", text)
        desc = extract(r'<meta\s+name="description"\s+content="(.*?)"\s*/?>', text)
        h1 = extract(r"<h1[^>]*>(.*?)</h1>", text)
        canonical = extract(r'<link\s+rel="canonical"\s+href="(.*?)"\s*/?>', text)
        robots = extract(r'<meta\s+name="robots"\s+content="(.*?)"\s*/?>', text)

        if not title:
            title_missing.append(rel)
        else:
            title_lengths.append((rel, len(title)))
            duplicate_titles[title] += 1
        if not desc:
            meta_missing.append(rel)
        else:
            meta_lengths.append((rel, len(desc)))
            duplicate_desc[desc] += 1
        if not h1:
            h1_missing.append(rel)
        if canonical and "https://www.besser-schlafen40.de" not in canonical:
            canonical_non_www.append((rel, canonical))

        if "noindex" in robots.lower():
            if "follow" in robots.lower() and "nofollow" not in robots.lower():
                noindex_follow.append(rel)
            else:
                noindex_other.append((rel, robots))

        if "<details>" in text:
            faq_count += 1

        for href in href_rx.findall(text):
            if href.startswith("/artikel/") and href.endswith(".html"):
                link_targets[href] += 1

    internal_links_to = {
        "hormonelle-schlafprobleme-ab-40.html": count_links_to_target(
            html_files, "hormonelle-schlafprobleme-ab-40.html"
        ),
        "cortisol-nachts-wach-ab-40.html": count_links_to_target(
            html_files, "cortisol-nachts-wach-ab-40.html"
        ),
        "welches-magnesium-fuer-schlaf-ab-40.html": count_links_to_target(
            html_files, "welches-magnesium-fuer-schlaf-ab-40.html"
        ),
    }

    weakly_linked_articles = []
    for p in article_files:
        slug = p.name
        target = f"/artikel/{slug}"
        c = link_targets[target]
        if c < 2:
            weakly_linked_articles.append((slug, c))

    bad_title_lengths = [t for t in title_lengths if t[1] < 35 or t[1] > 65]
    bad_meta_lengths = [m for m in meta_lengths if m[1] < 120 or m[1] > 165]

    dupe_titles = [(k, v) for k, v in duplicate_titles.items() if v > 1]
    dupe_desc = [(k, v) for k, v in duplicate_desc.items() if v > 1]

    print("TOTAL_HTML", len(html_files))
    print("TOTAL_ARTICLES", len(article_files))
    print("TITLE_MISSING", len(title_missing))
    print("META_MISSING", len(meta_missing))
    print("H1_MISSING", len(h1_missing))
    print("CANONICAL_NON_WWW", len(canonical_non_www))
    print("FAQ_PAGES_WITH_DETAILS", faq_count)
    print("NOINDEX_FOLLOW", len(noindex_follow))
    print("NOINDEX_OTHER", len(noindex_other))
    print("BAD_TITLE_LENGTH", len(bad_title_lengths))
    print("BAD_META_LENGTH", len(bad_meta_lengths))
    print("DUPLICATE_TITLES", len(dupe_titles))
    print("DUPLICATE_DESCRIPTIONS", len(dupe_desc))
    print("LINKS_TO_PRIORITY", internal_links_to)
    print("WEAKLY_LINKED_ARTICLES", weakly_linked_articles[:15])
    if title_missing:
        print("TITLE_MISSING_FILES", title_missing[:15])
    if meta_missing:
        print("META_MISSING_FILES", meta_missing[:15])
    if canonical_non_www:
        print("CANONICAL_NON_WWW_FILES", canonical_non_www[:15])
    if noindex_other:
        print("NOINDEX_OTHER_FILES", noindex_other[:15])
    if bad_title_lengths:
        print("BAD_TITLE_LENGTH_FILES", bad_title_lengths[:15])
    if bad_meta_lengths:
        print("BAD_META_LENGTH_FILES", bad_meta_lengths[:15])


if __name__ == "__main__":
    main()
