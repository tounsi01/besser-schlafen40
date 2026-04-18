"""
Apply CTR-optimized <title> and meta description to artikel/*.html
Rules: title < 60 chars, meta description < 155 chars (visible intent).
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIKEL = ROOT / "artikel"

# filename -> (title, description) — lengths verified in assert block at end
SEO: dict[str, tuple[str, str]] = {
    "angst-nachts-wach-ab-40.html": (
        "Angst nachts wach? So beruhigst du Körper und Kopf",
        "Herzrasen um 3 Uhr, Panik im Dunkeln: Ursachen verstehen und kleine Schritte, die wirklich helfen – ohne Vorwürfe, mit Hoffnung.",
    ),
    "angststoerung-schlafprobleme-hilfe.html": (
        "Angst & Schlaf: Wann Therapie helfen kann",
        "Wenn die Nacht zur Falle wird: Anzeichen erkennen, Therapie-Optionen, nächste Schritte. Klar, ruhig, ohne Scham.",
    ),
    "besser-schlafen-ohne-medikamente-ab-40.html": (
        "Ohne Pillen besser schlafen: Stufenplan ab 40",
        "Kein Verzichts-Kult: erst Licht und Rhythmus, dann feine Tuning-Schritte. So gewinnst du Nächte zurück, ohne sofort an Medikamente zu denken.",
    ),
    "besser-schlafen-tipps.html": (
        "7 Schlaf-Tipps, die du heute noch testen kannst",
        "Keine endlosen Listen: zwei Hebel reichen oft. Kurz, prioritisiert, mit spürbarem Nutzen für deinen Abend und Morgen.",
    ),
    "cortisol-nachts-wach-ab-40.html": (
        "Cortisol hält dich nachts wach? So brichst du den Kreislauf",
        "Hochgefahren um 3 Uhr, tagsüber platt: Rhythmus und Stress verstehen, konkrete Schritte für ruhigere Nächte ab 40.",
    ),
    "cortisol-schlafen-problem.html": (
        "Cortisol & Schlaf: warum Abends noch „Büro-Modus“ an ist",
        "Tageskurve verstehen: Licht, Koffein, Stress. Neugier statt Panik – plus Ideen, die den Abend wieder weicher machen.",
    ),
    "depression-schlafprobleme-warnzeichen.html": (
        "Depression & Schlaf: 7 Warnzeichen ernst nehmen",
        "Schlaf bricht zusammen, Stimmung sinkt: wann es mehr als Stress ist und Hilfe der nächste kluge Schritt ist.",
    ),
    "durchschlafen-ab-40-tipps.html": (
        "Durchschlafen ab 40: ohne Bett-Stress, mit Rhythmus",
        "Fragmentierte Nächte? Rhythmus, Licht und kleine Grenzen bringen oft mehr als neue Gadgets. Praktisch und machbar.",
    ),
    "durchschlafen-probleme.html": (
        "Durchschlafen: Zyklus-Rätsel – und wie du es löst",
        "Mikroaufwachen, REM, Tiefschlaf: einmal ehrlich erklärt – damit du weniger kämpfst und klügere nächste Schritte wählst.",
    ),
    "einschlafen-dauert-lange.html": (
        "Einschlafen dauert ewig? So kommst du schneller zur Ruhe",
        "Grübeln, Koffein, Druck „sofort pennen“: die häufigsten Bremsen – und was heute Abend wirklich hilft, ohne Perfektion.",
    ),
    "frueh-aufwachen-ab-40-ursachen.html": (
        "Zu früh wach – und müde? Ursachen jenseits vom „Alter“",
        "Licht, Hormone, Stimmung, Schlafapnoe: was oft übersehen wird und welche Klärung sich wirklich lohnt.",
    ),
    "gedanken-kreisen-nachts-ab-40.html": (
        "Gedankenkreiseln nachts stoppen – ohne „einfach abschalten“",
        "Der Kopf spinnt um 2 Uhr weiter: sanfte Brüche, klare Mini-Schritte und weniger Selbst-Vorwürfe bis zum Einschlafen.",
    ),
    "hausmittel-schlafprobleme-sanfte-methoden.html": (
        "9 Hausmittel für den Schlaf – sanft, ohne Esoterik-Zwang",
        "Tee, Wärme, Routine: was sich gut anfühlt und was nur Zeit kostet. Ehrlich sortiert für ruhigere Nächte.",
    ),
    "hormone-schlafstoerung.html": (
        "Hormone & Schlaf – Mini-Lexikon ohne Fachchinesisch",
        "Östrogen, Cortisol, Schilddrüse in einem Satz erklärt: endlich Kontext fürs Gespräch mit Arzt oder Ärztin.",
    ),
    "hormonelle-schlafprobleme-ab-40.html": (
        "Hormone zerlegen deinen Schlaf? So fängst du wieder an",
        "Muster statt Panik: typische Symptome, realistische Hebel, wann Abklärung Sinn macht – verständlich für den Alltag.",
    ),
    "jede-nacht-wach-ab-40.html": (
        "Jede Nacht wach – wann es Muster statt „Pech“ ist",
        "Chronisch kaputt trotz Bett? Ursachen sortieren, Hoffnung zurückholen, erste Schritte, die nicht überfordern.",
    ),
    "job-stress-schlafen-ab-40.html": (
        "Job-Stress frisst deinen Schlaf? Grenzen ohne Drama setzen",
        "Kopf arbeitet nach Feierabend weiter: erkennbar, änderbar. Kleine Hebel für echte Erholung statt nur Überstehen.",
    ),
    "jobstress-schlafprobleme-ab-40.html": (
        "Jobstress & Schlaf: wenn der Alarm im Körper nicht ausgeht",
        "Deadline im Nacken, Nacht zum Grübeln: was wirklich passiert und wie du den ersten Hebel ziehst – ohne sofort kündigen zu müssen.",
    ),
    "magnesium-abends-schlafprobleme-timing.html": (
        "Magnesium abends: wann es hilft – und wann Timing nervt",
        "Zu früh, zu spät, zu viel? Typische Fehler und ein einfacher Plan, damit die Kapsel nicht gegen dich arbeitet.",
    ),
    "magnesium-bei-schlafproblemen-wirkung-dosierung.html": (
        "Magnesium für den Schlaf: was realistisch drinsteckt",
        "Formen, Dosis, Erwartung: ohne Marketing-Rausch. Ob es sich für dich lohnt – nüchtern und freundlich erklärt.",
    ),
    "magnesium-nachts-aufwachen-ab-40.html": (
        "Magnesium bei nächtlichem Aufwachen – Hoffnung oder Hype?",
        "Wann es passt, wann nicht: Muster zuerst, dann Mineralstoff. Weniger Geld verbrennen, mehr Klarheit für die Nacht.",
    ),
    "magnesium-naechtliches-aufwachen.html": (
        "Nachts aufwachen: erst Muster, dann Magnesium überlegen",
        "Hitze, Krampf, Grübeln – der erste Hebel ist selten die Dose. Entscheidungshilfe, die dir Zeit und Nerven spart.",
    ),
    "magnesium-oder-melatonin-schlafprobleme.html": (
        "Magnesium oder Melatonin? Die ehrliche Entscheidungshilfe",
        "Zwei Namen, zwei Logiken: wofür welches Mittel Sinn hat – ohne Apotheken-Stress und ohne Google-Angst.",
    ),
    "magnesium-schlafen.html": (
        "Magnesiummangel & Schlaf: Zeichen statt Dr-Google",
        "Krämpfe, Unruhe, schlechte Nächte: wann Labor und Arzt statt Kapseln die klügere erste Idee sind.",
    ),
    "magnesium-wirkung-schlaf.html": (
        "Magnesium & Schlaf: was Studien wirklich sagen",
        "Keine Wunderversprechen: Evidenz in Menschensprache – damit du Erwartungen und Geldbeutel schützt.",
    ),
    "melatonin-schlafen.html": (
        "Melatonin in Deutschland: was geht – und was riskant ist",
        "Rezept, Qualität, keine dubiosen Importe: rechtlich sauber schlafen wollen geht – so gehst du’s mit Ruhe an.",
    ),
    "melatonin-weniger-ab-40-schlaf.html": (
        "Weniger Melatonin ab 40? Licht, Alter & was du tun kannst",
        "Innere Uhr tickt anders: neugierig statt erschrocken – mit Schritten, die den Abend wieder freundlicher machen.",
    ),
    "muede-aber-kann-nicht-schlafen-ab-40.html": (
        "Müde, aber wach („tired but wired“) – so löst du den Knoten",
        "Der Körper will Ruhe, das System ist auf Hochtouren: Ursache grob verstehen und heute Abend einen Gang runter.",
    ),
    "nachts-aufwachen-nicht-wieder-einschlafen-ab-40.html": (
        "Wach und liegst wach? So brichst du die Grübel-Schleife",
        "Stimuluskontrolle, Licht, Stress: was wirklich hilft, wenn die Uhr quält und der Kopf nicht stoppt.",
    ),
    "nachts-unruhig-schlafen-ab-40.html": (
        "Nachts unruhig: Beine, Kopf – erste Orientierung",
        "Zappeln, Wenden, Wachsein: wann Alltag reicht und wann ein Arzttermin Gold wert ist. Klar und ohne Panik.",
    ),
    "nachts-unruhig-schlafen.html": (
        "Unruhige Beine (RLS)? Wenn der Schlaf zur Qual wird",
        "Bewegungsdrang abends: Anzeichen erkennen, Stress abgrenzen, wann Diagnose und Hilfe Sinn ergeben.",
    ),
    "nahrungsergaenzung-schlafprobleme-ab-40.html": (
        "Nahrungsergänzung & Schlaf: Lohn vs. Leerläufe",
        "Vor dem vollen Schrank: Prioritäten statt Shopping. Weniger Geld verbrennen, mehr erholsame Nächte anpeilen.",
    ),
    "natuerliche-abendroutine-gegen-schlafprobleme.html": (
        "Abendroutine in 60 Minuten – ohne Wellness-Theater",
        "Sanft runterfahren: Licht, Bewegung, klare Stopps. Spürbarer Schlaf ohne 20 neue Regeln.",
    ),
    "natuerliche-schlafmittel-ab-40.html": (
        "Natürliche Schlafmittel ab 40: Evidenz & Vernunft",
        "Kräuter, Tee, Routinen: was realistisch hilft und was nur beruhigt die Geldbörse, nicht den Kopf.",
    ),
    "nervensystem-beruhigen-schlafen.html": (
        "Nervensystem runter: Atem, Vagus, weniger Spannung",
        "Körperlich abschalten vor Mitternacht: einfache Trigger, die sich nicht nach Leistungssport anfühlen.",
    ),
    "schlafprobleme-beheben-ohne-medikamente.html": (
        "Schlaf reparieren ohne Medis – 14 Tage, die nicht nerven",
        "Kleine Gewohnheiten statt Heldentum: Plan mit Luft zum Atmen und echtem Chancen-Gefühl.",
    ),
    "schlafprobleme-frauen-ab-40.html": (
        "Schlafprobleme als Frau ab 40 – Hormone, Last, Lösungen",
        "Wechseljahre, Job, Familie: du bist nicht „nur müde“. Einordnung mit Würde und nächsten sinnvollen Schritten.",
    ),
    "schlafprobleme-hormonell-checkliste.html": (
        "Hormonell schlecht geschlafen? Checkliste zum Abhaken",
        "Symptome sortieren, Arztgespräch vorbereiten, weniger Druck im Kopf – eine Seite, die Struktur schenkt.",
    ),
    "schlafprobleme-maenner-ab-40-hormone.html": (
        "Schlaf & Hormone bei Männern ab 40 – kein Tabu, nur Fakten",
        "Testosteron, Stress, Schnarchen: wann es mehr als „älter werden“ ist und was du realistisch prüfen kannst.",
    ),
    "schlafprobleme-stress-strategien.html": (
        "Stress frisst deinen Schlaf? 7 Strategien, die wirken",
        "Hyperarousal greifbar machen: konkrete Übungen statt leerer Tipps – für Nächte, in denen du wieder landest.",
    ),
    "schlafprobleme-vor-periode-ab-40.html": (
        "Schlaf vor der Periode mies? PMS, Hormone, was hilft",
        "Gereizt, aufgedreht, wach: Zyklus nicht ignorieren. Sanfte Hilfen und wann ärztliche Klärung Sinn macht.",
    ),
    "schlafprobleme-wechseljahre-tipps.html": (
        "Wechseljahre & Schlaf: Checkliste für kühlere Nächte",
        "Hitze, Schweiß, Licht: schnell umsetzbare Punkte plus Orientierung, was der lange Ratgeber vertieft.",
    ),
    "schlafprobleme-wechseljahre-ursachen-hilfe.html": (
        "Schlaf in den Wechseljahren: Ursachen & echte Hilfe",
        "Hormone, Hitzewallungen, innere Unruhe: verständlich erklärt, mit Wegen, die sich nicht nach Kampf anfühlen.",
    ),
    "schlafqualitaet-verbessern.html": (
        "Schlafqualität messen – ohne Tracker-Zwang und Stress",
        "Subjektiv ehrlich: Tagebuch, Gefühl, wann Zahlen helfen und wann sie nur nerven. Mehr Klarheit, weniger Druck.",
    ),
    "schlafstoerung-stress-arbeit.html": (
        "Job frisst deinen Schlaf? So setzt du Grenzen",
        "Meeting im Kopf um 23 Uhr? Erkennen, benennen, erste Schritte. Erholung statt Dauerfeuer – realistisch für Jobs.",
    ),
    "schlafstoerungen-ab-40.html": (
        "Schlafstörungen ab 40: Hub – Ursachen, Tipps & 20 Ratgeber",
        "Zentraler Ratgeber ab 40: Einschlafen, Hormone, Stress, Magnesium. Fünf Themen mit Kurzfassung und 20 Spezial-Artikeln – strukturiert für ruhigere Nächte.",
    ),
    "schlecht-schlafen-stress.html": (
        "Stress & schlechter Schlaf: So brichst du den Kreis",
        "Hochgefahren und erschöpft zugleich: was im Körper passiert und welche nächsten Schritte Erleichterung bringen.",
    ),
    "schlechter-schlaf-ab-40-ursachen.html": (
        "Schlechter Schlaf ab 40: Ursachen finden statt raten",
        "Vom Schnarchen bis zur Stimmung: Filter für das, was häufig übersehen wird – damit du die richtige Hilfe triffst.",
    ),
    "schlechter-schlaf-wechseljahre-ursachen.html": (
        "Wechseljahre & Schlaf: Was wirklich dran ist?",
        "Hitzewallungen ja – aber nicht alles der Menopause zuschreiben. Klüger zuordnen, besser schlafen, weniger Sorgen.",
    ),
    "stress-abbauen-schlafen.html": (
        "Stress senken für Schlaf: 3 Kalender-Tricks",
        "Weniger Last tagsüber, mehr Ruhe nachts: Grenzen, Pausen, Kommunikation ohne großes Wellness-Programm.",
    ),
    "stress-schlafprobleme-trotz-muedigkeit.html": (
        "Müde, aber kein Schlaf? Warum der Körper nicht landet",
        "Trotz Erschöpfung wach: Stress, Hormone, Gewohnheiten – und was du heute probieren kannst, ohne dich zu zwingen.",
    ),
    "stressbedingte-schlafprobleme-ab-40.html": (
        "Stress-Schlaf & Hyperarousal: Was dahinter steckt",
        "Innerer Alarm bleibt an: erklärt in Alltagssprache, mit Wegen raus aus der permanenten Bereitschaft.",
    ),
    "tiefer-schlaf-verbessern.html": (
        "Tiefschlaf boosten? Was wirklich hilft (ohne Gadget-Zwang)",
        "Alkohol, Apnoe, Rhythmus: indirekt Tiefschlaf schützen statt Marketing versprechen. Ehrlich und erleichternd.",
    ),
    "unruhiger-schlaf-ursachen.html": (
        "Unruhig geschlafen? Medizin, Gewohnheit oder Psyche zuerst?",
        "Schneller Entscheidungsbaum: weniger Rätselraten, klarere nächste Schritte – ohne Dr. Selbstdiagnose.",
    ),
    "vollmond-schlafprobleme-mythos-oder-effekt.html": (
        "Vollmond & Schlaf: Mythos oder echter Effekt?",
        "Nebel, Licht, Erwartung: warum du nachts spürbar schlechter liegst – oft ohne Hexerei. Beruhigend erklärt.",
    ),
    "warum-wache-ich-nachts-auf-ab-40.html": (
        "Warum du nachts aufwachst (und wie du es entschärft)",
        "Zwischen 2 und 5 Uhr wach: typische Auslöser, klare erste Hilfen – weniger Grübeln, mehr Plan für die Nacht.",
    ),
    "warum-wache-ich-nachts-auf.html": (
        "2–4 Uhr wach: warum genau dieses Fenster so nervt",
        "Cortisol, Hitze, leichter Schlaf: Muster erkennen statt Uhr starren. Hoffnung + konkrete Mini-Schritte.",
    ),
    "was-tun-bei-schlafproblemen-leitfaden.html": (
        "Schlafprobleme? Der Leitfaden, der nicht überlädt",
        "Schritt für Schritt: was zuerst, was später, wann Arzt. Weniger Chaos im Kopf, mehr Kontrolle fürs Bett.",
    ),
    "wechseljahre-naechtliches-aufwachen-hilfe.html": (
        "Wechseljahre: nachts nass wach – Hilfe, die tröstet",
        "Hitzewallungen, Schweiß, gebrochener Schlaf: Ursachen und Tipps, die sich nicht nach Kampf anfühlen.",
    ),
    "welches-magnesium-fuer-schlaf-ab-40.html": (
        "Welches Magnesium fürs Schlafen? Formen ohne Marketing-Lärm",
        "Citrat, Bisglycinat, Verträglichkeit: die Kaufentscheidung wird einfacher – und dein Magen dankt’s.",
    ),
    "welches-magnesium-zum-schlafen.html": (
        "Magnesium & empfindlicher Magen: welche Form abends passt",
        "Kein Durchfall statt Entspannung: Citrat, Oxid, Chelat verständlich – damit die Nacht nicht auf der Toilette endet.",
    ),
    "_vorlage-requete-seo.html": (
        "Dein Thema: Schlaf-Titel unter 60 Zeichen",
        "Platzhalter: emotionale Meta unter 155 Zeichen mit Nutzen und Neugier – Text im Artikel ersetzen vor Veröffentlichung.",
    ),
}


def escape_title(s: str) -> str:
    return s.replace("&", "&amp;")


def escape_desc(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;")


def replace_title(html: str, new: str) -> str:
    new_e = escape_title(new)
    return re.sub(r"<title>\s*.*?\s*</title>", f"<title>{new_e}</title>", html, count=1, flags=re.DOTALL)


def replace_meta_description(html: str, new: str) -> str:
    new_e = escape_desc(new)
    # Multiline: <meta\n name="description"\n content="..."\n />
    html = re.sub(
        r'<meta\s*\n\s*name="description"\s*\n\s*content="[^"]*"\s*\n\s*/>',
        f'<meta name="description" content="{new_e}" />',
        html,
        count=1,
    )
    if f'content="{new_e}"' not in html:
        html = re.sub(
            r'<meta\s+name="description"\s+content="[^"]*"\s*/>',
            f'<meta name="description" content="{new_e}" />',
            html,
            count=1,
        )
    return html


def validate() -> None:
    for name, (title, desc) in SEO.items():
        assert len(title) < 60, f"{name} title {len(title)}: {title!r}"
        assert len(desc) < 155, f"{name} desc {len(desc)}: {desc!r}"


def main() -> None:
    validate()
    for name, (title, desc) in SEO.items():
        path = ARTIKEL / name
        if not path.exists():
            print("SKIP missing", name)
            continue
        text = path.read_text(encoding="utf-8")
        text2 = replace_title(text, title)
        text2 = replace_meta_description(text2, desc)
        if text2 != text:
            path.write_text(text2, encoding="utf-8")
            print("OK", name)
        else:
            print("NOCHANGE", name)


if __name__ == "__main__":
    main()
