/* =============================================================================
   Pour Faire Simple. — JavaScript vanilla, sans dépendance.
   Modules : header, menu mobile, transitions de page, révélations au scroll,
   compteurs, grille de réalisations (filtres, preview, curseur, modale),
   lecteur vidéo à la demande, formulaire de qualification.
   ========================================================================== */
(function () {
  "use strict";

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const finePointer = window.matchMedia("(pointer: fine)").matches;
  const $ = (sel, ctx) => (ctx || document).querySelector(sel);
  const $$ = (sel, ctx) => Array.from((ctx || document).querySelectorAll(sel));

  /* ---------- Entrée de page ---------- */
  document.body.classList.add("is-entering");

  /* ---------- Header : état "scrolled" ---------- */
  const header = $(".site-header");
  if (header) {
    const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 24);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
  }

  /* ---------- Menu mobile ---------- */
  const burger = $(".burger");
  const menu = $("#menu");
  if (burger && menu) {
    const focusables = () => $$("a, button", menu);
    const setOpen = (open) => {
      burger.setAttribute("aria-expanded", String(open));
      burger.setAttribute("aria-label", open ? "Fermer le menu" : "Ouvrir le menu");
      menu.classList.toggle("is-open", open);
      document.body.classList.toggle("menu-open", open);
      if (open) { const f = focusables()[0]; if (f) f.focus(); } else { burger.focus(); }
    };
    burger.addEventListener("click", () => setOpen(burger.getAttribute("aria-expanded") !== "true"));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && menu.classList.contains("is-open")) setOpen(false);
      if (e.key === "Tab" && menu.classList.contains("is-open")) {
        const f = focusables(); const first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); burger.focus(); }
      }
    });
  }

  /* ---------- Transitions de page (fondu) ---------- */
  if (!reduceMotion) {
    document.addEventListener("click", (e) => {
      const a = e.target.closest("a[href]");
      if (!a || a.target === "_blank" || a.hasAttribute("download") || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      const url = new URL(a.href, location.href);
      if (url.origin !== location.origin || url.pathname === location.pathname || a.href.startsWith("mailto:") || a.href.startsWith("tel:") || url.hash && url.pathname === location.pathname) return;
      if (url.protocol !== "http:" && url.protocol !== "https:" && url.protocol !== "file:") return;
      e.preventDefault();
      document.body.classList.add("is-leaving");
      setTimeout(() => { location.href = a.href; }, 260);
    });
    window.addEventListener("pageshow", (e) => { if (e.persisted) document.body.classList.remove("is-leaving"); });
  }

  /* ---------- Révélations au scroll ---------- */
  const revealEls = $$(".reveal, .reveal--stagger");
  if (revealEls.length && "IntersectionObserver" in window && !reduceMotion) {
    const io = new IntersectionObserver((entries) => {
      entries.forEach((en) => { if (en.isIntersecting) { en.target.classList.add("is-visible"); io.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach((el) => io.observe(el));
  } else {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Compteurs ---------- */
  const counters = $$("[data-count]");
  if (counters.length) {
    const run = (el) => {
      const target = parseFloat(el.dataset.count);
      const suffix = el.dataset.suffix || "";
      const prefix = el.dataset.prefix || "";
      const dec = (el.dataset.count.split(".")[1] || "").length;
      const dur = 1400; const t0 = performance.now();
      const tick = (t) => {
        const p = Math.min(1, (t - t0) / dur); const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = prefix + (target * eased).toFixed(dec).replace(".", ",") + suffix;
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    };
    if ("IntersectionObserver" in window && !reduceMotion) {
      const io = new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) { run(en.target); io.unobserve(en.target); } });
      }, { threshold: 0.5 });
      counters.forEach((el) => io.observe(el));
    } else {
      counters.forEach((el) => { el.textContent = (el.dataset.prefix || "") + el.dataset.count.replace(".", ",") + (el.dataset.suffix || ""); });
    }
  }

  /* ---------- Vidéo hero : lecture seulement si visible ---------- */
  const heroVideo = $(".hero__media video");
  if (heroVideo) {
    if (reduceMotion) { heroVideo.removeAttribute("autoplay"); heroVideo.pause(); }
    else if ("IntersectionObserver" in window) {
      new IntersectionObserver((entries) => {
        entries.forEach((en) => { if (en.isIntersecting) heroVideo.play().catch(() => {}); else heroVideo.pause(); });
      }, { threshold: 0.1 }).observe(heroVideo);
    }
  }

  /* ---------- Grille de réalisations ---------- */
  const grid = $(".work-grid");
  if (grid) {
    const cards = $$(".work-card", grid);
    const chips = $$(".chip[data-filter]");
    const countEl = $(".filters__count");
    const empty = $(".work-empty");
    const state = { format: "all", secteur: "all" };

    const apply = () => {
      let shown = 0;
      cards.forEach((c) => {
        const okF = state.format === "all" || c.dataset.format === state.format;
        const okS = state.secteur === "all" || c.dataset.secteur === state.secteur;
        const ok = okF && okS; c.hidden = !ok; if (ok) shown++;
      });
      if (countEl) countEl.textContent = shown + (shown > 1 ? " réalisations" : " réalisation");
      if (empty) empty.classList.toggle("is-visible", shown === 0);
    };
    chips.forEach((chip) => {
      chip.addEventListener("click", () => {
        const group = chip.dataset.filter; const value = chip.dataset.value;
        state[group] = value;
        chips.filter((c) => c.dataset.filter === group).forEach((c) => c.setAttribute("aria-pressed", String(c === chip)));
        apply();
      });
    });
    // Filtre initial depuis l'URL (?format=motion-design)
    const params = new URLSearchParams(location.search);
    ["format", "secteur"].forEach((k) => {
      const v = params.get(k);
      const chip = v && chips.find((c) => c.dataset.filter === k && c.dataset.value === v);
      if (chip) chip.click();
    });
    apply();

    // Preview au survol / focus (classe pilotant l'animation CSS)
    cards.forEach((c) => {
      c.addEventListener("mouseenter", () => c.classList.add("is-playing"));
      c.addEventListener("mouseleave", () => c.classList.remove("is-playing"));
    });

    // Curseur personnalisé
    if (finePointer && !reduceMotion) {
      const cursor = document.createElement("div");
      cursor.className = "cursor"; cursor.setAttribute("aria-hidden", "true"); cursor.dataset.label = "Voir";
      document.body.appendChild(cursor);
      let x = 0, y = 0, cx = 0, cy = 0, raf = null;
      const loop = () => { cx += (x - cx) * 0.2; cy += (y - cy) * 0.2; cursor.style.transform = `translate(${cx}px, ${cy}px) translate(-50%, -50%)`; raf = requestAnimationFrame(loop); };
      grid.addEventListener("mouseenter", () => { cursor.classList.add("is-visible"); if (!raf) loop(); });
      grid.addEventListener("mouseleave", () => { cursor.classList.remove("is-visible", "is-active"); cancelAnimationFrame(raf); raf = null; });
      grid.addEventListener("mousemove", (e) => { x = e.clientX; y = e.clientY; const onCard = e.target.closest(".work-card"); cursor.classList.toggle("is-active", !!onCard); if (onCard) cursor.dataset.label = onCard.dataset.cursor || "Voir"; });
    }

    // Modale pour les fiches non encore rédigées
    const modal = $("#modal");
    if (modal) {
      const box = $(".modal__box", modal); let lastFocus = null;
      const close = () => { modal.classList.remove("is-open"); modal.setAttribute("aria-hidden", "true"); if (lastFocus) lastFocus.focus(); };
      const open = (btn) => {
        lastFocus = btn;
        $("#modal-title").textContent = btn.dataset.title || "";
        $("#modal-sub").textContent = btn.dataset.sub || "";
        const img = $("#modal-img"); img.src = btn.dataset.poster; img.alt = "Visuel de la réalisation " + (btn.dataset.title || "");
        modal.classList.add("is-open"); modal.setAttribute("aria-hidden", "false"); $(".modal__close", modal).focus();
      };
      $$("button.work-card", grid).forEach((b) => b.addEventListener("click", () => open(b)));
      $(".modal__close", modal).addEventListener("click", close);
      modal.addEventListener("click", (e) => { if (!box.contains(e.target)) close(); });
      document.addEventListener("keydown", (e) => { if (e.key === "Escape" && modal.classList.contains("is-open")) close(); });
    }
  }

  /* ---------- Lecteur vidéo à la demande (poster + chargement au clic) ---------- */
  $$(".player").forEach((player) => {
    const btn = $(".player__btn", player);
    if (!btn) return;
    btn.addEventListener("click", () => {
      const src = player.dataset.src; if (!src) return;
      const video = document.createElement("video");
      video.controls = true; video.autoplay = true; video.playsInline = true; video.setAttribute("aria-label", btn.getAttribute("aria-label") || "Lecture de la vidéo");
      if (player.dataset.poster) video.poster = player.dataset.poster;
      const s = document.createElement("source"); s.src = src; s.type = player.dataset.type || "video/webm"; video.appendChild(s);
      player.appendChild(video); player.classList.add("is-playing");
      video.play().catch(() => {});
    });
  });

  /* ---------- Formulaire de qualification ---------- */
  const form = $("#contact-form");
  if (form) {
    const status = $(".form__status", form);
    const success = $("#form-success");
    const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

    const setError = (field, msg) => {
      const wrap = field.closest(".field"); if (!wrap) return;
      const err = $(".field__error", wrap);
      wrap.classList.toggle("has-error", !!msg);
      if (err) err.textContent = msg || "";
      const invalidTarget = field.matches("fieldset") ? null : field;
      if (invalidTarget) invalidTarget.setAttribute("aria-invalid", msg ? "true" : "false");
    };

    const validate = () => {
      const errors = [];
      // Champs requis (input/select/textarea)
      $$("[required]", form).forEach((el) => {
        if (el.type === "checkbox") { if (!el.checked) { setError(el, "Cette case doit être cochée."); errors.push(el); } else setError(el, ""); return; }
        if (el.type === "radio") return;
        const v = el.value.trim();
        if (!v) { setError(el, "Ce champ est obligatoire."); errors.push(el); return; }
        if (el.type === "email" && !emailRe.test(v)) { setError(el, "Cette adresse email ne semble pas valide."); errors.push(el); return; }
        setError(el, "");
      });
      // Groupes radio requis
      $$("fieldset[data-required]", form).forEach((fs) => {
        const checked = $$("input[type=radio]:checked", fs).length > 0;
        setError(fs, checked ? "" : "Choisissez une option.");
        if (!checked) errors.push($("input", fs));
      });
      return errors;
    };

    $$("input, select, textarea", form).forEach((el) => {
      el.addEventListener("blur", () => { if (el.closest(".field")?.classList.contains("has-error")) validate(); });
      el.addEventListener("input", () => { const w = el.closest(".field"); if (w && w.classList.contains("has-error")) validate(); });
    });

    form.addEventListener("submit", (e) => {
      e.preventDefault();
      if ($(".honeypot input", form)?.value) return; // bot
      const errors = validate();
      if (errors.length) {
        status.textContent = errors.length + (errors.length > 1 ? " champs demandent votre attention." : " champ demande votre attention.");
        status.classList.add("is-error"); errors[0].focus();
        return;
      }
      status.classList.remove("is-error"); status.textContent = "";
      // Maquette : aucun envoi réseau. Récapitulatif affiché à l'écran.
      const data = new FormData(form);
      const recap = $("#form-recap");
      if (recap) {
        const rows = [["Projet", data.get("type")], ["Format", data.getAll("format").join(", ")], ["Échéance", data.get("echeance")], ["Budget", data.get("budget")], ["Diffusion", data.getAll("diffusion").join(", ")]].filter((r) => r[1]);
        recap.innerHTML = rows.map((r) => `<li><strong>${r[0]}</strong> : ${String(r[1]).replace(/</g, "&lt;")}</li>`).join("");
      }
      form.classList.add("is-sent"); success.classList.add("is-visible"); success.focus();
      success.scrollIntoView({ behavior: reduceMotion ? "auto" : "smooth", block: "start" });
    });

    // Bascule "vous êtes une agence" (?profil=agence)
    const profil = new URLSearchParams(location.search).get("profil");
    if (profil === "agence") { const r = $("input[name=type][value='Agence : production en marque blanche']", form); if (r) r.checked = true; }
  }
})();
