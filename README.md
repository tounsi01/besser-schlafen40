# SchlafGut 40+ - Projektstruktur

## Seitenstruktur

- `/` - Homepage mit Positionierung, CTA, FAQ, Affiliate-Teaser
- `/blog/` - Blog-Uebersicht mit internen Links
- `/blog/artikel-template.html` - Wiederverwendbares SEO-Artikel-Template
- `/artikel/schlafstoerungen-ab-40.html` - Leitartikel mit Conversion-Elementen
- `/quiz/` - Quiz-Landingpage mit Ergebnislogik

## Technische Dateien

- `/styles.css` - globales, leichtgewichtiges Designsystem
- `/script.js` - Quiz-Interaktion
- `/robots.txt` - Crawling-Freigabe + Sitemap-Hinweis
- `/sitemap.xml` - URL-Verzeichnis fuer Suchmaschinen

## Affiliate- und SEO-Elemente

- Affiliate-Boxen auf Homepage und Leitartikel
- `rel="sponsored nofollow"` fuer Affiliate-Links
- Meta-Title, Description, Canonical auf allen Hauptseiten
- Strukturierte Daten auf Homepage (WebSite) und Leitartikel (Article)
- FAQ-Sektionen fuer Long-Tail-Keywords
- Interne Verlinkung zwischen Homepage, Blog, Artikel und Quiz
