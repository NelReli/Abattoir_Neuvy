#!/usr/bin/env python3
"""Seconde proposition : tout le site sur une seule page (onepage.html).
Usage : python tools/build_onepage.py   (depuis la racine du projet)
Les pages du site actuel ne sont pas modifiees. Memes donnees : data/*.json.
"""
import hashlib
import html

import build as b

ROOT = b.ROOT
VER = hashlib.md5(b"".join((ROOT / n).read_bytes()
                            for n in ("css/onepage.css", "js/main.js", "js/onepage.js"))).hexdigest()[:8]

ANCRES = [("abattoir", "L'abattoir"), ("services", "Services"), ("processus", "Processus"), ("contact", "Contact")]


def arches():
    # Les textes viennent de data/config.json, rafraichis a l'ouverture par js/main.js
    """Jours et horaires dans des arches, la forme des photos d'especes."""
    blocs = "".join(f'<li class="{cls}"><h3>{titre}</h3><p>{b.c(cle)}</p></li>' for cls, titre, cle in (
        ("jour", "Abattage", "jours"), ("depot", "Dépôt des animaux", "depot"),
        ("retrait", "Retrait des carcasses", "retrait")))
    return f"""
    <h2>Jours et horaires</h2>
    <ul class="arches" data-reveal>{blocs}</ul>
    <p class="ouvert-ferme">Ouvert {b.c("ouverture")}. Fermeture annuelle {b.c("fermeture")}.</p>"""


def passage(nombre, fond, retour=False):
    """Colline aux couleurs de la section suivante ; des poussins la traversent au rythme du defilement."""
    sens = " retour" if retour else ""
    poussins = "".join(b.poussin() for _ in range(nombre))
    svg = '<svg class="{}" viewBox="0 0 100 48" preserveAspectRatio="none" focusable="false"><path d="{}"/></svg>'
    colline = (svg.format("colline", "M0 48Q50-48 100 48Z")
               + svg.format("trace", "M0 48Q50-48 100 48").replace("<path ", '<path vector-effect="non-scaling-stroke" '))
    return (f'<div class="passage vers-{fond}{sens}" aria-hidden="true"><div class="piste">'
            f'{colline}<div class="bande">{poussins}</div></div></div>')


def page():
    nav = "".join(f'<a href="#{i}">{n}</a>' for i, n in ANCRES)
    especes = "".join(f"<li>{b.img(i)}<span>{n}</span></li>" for i, n in
                      (("poulet", "Poulets"), ("pintade", "Pintades"), ("canard", "Canards"), ("lapin", "Lapins")))
    chapitres = ""
    for cle, titre in (("histoire_1", "À taille humaine"), ("histoire_2", "Bio depuis le 28 juin 2001"),
                       ("histoire_3", "Un environnement calme"), ("histoire_4", "De l'élevage à l'assiette")):
        attr, texte = b.t(cle)
        chapitres += f"<article><h3>{titre}</h3><p {attr}>{texte}</p></article>"
    services = "".join(f"<div><dt>{n}</dt><dd>{d}</dd></div>" for n, d in (
        ("Abattage de volailles et de lapins", "Poulets, pintades, canards et lapins, dans le respect des normes sanitaires et du bien-être animal."),
        ("Préparation et transformation", "Plumage, éviscération, découpe, et bridage sur demande."),
        ("Conditionnement", "Conditionnement sous vide et étiquetage, dans le respect de l'hygiène et de la qualité."),
        ("Gestion et traçabilité", "Suivi de chaque lot, de la réception des animaux à la remise des carcasses."),
        ("Accompagnement des professionnels", "Appui aux éleveurs dans une relation de partenariat durable.")))
    etapes = "".join(f"<li><strong>{n}</strong><span>{d}</span></li>" for n, d in (
        ("Réception", "Animaux déposés par l'éleveur"), ("Contrôle", "Des animaux et du lot"),
        ("Abattage", "Sur le site de Neuvy-Bouin"), ("Préparation", "Plumage, éviscération, découpe, bridage"),
        ("Conditionnement", "Sous vide et étiquetage"), ("Expédition", "Carcasses remises à l'enlèvement")))
    avis = "".join(f'<li><blockquote><p>{html.escape(a["texte"])}</p><footer>{html.escape(a["auteur"])}</footer></blockquote></li>'
                   for a in b.CT.get("avis", []))
    k_acc, v_acc = b.t("accroche")
    k_int, v_int = b.t("accueil_intro")
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta http-equiv="Content-Security-Policy" content="{b.CSP}">
<meta name="referrer" content="strict-origin-when-cross-origin">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Abattoir de Neuvy, abattage bio de volailles et de lapins</title>
<meta name="description" content="Abattoir de volailles et de lapins certifié bio Ecocert France à Neuvy-Bouin (Deux-Sèvres).">
<meta name="robots" content="noindex">
<meta name="theme-color" content="#12307d">
<link rel="icon" type="image/png" href="assets/logo-poule.png">
<link rel="stylesheet" href="css/onepage.css?v={VER}">
<script src="js/main.js?v={VER}" defer></script>
<script src="js/onepage.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<header class="tete">
  <div class="cadre">
    <a class="marque" href="#main"><img src="assets/logo-poule.png" alt="" width="34" height="40"><span>Abattoir de Neuvy</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav"><span class="sr">Menu</span>{b.MENU_ICON}</button>
    <nav id="nav" class="nav" aria-label="Sections de la page">{nav}</nav>
    <a class="tete-tel" data-cfg-tel href="{b.TEL_HREF}">{b.c("tel")}</a>
  </div>
</header>

<main id="main">
<section class="ouverture">
  {b.img("poules-prairie", eager=True)}
  <div class="cadre">
    <div class="annonce">
      <h1 {k_acc}>{v_acc}</h1>
      <p>Certifié bio par Ecocert France, à Neuvy-Bouin dans les Deux-Sèvres.</p>
      <div class="actions">
        <a class="bouton vert" data-cfg-tel href="{b.TEL_HREF}">Appeler</a>
        <a class="bouton clair" href="#contact">Écrire à l'abattoir</a>
      </div>
    </div>
  </div>
  <p class="tampon" data-reveal><span>Bio depuis</span> <strong>2001</strong></p>
</section>

{passage(3, "brume")}
<section id="abattoir" class="abattoir">
  <div class="cadre">
    <div class="presentation">
      <h2>Une ferme et un abattoir</h2>
      <p {k_int}>{v_int}</p>
      {b.img("eleveur-cloture")}
    </div>
    <div class="chapitres">{chapitres}</div>
  </div>
</section>

{passage(4, "blanc", True)}
<section class="especes">
  <div class="cadre">
    <h2>Quatre espèces</h2>
    <ul data-reveal>{especes}</ul>
  </div>
</section>

{passage(3, "vert")}
<section id="services" class="services">
  <div class="cadre">
    <h2>Services</h2>
    <dl>{services}</dl>
    <p class="tarifs">Tarifs sur demande. <a href="#contact">Demander un tarif</a></p>
  </div>
</section>

{passage(5, "blanc", True)}
<section id="processus" class="processus">
  <div class="cadre">
    <h2>Le parcours d'un lot</h2>
    <ol data-reveal>{etapes}</ol>
  </div>
</section>

{passage(2, "brume")}
<section class="avis">
  <div class="cadre">
    <h2>Avis de nos clients</h2>
    <ul data-avis data-reveal>{avis}</ul>
  </div>
</section>

{passage(4, "blanc", True)}
<section id="horaires" class="horaires">
  <div class="cadre">
    {arches()}
  </div>
</section>

{passage(3, "marine")}
<section id="contact" class="contact">
  <div class="cadre">
    <div class="venir">
      <h2>Nous contacter</h2>
      <p class="grand-tel"><a data-cfg-tel href="{b.TEL_HREF}">{b.c("tel")}</a></p>
      <p><a data-cfg-mail href="mailto:{b.MAIL}">{b.MAIL}</a></p>
      <p>Abattoir de Neuvy<br>{b.c("adresse")}</p>
      <p>Ouvert {b.c("ouverture")}<br>Abattage {b.c("jours")}</p>
      <a class="bouton clair" href="https://www.google.com/maps/search/?api=1&amp;query=Abattoir+de+Neuvy%2C+Le+Fay%2C+79130+Neuvy-Bouin" rel="noopener" target="_blank">Carte d'accès<span class="sr"> (nouvelle fenêtre)</span></a>
    </div>
    <div class="ecrire">
      <div id="erreur-envoi" class="resume" role="alert" tabindex="-1" hidden>
        <strong>Votre message n'a pas pu être envoyé.</strong>
        Appelez-nous au <a data-cfg-tel href="{b.TEL_HREF}">{b.c("tel")}</a>.
      </div>
      <div id="confirmation" role="status" tabindex="-1" hidden>
        <h3>Merci !</h3>
        <p><strong>Votre message est bien reçu. Nous vous rappelons sous {b.c("delai")}.</strong></p>
        <p>Un e-mail d'accusé de réception vous a été envoyé.</p>
      </div>
      <form id="form-contact" novalidate>
        <div id="resume-erreurs" class="resume" role="alert" tabindex="-1" hidden></div>
        <div class="duo">{b.champ("prenom", "Prénom", autocomplete="given-name")}{b.champ("nom", "Nom", autocomplete="family-name")}</div>
        <div class="duo">{b.champ("telephone", "Téléphone", "tel", 'inputmode="tel"', "tel")}{b.champ("email", "E-mail", "email", 'inputmode="email"', "email")}</div>
        <div class="field">
          <label for="message">Message <span class="req" aria-hidden="true">*</span></label>
          <textarea id="message" name="message" rows="5" maxlength="2000" aria-required="true" aria-describedby="err-message"></textarea>
          <div class="field-error" id="err-message" role="status"></div>
        </div>
        <div class="hp" aria-hidden="true"><label for="site_web">Ne pas remplir</label><input type="text" id="site_web" name="site_web" tabindex="-1" autocomplete="off"></div>
        <label class="consentement" for="consentement">
          <input type="checkbox" id="consentement" name="consentement" aria-describedby="err-consentement">
          <span>J'accepte que mes données soient utilisées pour traiter ma demande (<a href="confidentialite.html">confidentialité</a>). <span class="req" aria-hidden="true">*</span></span>
        </label>
        <div class="field-error" id="err-consentement" role="status"></div>
        <button class="bouton plein" type="submit">Envoyer</button>
      </form>
    </div>
  </div>
</section>
</main>

<footer class="pied">
  <div class="cadre">
    <p>© Abattoir de Neuvy, certifié bio Ecocert France</p>
    <p><a href="mentions-legales.html">Mentions légales</a><a href="confidentialite.html">Confidentialité</a></p>
  </div>
</footer>
<a class="barre-appel" data-cfg-tel href="{b.TEL_HREF}">{b.PHONE_ICON}<span>Appeler le {b.c("tel")}</span></a>
<script type="application/ld+json">{b.fiche()}</script>
</body>
</html>
"""


if __name__ == "__main__":
    (ROOT / "onepage.html").write_text(page(), encoding="utf-8")
    print("ok onepage.html")
