"""
Insert mid-article conversion block (~30% content) + standardized Neowake final CTA.
Idempotent: safe to re-run (replaces existing conversion-mid / neowake-cta-end).
"""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parents[1]

MID_HTML = """<section class="card conversion-mid" aria-labelledby="conversion-mid-h">
<h2 id="conversion-mid-h">Warum du nicht schläfst (die wahre Ursache)</h2>
<p>Oft liegt es weniger an „Disziplin“ als an Erregung, Tagesrhythmus oder mentaler Last. In 30 Sekunden siehst du, welcher Hebel bei dir zuerst Sinn macht.</p>
<p class="conversion-mid__actions"><a class="button" href="/quiz/">Finde deine Lösung in 30 Sekunden</a></p>
</section>"""

FINAL_HTML = """<div class="neowake-cta-end" data-conversion-final="1">
<div class="card conversion-final">
<h2 class="conversion-final__title">Teste diese Methode heute Nacht</h2>
<p class="conversion-final__lede">Neowake: sanftes Schlafprogramm mit Audio-Routinen für Erwachsene 40+ — ohne Medikamente als Ausgangspunkt.</p>
<div class="conversion-final__actions">
<a class="button" href="https://neowake.de/jetzt-testen#aff=Amouna" rel="sponsored nofollow">Zu Neowake</a>
<a class="button alt" href="/neowake.html">Programm lesen</a>
</div>
<p class="muted conversion-final__hint">Affiliate-Link · <a href="/affiliate-disclosure.html">Hinweis</a></p>
</div>
</div>"""


def block_children(parent: Tag) -> list[Tag]:
    out: list[Tag] = []
    for c in parent.children:
        if not isinstance(c, Tag):
            continue
        cls = c.get("class") or []
        if c.name == "div" and "neowake-cta-end" in cls:
            continue
        if c.name == "section" and "conversion-mid" in cls:
            continue
        out.append(c)
    return out


def insert_mid_at_fraction(root: Tag, soup: BeautifulSoup, fraction: float = 0.3) -> None:
    nodes = block_children(root)
    if not nodes:
        return
    lengths = [len(c.get_text(strip=True)) for c in nodes]
    total = sum(lengths)
    if total == 0:
        insert_after_idx = min(0, len(nodes) - 1)
    else:
        target = total * fraction
        cum = 0
        insert_after_idx = 0
        for i, ln in enumerate(lengths):
            cum += ln
            insert_after_idx = i
            if cum >= target:
                break
    frag = BeautifulSoup(MID_HTML, "html.parser").find("section", class_="conversion-mid")
    if frag is None:
        return
    nodes[insert_after_idx].insert_after(frag)


def strip_old_mid(soup: BeautifulSoup) -> None:
    for el in soup.select("section.conversion-mid"):
        el.decompose()


def upsert_final(soup: BeautifulSoup, append_parent: Tag | None) -> None:
    new_outer = BeautifulSoup(FINAL_HTML, "html.parser").find("div", class_="neowake-cta-end")
    if new_outer is None:
        return
    old = soup.select_one("div.neowake-cta-end")
    if old is not None:
        old.replace_with(new_outer)
    elif append_parent is not None:
        append_parent.append(new_outer)


def resolve_root(rel: Path, soup: BeautifulSoup) -> tuple[Tag | None, Tag | None]:
    """
    Returns (root_for_mid_insert, append_parent_for_final_if_missing_neowake).
    append_parent is used when no neowake-cta-end exists yet.
    """
    s = rel.as_posix()
    if "artikel/" in s and s.endswith(".html"):
        art = soup.find("article")
        return (art, art)
    if s.endswith("quiz/index.html"):
        m = soup.select_one("main.section .container")
        return (m, m)
    if s.endswith("artikel-uebersicht.html"):
        m = soup.select_one("main.section .container")
        return (m, m)
    if s.endswith("blog/index.html"):
        m = soup.select_one("main.blog-page .container")
        if m:
            return (m, m)
        m = soup.select_one("main .container")
        return (m, m)
    if s == "index.html":
        m = soup.find("main")
        return (m, m)
    if s.endswith("neowake.html"):
        m = soup.find("main")
        return (m, m)
    if s in ("impressum.html", "datenschutz.html", "affiliate-disclosure.html"):
        m = soup.select_one("main.section .container")
        return (m, m)
    m = soup.find("main")
    return (m, m)


def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    soup = BeautifulSoup(raw, "html.parser")
    rel = path.relative_to(ROOT)
    root, append_parent = resolve_root(rel, soup)
    if root is None:
        print("SKIP no-root", rel)
        return False

    strip_old_mid(soup)
    insert_mid_at_fraction(root, soup, 0.3)
    upsert_final(soup, append_parent)

    new_raw = str(soup)
    if new_raw != raw:
        path.write_text(new_raw, encoding="utf-8")
        print("OK", rel)
        return True
    print("NOCHANGE", rel)
    return False


def main() -> None:
    targets: list[Path] = []
    targets.append(ROOT / "index.html")
    targets.append(ROOT / "artikel-uebersicht.html")
    targets.append(ROOT / "neowake.html")
    targets.append(ROOT / "impressum.html")
    targets.append(ROOT / "datenschutz.html")
    targets.append(ROOT / "affiliate-disclosure.html")
    targets.append(ROOT / "quiz" / "index.html")
    targets.append(ROOT / "blog" / "index.html")
    targets.extend(sorted((ROOT / "artikel").glob("*.html")))
    for p in targets:
        if p.exists():
            process_file(p)
        else:
            print("MISSING", p.relative_to(ROOT))


if __name__ == "__main__":
    main()
