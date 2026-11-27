/* Page unique : refermer le menu mobile apres le choix d'une section */
(function () {
  "use strict";
  var nav = document.getElementById("nav");
  var btn = document.querySelector(".menu-btn");
  if (!nav || !btn) return;
  nav.addEventListener("click", function (e) {
    if (!e.target.closest("a")) return;
    nav.classList.remove("open");
    btn.setAttribute("aria-expanded", "false");
  });
})();

/* Poussins : ils gravissent la colline avec le defilement et s'arretent avec lui */
(function () {
  "use strict";
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var passages = document.querySelectorAll(".passage");
  var attente = false;

  function marcher() {
    attente = false;
    var haut = window.innerHeight;
    Array.prototype.forEach.call(passages, function (p) {
      var y = p.getBoundingClientRect().top;
      if (y < 0 || y > haut + 90) return;
      var bande = p.querySelector(".bande");
      var trace = p.querySelector(".trace");
      var colline = parseFloat(window.getComputedStyle(p).getPropertyValue("--colline")) || 0;
      var large = p.clientWidth;
      var long = bande.offsetWidth;
      var retour = p.classList.contains("retour");
      var avance = Math.min(1, Math.max(0, (haut - y) / (haut - 76)));
      if (retour) avance = 1 - avance;
      var x = avance * (large + long) - long;
      bande.style.left = "0";
      bande.style.bottom = "0";
      bande.style.transform = "translateX(" + x + "px)";
      var bord = bande.getBoundingClientRect().left;
      Array.prototype.forEach.call(bande.children, function (poussin, i) {
        /* Les SVG n'ont pas offsetLeft : on mesure leur boite a l'ecran */
        var boite = poussin.getBoundingClientRect();
        var u = Math.min(1, Math.max(0, (x + boite.left - bord + boite.width / 2) / large));
        var sol = colline * 4 * u * (1 - u);
        var pente = Math.atan(colline * 4 * (1 - 2 * u) / large) * 180 / Math.PI;
        var saut = 7 * Math.abs(Math.sin(x / 22 + i * 1.3));
        poussin.style.translate = "0 " + (2 - sol - saut) + "px";
        poussin.style.rotate = (-pente) + "deg";
      });
      if (trace) {
        /* La trace n'apparait que derriere les poussins */
        trace.style.clipPath = retour
          ? "inset(-10px 0 -10px " + Math.max(0, x + long) + "px)"
          : "inset(-10px " + Math.max(0, large - x) + "px -10px 0)";
      }
    });
  }

  function demander() {
    if (attente) return;
    attente = true;
    window.requestAnimationFrame(marcher);
  }

  window.addEventListener("scroll", demander, { passive: true });
  window.addEventListener("resize", demander);
  window.addEventListener("load", demander);
  demander();
})();

/* Titre lettre par lettre, puis apparitions au defilement */
(function () {
  "use strict";
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;

  var titre = document.querySelector(".ouverture h1");

  function decouper() {
    var texte = titre.textContent.trim();
    var rang = 0;
    titre.setAttribute("aria-label", texte);
    titre.textContent = "";
    texte.split(/\s+/).forEach(function (mot, i) {
      if (i) titre.appendChild(document.createTextNode(" "));
      var boite = document.createElement("span");
      boite.className = "mot";
      boite.setAttribute("aria-hidden", "true");
      Array.from(mot).forEach(function (signe) {
        var lettre = document.createElement("span");
        lettre.className = "lettre";
        lettre.style.setProperty("--i", rang++);
        lettre.textContent = signe;
        boite.appendChild(lettre);
      });
      titre.appendChild(boite);
    });
  }

  if (titre) {
    decouper();
    /* main.js peut reecrire le titre avec le texte a jour : on le redecoupe */
    new MutationObserver(function () {
      if (!titre.querySelector(".lettre")) decouper();
    }).observe(titre, { childList: true });
  }

  if (!("IntersectionObserver" in window)) return;
  document.documentElement.classList.add("anime");
  var veille = new IntersectionObserver(function (entrees) {
    entrees.forEach(function (e) {
      if (!e.isIntersecting) return;
      e.target.classList.add("vu");
      veille.unobserve(e.target);
    });
  }, { threshold: 0.2 });
  Array.prototype.forEach.call(document.querySelectorAll("[data-reveal]"), function (el) { veille.observe(el); });
})();
