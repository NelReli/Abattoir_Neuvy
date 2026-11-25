/* Abattoir de Neuvy - menu, valeurs partagees (config.json), textes (content.json), formulaire de contact */
(function () {
  "use strict";

  var JOURS = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"];
  var MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"];

  /* ---------- Formats ---------- */
  function hh(t) { // "06:00" -> "6 h 00"
    var p = t.split(":");
    return parseInt(p[0], 10) + " h " + p[1];
  }
  function joursTexte(j) {
    var s = j.slice().sort(function (a, b) { return ((a + 6) % 7) - ((b + 6) % 7); }); // lundi en premier
    var contigu = s.every(function (v, i) { return i === 0 || ((v + 6) % 7) === ((s[i - 1] + 6) % 7) + 1; });
    if (s.length > 2 && contigu) return "du " + JOURS[s[0]] + " au " + JOURS[s[s.length - 1]];
    if (s.length === 1) return "le " + JOURS[s[0]];
    return "les " + s.slice(0, -1).map(function (d) { return JOURS[d]; }).join(", ") + " et " + JOURS[s[s.length - 1]];
  }
  function fermetureTexte(f) {
    var d1 = f.jour_debut === 1 ? "1er" : String(f.jour_debut);
    return "du " + d1 + " au " + f.jour_fin + " " + MOIS[f.mois - 1];
  }
  function telLien(t) { return "tel:+33" + t.replace(/\s/g, "").replace(/^0/, ""); }

  function valeurs(c) {
    var a = c.abattage;
    return {
      tel: c.telephone,
      adresse: c.adresse,
      email: c.email_contact,
      jours: joursTexte(a.jours),
      depot: "de " + hh(a.depot_debut) + " à " + hh(a.depot_fin),
      retrait: "de " + hh(a.retrait_debut) + " à " + hh(a.retrait_fin),
      ouverture: "de " + hh(a.ouverture_debut) + " à " + hh(a.ouverture_fin),
      fermeture: fermetureTexte(c.fermeture_annuelle),
      delai: c.delai_rappel,
      conservation: c.conservation_donnees,
      raison_sociale: c.legal.raison_sociale,
      siret: c.legal.siret,
      directeur: c.legal.directeur_publication,
      agrement: c.legal.agrement_sanitaire,
      hebergeur: c.legal.hebergeur
    };
  }

  function appliquerConfig(c) {
    var v = valeurs(c);
    document.querySelectorAll("[data-cfg]").forEach(function (el) {
      var k = el.getAttribute("data-cfg");
      if (v[k] !== undefined) el.textContent = v[k];
    });
    document.querySelectorAll("a[data-cfg-tel]").forEach(function (a) {
      a.setAttribute("href", telLien(c.telephone));
    });
    document.querySelectorAll("a[data-cfg-mail]").forEach(function (a) {
      a.setAttribute("href", "mailto:" + c.email_contact);
      a.textContent = c.email_contact;
    });
    document.querySelectorAll("[data-simule]").forEach(function (el) { el.hidden = !c.simule; });
  }

  function appliquerAvis(ct) {
    var liste = document.querySelector("[data-avis]");
    if (!liste || !Array.isArray(ct.avis) || !ct.avis.length) return;
    liste.innerHTML = "";
    ct.avis.forEach(function (a) {
      var li = document.createElement("li");
      var bq = document.createElement("blockquote");
      var p = document.createElement("p");
      var f = document.createElement("footer");
      p.textContent = a.texte || "";
      f.textContent = a.auteur || "";
      bq.appendChild(p); bq.appendChild(f); li.appendChild(bq); liste.appendChild(li);
    });
  }

  function appliquerContenu(ct) {
    appliquerAvis(ct);
    document.querySelectorAll("[data-content]").forEach(function (el) {
      var k = el.getAttribute("data-content");
      if (typeof ct[k] === "string" && ct[k].trim()) el.textContent = ct[k];
    });
  }

  function charger(url) {
    return fetch(url, { cache: "no-cache" }).then(function (r) {
      if (!r.ok) throw new Error(url + " " + r.status);
      return r.json();
    });
  }

  /* ---------- Menu mobile ---------- */
  function initMenu() {
    var btn = document.querySelector(".menu-btn");
    var nav = document.getElementById("nav");
    if (!btn || !nav) return;
    btn.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      btn.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("open")) {
        nav.classList.remove("open");
        btn.setAttribute("aria-expanded", "false");
        btn.focus();
      }
    });
  }

  /* ---------- Formulaire de contact ---------- */
  function initFormulaire(c) {
    var form = document.getElementById("form-contact");
    if (!form) return;
    var debut = Date.now();

    function val(name) { var e = form.elements[name]; return e ? e.value.trim() : ""; }

    function valider() {
      var err = [];
      function add(champ, msg) { err.push({ champ: champ, msg: msg }); }
      if (!val("prenom")) add("prenom", "Indiquez votre prénom.");
      if (!val("nom")) add("nom", "Indiquez votre nom.");
      if (!/^0\d{9}$/.test(val("telephone").replace(/[\s.\-]/g, ""))) add("telephone", "Indiquez un numéro français à 10 chiffres.");
      if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val("email"))) add("email", "Indiquez une adresse e-mail valide.");
      if (!val("message")) add("message", "Écrivez votre message.");
      if (val("message").length > 2000) add("message", "Le message est limité à 2 000 caractères.");
      if (!form.elements["consentement"].checked) add("consentement", "Cochez la case de consentement pour envoyer votre message.");
      return err;
    }

    function afficherErreurs(err) {
      form.querySelectorAll(".field-error").forEach(function (e) { e.textContent = ""; });
      form.querySelectorAll("[aria-invalid]").forEach(function (e) { e.removeAttribute("aria-invalid"); });
      var resume = document.getElementById("resume-erreurs");
      if (!err.length) { resume.hidden = true; resume.innerHTML = ""; return; }
      var ul = document.createElement("ul");
      err.forEach(function (e) {
        var cible = document.getElementById(e.champ);
        var zone = document.getElementById("err-" + e.champ);
        if (zone) zone.textContent = e.msg;
        if (cible) cible.setAttribute("aria-invalid", "true");
        var li = document.createElement("li");
        var lien = document.createElement("a");
        lien.href = "#" + e.champ; lien.textContent = e.msg;
        lien.addEventListener("click", function (ev) { ev.preventDefault(); if (cible) cible.focus(); });
        li.appendChild(lien); ul.appendChild(li);
      });
      resume.innerHTML = "";
      var t = document.createElement("strong");
      t.textContent = err.length === 1 ? "Un champ est à corriger :" : err.length + " champs sont à corriger :";
      resume.appendChild(t); resume.appendChild(ul);
      resume.hidden = false;
      resume.focus();
    }

    function payload() {
      return {
        motif: "Contact / question",
        nom: val("nom"), prenom: val("prenom"), telephone: val("telephone"), email: val("email"),
        message: val("message"), consentement: true,
        delai_rappel: c.delai_rappel
      };
    }

    function confirmer() {
      var conf = document.getElementById("confirmation");
      form.hidden = true;
      conf.hidden = false;
      conf.focus();
    }

    var envoi = false;
    form.addEventListener("submit", function (ev) {
      ev.preventDefault();
      if (envoi) return;
      var err = valider();
      afficherErreurs(err);
      if (err.length) return;

      var erreurEnvoi = document.getElementById("erreur-envoi");
      erreurEnvoi.hidden = true;

      // Anti-spam sans contrainte : champ piege + delai minimal. Le robot croit avoir reussi.
      var robot = form.elements["site_web"].value || (Date.now() - debut < 3000);
      if (robot) { confirmer(); return; }

      var bouton = form.querySelector('button[type="submit"]');
      envoi = true; bouton.disabled = true; bouton.textContent = "Envoi en cours…";
      var url = c.formulaire_webhook;
      var requete = url
        ? fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(payload()) })
        : Promise.reject(new Error("webhook non configuré"));
      requete.then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        confirmer();
      }).catch(function () {
        erreurEnvoi.hidden = false;
        erreurEnvoi.focus();
        envoi = false; bouton.disabled = false; bouton.textContent = "Envoyer";
      });
    });
  }

  /* ---------- Demarrage ---------- */
  initMenu();
  Promise.all([
    charger("data/config.json"),
    charger("data/content.json").catch(function () { return {}; })
  ]).then(function (r) {
    appliquerConfig(r[0]);
    appliquerContenu(r[1]);
    initFormulaire(r[0]);
  }).catch(function () {
    // Sans config : le HTML statique reste affiche, le telephone reste visible.
    var erreur = document.getElementById("erreur-envoi");
    var f = document.getElementById("form-contact");
    if (f) { f.hidden = true; if (erreur) erreur.hidden = false; }
  });
})();
