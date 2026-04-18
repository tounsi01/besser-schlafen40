#!/usr/bin/env python3
"""
Boost internal /artikel/ links to 10-15 per page (target 12 new links when below 10).
Skips: _vorlage-requete-seo.html, files with >= 10 /artikel/ links already.
Inserts a contextual 'Themen-Netzwerk' section before </article> if not present.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIKEL = ROOT / "artikel"

# (slug, anchor) — natural German anchors; priority clusters: stress, sleep, magnesium, hormones
LINKS_STRESS = [
    ("schlafprobleme-stress-strategien.html", "Stress und Schlaf: sieben Strategien"),
    ("stressbedingte-schlafprobleme-ab-40.html", "stressbedingte Schlafprobleme ab 40"),
    ("job-stress-schlafen-ab-40.html", "Job-Stress und Schlaf ab 40"),
    ("jobstress-schlafprobleme-ab-40.html", "Jobstress und nächtliche Erschöpfung"),
    ("gedanken-kreisen-nachts-ab-40.html", "Gedankenkreisen nachts"),
    ("schlafstoerung-stress-arbeit.html", "Schlaf und Belastung durch Arbeit"),
    ("stress-abbauen-schlafen.html", "Stress im Alltag abbauen für den Schlaf"),
    ("schlecht-schlafen-stress.html", "schlechter Schlaf bei chronischem Stress"),
    ("nervensystem-beruhigen-schlafen.html", "Nervensystem beruhigen vor dem Schlaf"),
    ("stress-schlafprobleme-trotz-muedigkeit.html", "müde und trotzdem wach durch Stress"),
]

LINKS_SLEEP = [
    ("schlafstoerungen-ab-40.html", "Schlafstörungen ab 40 – Überblick"),
    ("was-tun-bei-schlafproblemen-leitfaden.html", "Leitfaden bei Schlafproblemen"),
    ("durchschlafen-ab-40-tipps.html", "Durchschlafen ab 40: praktische Tipps"),
    ("durchschlafen-probleme.html", "Schlafzyklen und Durchschlaf-Probleme"),
    ("warum-wache-ich-nachts-auf-ab-40.html", "nachts aufwachen ab 40"),
    ("warum-wache-ich-nachts-auf.html", "Aufwachen im Zeitfenster 2–4 Uhr"),
    ("nachts-aufwachen-nicht-wieder-einschlafen-ab-40.html", "aufwachen und nicht wieder einschlafen"),
    ("jede-nacht-wach-ab-40.html", "jede Nacht wach liegen"),
    ("einschlafen-dauert-lange.html", "wenn das Einschlafen lange dauert"),
    ("schlechter-schlaf-ab-40-ursachen.html", "Ursachen für schlechten Schlaf ab 40"),
    ("schlafqualitaet-verbessern.html", "Schlafqualität verstehen und beobachten"),
    ("besser-schlafen-tipps.html", "kurze Tipps für besseren Schlaf"),
    ("tiefer-schlaf-verbessern.html", "Tiefschlaf und Schlafqualität verbessern"),
]

LINKS_MG = [
    ("welches-magnesium-fuer-schlaf-ab-40.html", "welches Magnesium für den Schlaf ab 40"),
    ("magnesium-bei-schlafproblemen-wirkung-dosierung.html", "Magnesium: Wirkung und Dosierung"),
    ("magnesium-nachts-aufwachen-ab-40.html", "Magnesium bei nächtlichem Aufwachen"),
    ("welches-magnesium-zum-schlafen.html", "Magnesiumformen und empfindlicher Magen"),
    ("magnesium-oder-melatonin-schlafprobleme.html", "Magnesium oder Melatonin"),
    ("magnesium-abends-schlafprobleme-timing.html", "Magnesium abends – Timing"),
    ("magnesium-schlafen.html", "Magnesiummangel und Schlaf"),
    ("magnesium-wirkung-schlaf.html", "Studienlage zu Magnesium und Schlaf"),
]

LINKS_HORMONE = [
    ("hormonelle-schlafprobleme-ab-40.html", "hormonelle Schlafprobleme ab 40"),
    ("schlafprobleme-wechseljahre-ursachen-hilfe.html", "Schlaf in den Wechseljahren"),
    ("schlafprobleme-hormonell-checkliste.html", "Checkliste hormoneller Schlafstörungen"),
    ("cortisol-nachts-wach-ab-40.html", "Cortisol und nächtliches Wachsein"),
    ("cortisol-schlafen-problem.html", "Cortisol-Tagesrhythmus und Schlaf"),
    ("melatonin-weniger-ab-40-schlaf.html", "Melatonin und älter werden"),
    ("hormone-schlafstoerung.html", "Hormone und Schlaf – Begriffe"),
    ("wechseljahre-naechtliches-aufwachen-hilfe.html", "nächtliches Aufwachen in den Wechseljahren"),
]

MARKER = 'data-internal-net="clusters"'


def count_artikel_links(html: str) -> int:
    return len(re.findall(r'href="/artikel/[^"]+"', html))


def existing_slugs(html: str) -> set[str]:
    out = set()
    for m in re.finditer(r'href="/artikel/([^"]+)"', html):
        out.add(m.group(1))
    return out


def interleave_candidates(
    current_slug: str, have: set[str]
) -> list[tuple[str, str]]:
    """Round-robin across four pools; skip self and slugs already linked on page."""
    pools = [LINKS_STRESS, LINKS_SLEEP, LINKS_MG, LINKS_HORMONE]
    picked: list[tuple[str, str]] = []
    used: set[str] = {current_slug} | have
    max_rounds = max(len(p) for p in pools) + 5
    for _round in range(max_rounds):
        for pool in pools:
            if _round >= len(pool):
                continue
            slug, anchor = pool[_round]
            if slug in used:
                continue
            used.add(slug)
            picked.append((slug, anchor))
    return picked


def build_section(links: list[tuple[str, str]]) -> str:
    """Two flowing paragraphs with natural anchors, ~12 links."""
    if not links:
        return ""
    # Split into two sentences clusters
    half = max(1, (len(links) + 1) // 2)
    part1 = links[:half]
    part2 = links[half:]

    def fmt_chunk(chunk: list[tuple[str, str]]) -> str:
        bits = []
        for slug, anchor in chunk:
            bits.append(f'<a href="/artikel/{slug}">{anchor}</a>')
        # join with commas and 'und' before last in German style for readability
        if len(bits) == 1:
            return bits[0]
        if len(bits) == 2:
            return f"{bits[0]} und {bits[1]}"
        return ", ".join(bits[:-1]) + f" sowie {bits[-1]}"

    p1 = (
        f"<p>Rund um <strong>Stress, Psyche und Schlaf</strong> vernetzt dieser Ratgeber mit "
        f"{fmt_chunk(part1)}.</p>"
    )
    p2 = (
        f"<p>Für <strong>Schlafarchitektur, Magnesium und Hormone</strong> sind unter anderem "
        f"{fmt_chunk(part2)} hilfreich.</p>"
    )
    return (
        f'\n        <section class="card" {MARKER}>\n'
        f'          <h2>Themen-Netzwerk: Stress, Schlaf, Magnesium &amp; Hormone</h2>\n'
        f"          {p1}\n          {p2}\n"
        f'          <p class="muted">Hinweis: Verlinkungen dienen der Orientierung im Ratgeber-Cluster und ersetzen keine Diagnose.</p>\n'
        f"        </section>\n"
    )


def process_file(path: Path) -> bool:
    if path.name.startswith("_"):
        return False
    text = path.read_text(encoding="utf-8")
    if MARKER in text:
        return False
    n = count_artikel_links(text)
    if n >= 10:
        return False
    target_total = 12
    need = max(0, target_total - n)
    if need <= 0:
        return False
    current_slug = path.name
    have = existing_slugs(text)
    candidates = interleave_candidates(current_slug, have)
    chosen = candidates[:need]
    if not chosen:
        return False
    section = build_section(chosen)
    if "</article>" not in text:
        return False
    text = text.replace("</article>", section + "    </article>", 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed = []
    for path in sorted(ARTIKEL.glob("*.html")):
        if process_file(path):
            changed.append(path.name)
    print(f"Updated {len(changed)} files:")
    for name in changed:
        print(" ", name)


if __name__ == "__main__":
    main()
