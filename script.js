document.querySelectorAll(".quiz").forEach((quizEl) => {
  const steps = [...quizEl.querySelectorAll(".quiz-step")];
  const resultBox = quizEl.querySelector(".result");
  let current = 0;
  let score = 0;
  const answers = [];

  const recommendationMap = [
    {
      title: "Nächtliches Aufwachen",
      byPoints: {
        2: "Stabilisiere den Schlaf mit einer gleichbleibenden Zubettgehzeit und reduziere Flüssigkeit 90 Minuten vor dem Schlafen.",
        3: "Priorisiere ein ergonomisches Kissen und konsequente Abdunkelung, um nächtliche Unterbrechungen zu reduzieren.",
      },
    },
    {
      title: "Morgendliche Erholung",
      byPoints: {
        2: "Erhöhe die Schlafqualität mit einer ruhigen Abendroutine und einer Schlafmaske bei Restlicht.",
        3: "Setze auf einen strukturierten Abendablauf mit Entspannungsaudio, damit dein Nervensystem vor dem Schlafen besser herunterfährt.",
      },
    },
    {
      title: "Abendlicher Stress",
      byPoints: {
        1: "Plane 20 Minuten digitale Auszeit ein, um den Stresspegel vor dem Einschlafen spürbar zu senken.",
        2: "Nutze täglich ein kurzes Atem- oder Audio-Programm am Abend, um innere Unruhe gezielt zu reduzieren.",
      },
    },
    {
      title: "Abendroutine",
      byPoints: {
        1: "Mache deine Abendroutine verbindlicher: gleiche Uhrzeit, Licht runter, kurze Entspannungsphase.",
        2: "Beginne mit einer einfachen 3-Schritte-Routine (Licht reduzieren, Reize minimieren, Entspannung), damit dein Schlafsignal klarer wird.",
      },
    },
  ];

  const showStep = (idx) => {
    steps.forEach((s, i) => s.classList.toggle("active", i === idx));
  };

  quizEl.addEventListener("click", (e) => {
    const target = e.target;
    if (!(target instanceof HTMLElement)) return;

    if (target.matches("[data-points]")) {
      const points = Number(target.dataset.points || 0);
      score += points;
      answers.push({
        stepIndex: current,
        points,
      });
      current += 1;

      if (current < steps.length) {
        showStep(current);
        return;
      }

      let level = "Leicht";
      let resultTitle = "Dein persönliches Schlafprofil: Gute Basis, mit Potenzial";
      let diagnosis =
        "Es zeigen sich leichte Hinweise auf einen noch nicht vollständig stabilen Schlafrhythmus.";
      let baseRecommendation =
        "Stärke deine Abendroutine mit kleinen, konstanten Schritten und beobachte die Entwicklung über 10 bis 14 Tage.";
      let link = "/artikel/schlafstoerungen-ab-40.html";

      if (score >= 8) {
        level = "Deutlich";
        resultTitle =
          "Dein persönliches Schlafprofil: Deutliche Schlafbelastung";
        diagnosis =
          "Deine Antworten sprechen für eine aktuell deutlich belastete Schlafqualität, vor allem durch Unterbrechungen und fehlende Regeneration.";
        baseRecommendation =
          "Setze auf eine Kombination aus Schlafumgebung, fester Abendstruktur und gezielter Entspannung.";
        link = "/artikel/schlafstoerungen-ab-40.html#empfehlungen";
      } else if (score >= 4) {
        level = "Mittel";
        resultTitle =
          "Dein persönliches Schlafprofil: Mittlere Schlafbelastung";
        diagnosis =
          "Es gibt mehrere Signale für einen unruhigen Schlaf, der deine Erholung am Morgen bereits beeinträchtigt.";
        baseRecommendation =
          "Optimiere Abendroutine, Lichtreduktion und Entspannung, um wieder mehr Schlafkontinuität zu erreichen.";
      }

      const personalizedRecommendations = answers
        .map((answer) => {
          const config = recommendationMap[answer.stepIndex];
          if (!config) return null;
          const recommendation = config.byPoints[answer.points];
          if (!recommendation) return null;
          return `<li><strong>${config.title}:</strong> ${recommendation}</li>`;
        })
        .filter(Boolean);

      if (personalizedRecommendations.length === 0) {
        personalizedRecommendations.push(
          `<li><strong>Nächster Schritt:</strong> ${baseRecommendation}</li>`
        );
      } else {
        personalizedRecommendations.unshift(
          `<li><strong>Priorität:</strong> ${baseRecommendation}</li>`
        );
      }

      resultBox.innerHTML = `
        <h3>${resultTitle}</h3>
        <p class="quiz-diagnosis"><strong>Kurze Einordnung:</strong> Schlafprobleme ${level}. ${diagnosis}</p>
        <figure class="quiz-result-media">
          <img
            src="https://images.pexels.com/photos/3771115/pexels-photo-3771115.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=960"
            srcset="
              https://images.pexels.com/photos/3771115/pexels-photo-3771115.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=480 480w,
              https://images.pexels.com/photos/3771115/pexels-photo-3771115.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=960 960w
            "
            sizes="(max-width: 920px) 100vw, 44rem"
            alt="Ruhige Abendatmosphaere fuer besseren Schlaf ab 40"
            loading="lazy"
            decoding="async"
            width="960"
            height="640"
          />
        </figure>
        <section class="quiz-result-neowake" aria-labelledby="quiz-neowake-heading">
          <span class="quiz-result-neowake__badge">Top Empfehlung 40+</span>
          <h4 id="quiz-neowake-heading" class="quiz-result-neowake__title">
            Basierend auf Ihren Antworten empfehlen wir
          </h4>
          <div class="quiz-result-neowake__highlight">Neowake Schlafprogramm</div>
          <p class="quiz-result-neowake__audio-brand">
            Geführte Audio-Entspannung für eine ruhigere Abendroutine
          </p>
          <p class="quiz-result-neowake__desc">
            Natürliches Schlafprogramm ohne Medikamente
          </p>
          <p class="quiz-result-neowake__text">
            Viele Leser berichten von schnellerem Einschlafen und tieferem Schlaf
          </p>
          <figure class="quiz-result-neowake__media">
            <img
              src="https://images.pexels.com/photos/6787202/pexels-photo-6787202.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=960"
              srcset="
                https://images.pexels.com/photos/6787202/pexels-photo-6787202.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=480 480w,
                https://images.pexels.com/photos/6787202/pexels-photo-6787202.jpeg?auto=compress&cs=tinysrgb&fm=webp&w=960 960w
              "
              sizes="(max-width: 920px) 100vw, 44rem"
              alt="Ruhige Schlafatmosphaere fuer erholsamen Schlaf ab 40"
              loading="lazy"
              decoding="async"
              width="960"
              height="640"
            />
          </figure>
          <p class="quiz-result-neowake__cta">
            <a
              class="button"
              href="https://neowake.de/jetzt-testen#aff=Amouna"
              rel="sponsored nofollow"
              >Jetzt besser schlafen mit Neowake</a
            >
          </p>
        </section>
        <ul class="quiz-recommendations">${personalizedRecommendations.join("")}</ul>
        <p class="quiz-result-actions">
          <a class="button" href="${link}">Passende Ratgeber-Tipps lesen</a>
          <a class="button alt" href="/#vergleich">Produkte vergleichen</a>
        </p>
        <p class="quiz-reassurance">Hinweis: Diese Auswertung dient deiner Orientierung und ersetzt keine medizinische Diagnose. Viele Schlafprobleme lassen sich mit passenden Gewohnheiten und der richtigen Unterstützung spürbar verbessern.</p>
      `;
      resultBox.hidden = false;
      steps.forEach((s) => s.classList.remove("active"));
    }
  });

  if (steps.length) showStep(0);
});
