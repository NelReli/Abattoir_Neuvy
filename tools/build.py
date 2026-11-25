#!/usr/bin/env python3
"""Genere les 6 pages HTML (en-tete et pied de page communs).
Usage : python tools/build.py   (depuis la racine du projet)
Les valeurs de data/config.json et data/content.json sont inscrites dans le HTML
(affichage sans JavaScript, referencement). Le JS les remet a jour a chaque visite.
"""
import hashlib
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "data/config.json").read_text(encoding="utf-8"))
CT = json.loads((ROOT / "data/content.json").read_text(encoding="utf-8"))

JOURS = ["dimanche", "lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi"]
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août",
        "septembre", "octobre", "novembre", "décembre"]


def hh(t):
    h, m = t.split(":")
    return f"{int(h)} h {m}"


def jours_txt(j):
    s = sorted(j, key=lambda d: (d + 6) % 7)
    if len(s) > 2 and all((s[i] + 6) % 7 == (s[i - 1] + 6) % 7 + 1 for i in range(1, len(s))):
        return f"du {JOURS[s[0]]} au {JOURS[s[-1]]}"
    if len(s) == 1:
        return f"le {JOURS[s[0]]}"
    return "les " + ", ".join(JOURS[d] for d in s[:-1]) + " et " + JOURS[s[-1]]


a = CFG["abattage"]
f = CFG["fermeture_annuelle"]
V = {
    "tel": CFG["telephone"],
    "adresse": CFG["adresse"],
    "jours": jours_txt(a["jours"]),
    "depot": f"de {hh(a['depot_debut'])} à {hh(a['depot_fin'])}",
    "retrait": f"de {hh(a['retrait_debut'])} à {hh(a['retrait_fin'])}",
    "ouverture": f"de {hh(a['ouverture_debut'])} à {hh(a['ouverture_fin'])}",
    "fermeture": f"du {'1er' if f['jour_debut'] == 1 else f['jour_debut']} au {f['jour_fin']} {MOIS[f['mois'] - 1]}",
    "delai": CFG["delai_rappel"],
    "conservation": CFG["conservation_donnees"],
    "raison_sociale": CFG["legal"]["raison_sociale"],
    "siret": CFG["legal"]["siret"],
    "directeur": CFG["legal"]["directeur_publication"],
    "agrement": CFG["legal"]["agrement_sanitaire"],
    "hebergeur": CFG["legal"]["hebergeur"],
}
TEL_HREF = "tel:+33" + CFG["telephone"].replace(" ", "").lstrip("0")
MAIL = CFG["email_contact"]


def c(key):
    """Span relie a data/config.json."""
    return f'<span data-cfg="{key}">{V[key]}</span>'


def t(key):
    """Attribut + texte relie a data/content.json."""
    return f'data-content="{key}"', CT[key]


NAV = [("index.html", "Accueil"), ("histoire.html", "Notre histoire"),
       ("services.html", "Nos services"), ("contact.html", "Contact")]

MENU_ICON = ('<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
             'stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 6h16M4 12h16M4 18h16"/></svg>')
PHONE_ICON = ('<svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">'
              '<path d="M6.6 10.8a15 15 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11 11 0 0 0 3.5.56 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.2.2 2.4.57 3.5a1 1 0 0 1-.25 1z"/></svg>')

# Numero de version des fichiers CSS et JS : change des qu'ils changent (evite le cache obsolete).
VER = hashlib.md5(b"".join((ROOT / n).read_bytes() for n in ("css/style.css", "js/main.js"))).hexdigest()[:8]

PHOTOS = {
    "poules-prairie": ("Poules en plein air sur une prairie", 1400, 788),
    "canards": ("Groupe de canards blancs sur l'herbe", 1000, 597),
    "poule-herbe": ("Poule marchant dans une prairie fleurie", 1000, 664),
    "nid-oeufs": ("Poule dans son nid, à côté de ses oeufs", 1000, 562),
    "oeufs-main": ("Deux oeufs frais dans une main, poules en arrière-plan", 1000, 662),
    "eleveur-cloture": ("Éleveur appuyé à la clôture de sa prairie", 1000, 662),
    "pintade": ("Pintade", 800, 600),
    "lapin": ("Lapin domestique", 800, 600),
    "poulet": ("Poule dans une prairie", 800, 600),
    "canard": ("Canards blancs", 800, 600),
}


def img(name, cls="", eager=False, alt=None):
    a_, w, h = PHOTOS[name]
    k = f' class="{cls}"' if cls else ""
    load = "" if eager else ' loading="lazy"'
    return f'<img{k} src="assets/photos/{name}.jpg" width="{w}" height="{h}" alt="{a_ if alt is None else alt}"{load}>'


STAMP = ('<div class="stamp"><svg viewBox="0 0 120 120" role="img" aria-label="Certifié bio Ecocert France depuis 2001">'
         '<circle cx="60" cy="60" r="57" fill="#ffffff" stroke="#2f7d1f" stroke-width="3"/>'
         '<circle cx="60" cy="60" r="35" fill="none" stroke="#5db946" stroke-width="1.5"/>'
         '<defs><path id="arc" d="M60,60 m-47,0 a47,47 0 1,1 94,0 a47,47 0 1,1 -94,0"/></defs>'
         '<text font-family="system-ui,Arial,sans-serif" font-size="10.5" font-weight="700" fill="#12307d">'
         '<textPath href="#arc" textLength="290" lengthAdjust="spacing">CERTIFIÉ BIO · ECOCERT FRANCE · </textPath></text>'
         '<text x="60" y="58" text-anchor="middle" font-family="Georgia,serif" font-size="9" font-weight="700" fill="#2f7d1f">DEPUIS</text>'
         '<text x="60" y="80" text-anchor="middle" font-family="Georgia,serif" font-size="27" font-weight="700" fill="#12307d">2001</text>'
         '</svg></div>')


def page(fichier, titre, description, corps, noindex=False):
    nav = "".join(
        f'<a href="{h}"{" aria-current=\"page\"" if h == fichier else ""}>{n}</a>' for h, n in NAV)
    liens = "".join(f'<li><a href="{h}">{n}</a></li>' for h, n in NAV)
    robots = '<meta name="robots" content="noindex">\n' if noindex else ""
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{titre}</title>
<meta name="description" content="{description}">
{robots}<meta name="theme-color" content="#fefdfb">
<link rel="icon" type="image/png" href="assets/logo-poule.png">
<link rel="stylesheet" href="css/style.css?v={VER}">
<script src="js/main.js?v={VER}" defer></script>
</head>
<body>
<a class="skip" href="#main">Aller au contenu</a>
<header class="site-header">
  <div class="wrap bar">
    <a class="brand" href="index.html"><img src="assets/logo-poule.png" alt="" width="34" height="40"><span>Abattoir de Neuvy</span></a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav"><span class="sr">Menu</span>{MENU_ICON}</button>
    <nav id="nav" class="nav" aria-label="Navigation principale">{nav}</nav>
    <a class="head-tel" data-cfg-tel href="{TEL_HREF}">{c("tel")}</a>
  </div>
</header>
<main id="main">
{corps}
</main>
<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <p class="foot-logo"><img src="assets/logo-complet.png" width="900" height="655" alt="Logo Abattoir de Neuvy : une poule au trait bleu marine et vert" loading="lazy"></p>
      <div>
        <h2>Contact</h2>
        <p>Abattoir de Neuvy<br>{c("adresse")}<br><a data-cfg-tel href="{TEL_HREF}">{c("tel")}</a><br><a data-cfg-mail href="mailto:{MAIL}">{MAIL}</a></p>
      </div>
      <div>
        <h2>Le site</h2>
        <ul>{liens}</ul>
      </div>
      <div>
        <h2>Légal</h2>
        <ul>
          <li><a href="mentions-legales.html">Mentions légales</a></li>
          <li><a href="confidentialite.html">Confidentialité</a></li>
        </ul>
        <p class="foot-bio">Certifié bio Ecocert France</p>
      </div>
    </div>
    <p class="copy">© Abattoir de Neuvy</p>
  </div>
</footer>
<a class="callbar" data-cfg-tel href="{TEL_HREF}">{PHONE_ICON}<span>Appeler le {c("tel")}</span></a>
</body>
</html>
"""


def hero(photo, titre, boutons="", petit=False, attr=""):
    cls = "hero-img small" if petit else "hero-img"
    return f"""
<section class="{cls}">
  {img(photo, eager=True, alt="")}
  <div class="wrap">
    <h1 {attr}>{titre}</h1>
    {boutons}
  </div>
</section>"""


BTN_CRENEAU = '<a class="btn btn-white" href="contact.html#formulaire">Nous contacter</a>'
BTN_APPEL = f'<a class="btn btn-line" data-cfg-tel href="{TEL_HREF}">Appeler</a>'


def story(titre, sous_titre, texte, photo, flip=False, attr="", bouton=""):
    sub = f'<p class="script">{sous_titre}</p>' if sous_titre else ""
    cls = "story flip" if flip else "story"
    return f"""
<section class="{cls}" style="padding:0">
  <div class="story-panel">
    <h2>{titre}</h2>
    {sub}
    <p {attr}>{texte}</p>
    {bouton}
  </div>
  <div class="story-photo">{img(photo)}</div>
</section>"""


# ---------------------------------------------------------------- Accueil
def avis_section():
    items = "".join(
        f'<li><blockquote><p>{a_["texte"]}</p><footer>{a_["auteur"]}</footer></blockquote></li>'
        for a_ in CT.get("avis", []))
    return f"""
<section class="avis">
  <div class="wrap">
    <img class="avis-icon" src="assets/logo-poule.png" width="46" height="54" alt="" loading="lazy">
    <h2>Avis de nos clients</h2>
    <ul class="avis-list" data-avis>{items}</ul>
    <div class="parade" aria-hidden="true">{"".join(poussin("vers-droite") for _ in range(5))}</div>
  </div>
</section>"""


def accueil():
    k_acc, v_acc = t("accroche")
    k_int, v_int = t("accueil_intro")
    galerie = "".join(f'<li>{img(n)}</li>' for n in
                      ("poule-herbe", "oeufs-main", "canards", "eleveur-cloture", "nid-oeufs", "poules-prairie"))
    corps = hero("poules-prairie", v_acc, f'<div class="btn-row">{BTN_CRENEAU}{BTN_APPEL}</div>', attr=k_acc) + f"""

<div class="trio">
  <div class="tile">
    {img("nid-oeufs", alt="")}
    <div class="label"><h3>Notre<br>histoire</h3><a href="histoire.html">L'histoire</a></div>
  </div>
  <div class="tile tile-panel">
    <div>
      {STAMP}
      <h3>Nos services</h3>
      <p>Abattage, préparation, conditionnement</p>
      <a class="btn btn-primary" href="services.html">Découvrir</a>
    </div>
  </div>
  <div class="tile">
    {img("eleveur-cloture", alt="")}
    <div class="label"><h3>Nous<br>contacter</h3><a href="contact.html#formulaire">Contact</a></div>
  </div>
</div>

<section class="intro">
  <div class="wrap">
    <img class="icon" src="assets/logo-poule.png" width="58" height="68" alt="" loading="lazy">
    <h2>L'Abattoir de Neuvy</h2>
    <p {k_int}>{v_int}</p>
  </div>
</section>
{avis_section()}

<section>
  <div class="wrap center">
    <h2>En images</h2>
    <ul class="galerie" style="list-style:none;padding:0">{galerie}</ul>
  </div>
</section>

<script type="application/ld+json">
{json.dumps({"@context": "https://schema.org", "@type": "LocalBusiness", "name": "Abattoir de Neuvy",
             "description": "Abattoir de volailles et de lapins certifié bio Ecocert France, Deux-Sèvres.",
             "telephone": "+33549635130",
             "address": {"@type": "PostalAddress", "streetAddress": "Le Fay", "postalCode": "79130",
                         "addressLocality": "Neuvy-Bouin", "addressCountry": "FR"}},
            ensure_ascii=False)}
</script>"""
    return page("index.html", "Abattoir de volailles bio en Deux-Sèvres | Abattoir de Neuvy",
                "Abattoir de volailles et de lapins certifié bio Ecocert France à Neuvy-Bouin (Deux-Sèvres). Contactez-nous en ligne.",
                corps)


# ---------------------------------------------------------------- Histoire
def histoire():
    p = {k: t(k) for k in ("histoire_1", "histoire_2", "histoire_3", "histoire_4")}
    corps = hero("poules-prairie", "Notre<br>histoire", petit=True)
    corps += story("L'histoire", "Une ferme et un abattoir à taille humaine", p["histoire_1"][1], "eleveur-cloture", attr=p["histoire_1"][0])
    corps += story("Certifié bio", "Ecocert France, depuis le 28 juin 2001", p["histoire_2"][1], "poule-herbe", flip=True, attr=p["histoire_2"][0])
    corps += story("Bien-être animal", "Un environnement calme", p["histoire_3"][1], "canards", attr=p["histoire_3"][0])
    corps += story("Traçabilité", "De l'élevage à l'assiette", p["histoire_4"][1], "nid-oeufs", flip=True, attr=p["histoire_4"][0],
                   bouton='<div class="btn-row center"><a class="btn btn-primary" href="services.html">Découvrir nos services</a></div>')
    return page("histoire.html", "Notre histoire, abattage bio | Abattoir de Neuvy",
                "Ferme et abattoir à taille humaine à Neuvy-Bouin, certifiés bio Ecocert France depuis le 28 juin 2001. Bien-être animal et traçabilité.",
                corps)


# ---------------------------------------------------------------- Services
def services():
    boutons = ('<div class="btn-row">' + BTN_CRENEAU +
               '<a class="btn btn-line" href="contact.html#formulaire">Demander un tarif</a></div>')
    corps = hero("canards", "Nos<br>services", boutons, petit=True) + f"""

<section class="center">
  <div class="wrap">
    <h2>Espèces</h2>
    <ul class="especes-row">
      <li>{img("poulet")}<span>Poulets</span></li><li>{img("pintade")}<span>Pintades</span></li><li>{img("canard")}<span>Canards</span></li><li>{img("lapin")}<span>Lapins</span></li>
    </ul>
  </div>
</section>

<section class="band center">
  <div class="wrap">
    <h2>Prestations</h2>
    <ul class="cols c3">
      <li><span class="num">01</span><h3>Abattage de volailles et de lapins</h3><p>Abattage de poulets, pintades, canards et lapins, dans le respect des normes sanitaires et du bien-être animal.</p></li>
      <li><span class="num">02</span><h3>Préparation et transformation</h3><p>Plumage, éviscération, découpe, et bridage sur demande.</p></li>
      <li><span class="num">03</span><h3>Conditionnement</h3><p>Conditionnement sous vide et étiquetage, dans le respect de l'hygiène et de la qualité.</p></li>
      <li><span class="num">04</span><h3>Gestion et traçabilité</h3><p>Suivi de chaque lot, de la réception des animaux à la remise des carcasses.</p></li>
      <li><span class="num">05</span><h3>Accompagnement des professionnels</h3><p>Appui aux éleveurs dans une relation de partenariat durable.</p></li>
    </ul>
  </div>
</section>

<section class="center">
  <div class="wrap">
    <h2>Le processus</h2>
    <ol class="process">
      <li><span class="n">1</span><strong>Réception</strong><p>Réception des animaux déposés par l'éleveur.</p></li>
      <li><span class="n">2</span><strong>Contrôle</strong><p>Contrôle des animaux et du lot.</p></li>
      <li><span class="n">3</span><strong>Abattage</strong></li>
      <li><span class="n">4</span><strong>Préparation</strong><p>Plumage, éviscération, découpe, bridage.</p></li>
      <li><span class="n">5</span><strong>Conditionnement</strong><p>Sous vide, étiquetage.</p></li>
      <li><span class="n">6</span><strong>Expédition</strong><p>Remise des carcasses à l'éleveur lors de l'enlèvement.</p></li>
    </ol>
  </div>
</section>

<section class="band visit">
  <div class="wrap">
    <h2>Jours et horaires</h2>
    <div class="visit-cols">
      <p><strong>Jours d'abattage</strong>{c("jours")}<strong>Fermeture annuelle</strong>{c("fermeture")}</p>
      <p><strong>Dépôt des animaux</strong>Le jour même, {c("depot")}<strong>Retrait des carcasses</strong>Le jour même, {c("retrait")}</p>
    </div>
  </div>
</section>

<section class="story" style="padding:0">
  <div class="story-panel">
    <h2>Tarifs sur demande</h2>
    <div class="btn-row center">
      <a class="btn btn-primary" href="contact.html#formulaire">Demander un tarif</a>
    </div>
  </div>
  <div class="story-photo">{img("poule-herbe")}</div>
</section>"""
    return page("services.html", "Services d'abattage de volailles et lapins | Abattoir de Neuvy",
                "Abattage, plumage, éviscération, découpe, conditionnement sous vide et étiquetage de volailles et lapins bio. Tarifs sur demande.",
                corps)


# ---------------------------------------------------------------- Contact
def champ(id_, label, type_="text", extra="", autocomplete=""):
    ac = f' autocomplete="{autocomplete}"' if autocomplete else ""
    return (f'<div class="field"><label for="{id_}">{label} <span class="req" aria-hidden="true">*</span></label>'
            f'<input type="{type_}" id="{id_}" name="{id_}"{ac} {extra} aria-required="true" aria-describedby="err-{id_}">'
            f'<div class="field-error" id="err-{id_}" role="status"></div></div>')


def poussin(cls=""):
    """Petit poussin dessine (decoratif), tourne vers la gauche par defaut."""
    return (f'<svg class="poussin {cls}" viewBox="0 0 40 36" aria-hidden="true" focusable="false">'
            '<path d="M13 29v5m0 0h-4m4 0l3 1M25 29v5m0 0h-4m4 0l3 1" fill="none" stroke="#e8710a" stroke-width="1.8" stroke-linecap="round"/>'
            '<path d="M12 6c6-2 11 2 12 7 5 0 9-2 13-5 1 8-1 14-5 18-4 4-11 5-17 3C8 27 5 22 6 16 4 11 7 7 12 6Z" fill="#f7b514"/>'
            '<path d="M18 19c3 4 9 4 13 0" fill="none" stroke="#e09600" stroke-width="1.8" stroke-linecap="round"/>'
            '<path d="M7 11L1 14l6 2Z" fill="#e8710a"/><circle cx="12" cy="12" r="1.7" fill="#12307d"/></svg>')


def contact():
    corps = f"""
<section class="band visit">
  <div class="wrap">
    <div class="famille">
      {poussin("vers-droite")}
      <img class="icon" src="assets/logo-poule.png" width="58" height="68" alt="">
      {poussin()}{poussin("petit")}
    </div>
    <h2>Visiter l'abattoir</h2>
    <div class="visit-cols">
      <p><strong>Adresse</strong>Abattoir de Neuvy<br>{c("adresse")}</p>
      <p><strong>Horaires</strong>Ouvert {c("ouverture")}<br>Abattage {c("jours")}<br>Fermeture : {c("fermeture")}</p>
    </div>
    <div class="btn-row center">
      <a class="btn btn-ghost" href="https://www.google.com/maps/search/?api=1&query=Abattoir+de+Neuvy%2C+Le+Fay%2C+79130+Neuvy-Bouin" rel="noopener" target="_blank">Carte d'accès<span class="sr"> (nouvelle fenêtre)</span></a>
    </div>
  </div>
</section>

<section>
  <div class="wrap">
    <div class="contact-card">
      <div class="contact-panel" id="formulaire">
        <h1 class="panel-title">Contact</h1>
        <p class="panel-line"><a data-cfg-tel href="{TEL_HREF}">{c("tel")}</a><span aria-hidden="true">|</span><a data-cfg-mail href="mailto:{MAIL}">{MAIL}</a></p>

        <div>
          <div id="erreur-envoi" class="error-summary" role="alert" tabindex="-1" hidden>
            <strong>Votre message n'a pas pu être envoyé.</strong>
            Appelez-nous au <a data-cfg-tel href="{TEL_HREF}">{c("tel")}</a>.
          </div>
          <div id="confirmation" class="confirm" role="status" tabindex="-1" hidden>
            <h2>Merci !</h2>
            <p><strong>Votre message est bien reçu. Nous vous rappelons sous {c("delai")}.</strong></p>
            <p>Un e-mail d'accusé de réception vous a été envoyé.</p>
            <div class="btn-row"><a class="btn btn-ghost" href="index.html">Retour à l'accueil</a></div>
          </div>

          <form id="form-contact" class="form-clean" novalidate>
            <div id="resume-erreurs" class="error-summary" role="alert" tabindex="-1" hidden></div>
            <div class="form-row">
              {champ("prenom", "Prénom", autocomplete="given-name")}
              {champ("nom", "Nom", autocomplete="family-name")}
            </div>
            <div class="form-row">
              {champ("telephone", "Téléphone", "tel", 'inputmode="tel"', "tel")}
              {champ("email", "E-mail", "email", 'inputmode="email"', "email")}
            </div>
            <div class="field">
              <label for="message">Message <span class="req" aria-hidden="true">*</span></label>
              <textarea id="message" name="message" maxlength="2000" aria-required="true" aria-describedby="err-message"></textarea>
              <div class="field-error" id="err-message" role="status"></div>
            </div>

            <div class="hp" aria-hidden="true"><label for="site_web">Ne pas remplir</label><input type="text" id="site_web" name="site_web" tabindex="-1" autocomplete="off"></div>

            <div class="send">
              <label class="consent" for="consentement">
                <input type="checkbox" id="consentement" name="consentement" aria-describedby="err-consentement">
                <span>J'accepte que mes données soient utilisées pour traiter ma demande (<a href="confidentialite.html">confidentialité</a>). <span class="req" aria-hidden="true">*</span></span>
              </label>
              <div class="field-error" id="err-consentement" role="status"></div>
              <button class="btn btn-primary btn-big" type="submit">Envoyer</button>
            </div>
          </form>
        </div>
      </div>
      <div class="contact-photo">{img("eleveur-cloture", alt="")}</div>
    </div>
  </div>
</section>"""
    return page("contact.html", "Contact | Abattoir de Neuvy",
                "Contactez l'Abattoir de Neuvy, Le Fay, 79130 Neuvy-Bouin, pour une question ou un tarif. Téléphone : 05 49 63 51 30.",
                corps)


# ---------------------------------------------------------------- Legal
SIMULE = ('<p class="note-simule" data-simule>Valeurs fictives [SIMULÉ] : à remplacer par les vraies informations '
          'de l\'abattoir avant la mise en ligne (modifiables dans l\'administration).</p>')


def mentions():
    corps = f"""
<section class="page-title"><div class="wrap"><h2 style="font-size:1.8rem">Mentions légales</h2></div></section>
<section style="padding-top:0">
  <div class="wrap prose">
    {SIMULE}
    <h2>Éditeur du site</h2>
    <ul>
      <li>Raison sociale : {c("raison_sociale")}</li>
      <li>SIRET : {c("siret")}</li>
      <li>Adresse : {c("adresse")}</li>
      <li>Téléphone : <a data-cfg-tel href="{TEL_HREF}">{c("tel")}</a></li>
      <li>Numéro d'agrément sanitaire : {c("agrement")}</li>
    </ul>
    <h2>Directeur de la publication</h2>
    <p>{c("directeur")}</p>
    <h2>Hébergeur</h2>
    <p>{c("hebergeur")}</p>
    <h2>Certification</h2>
    <p>Abattoir certifié bio par Ecocert France depuis le 28 juin 2001.</p>
    <h2>Propriété intellectuelle</h2>
    <p>Le logo et les textes sont la propriété de l'Abattoir de Neuvy.</p>
    <h2>Crédits photos</h2>
    <p>Photos provisoires libres de droits (United States Department of Agriculture pour la plupart), via Wikimedia Commons, en attendant le reportage photo de l'abattoir. Elles ne représentent pas l'abattoir.</p>
    <ul>
      <li><a href="https://commons.wikimedia.org/wiki/File:20210619-USDA-OC-PSD-0248_Agriculture_in_the_United_States_(United_States_Department_of_Agriculture)_USDA_images.jpg" rel="noopener">Poules en plein air</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:20160521-RD-LSC-0422_(27438400130).jpg" rel="noopener">Canards blancs</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:20130712-USDA-OC-PSD-0026_Agriculture_in_the_United_States.jpg" rel="noopener">Oeufs dans une main</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:Nick%27s_Organic_Farm_(20130712-AMS-LSC-0666).jpg" rel="noopener">Éleveur à la clôture</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:20110505-USDA-OC-PSD-0008_Agriculture_in_the_United_States.jpg" rel="noopener">Poule dans l'herbe</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:20210619-USDA-OC-PSD-0245_Agriculture_in_the_United_States_(United_States_Department_of_Agriculture)_USDA_images.jpg" rel="noopener">Poule au nid</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:Helmeted_guineafowl_(Numida_meleagris),_Kenya.jpg" rel="noopener">Pintade (CC0)</a></li>
      <li><a href="https://commons.wikimedia.org/wiki/File:Oryctolagus_cuniculus_domesticus_-_Nart_Barileva_-_605739065.jpeg" rel="noopener">Lapin (CC0)</a></li>
    </ul>
  </div>
</section>"""
    return page("mentions-legales.html", "Mentions légales | Abattoir de Neuvy",
                "Mentions légales du site de l'Abattoir de Neuvy.", corps, noindex=True)


def confidentialite():
    corps = f"""
<section class="page-title"><div class="wrap"><h2 style="font-size:1.8rem">Politique de confidentialité</h2></div></section>
<section style="padding-top:0">
  <div class="wrap prose">
    {SIMULE}
    <h2>Responsable du traitement</h2>
    <p>{c("raison_sociale")}, {c("adresse")}. Contact : <a data-cfg-mail href="mailto:{MAIL}">{MAIL}</a>.</p>
    <h2>Données collectées</h2>
    <p>Lorsque vous envoyez le formulaire de contact, nous collectons : nom, prénom, téléphone, e-mail et message.</p>
    <h2>Finalité</h2>
    <p>Ces données servent uniquement à traiter votre demande et à vous rappeler. Elles ne sont ni vendues ni utilisées à des fins publicitaires.</p>
    <h2>Base légale</h2>
    <p>Votre consentement, donné en cochant la case du formulaire.</p>
    <h2>Destinataires</h2>
    <p>Les personnes de l'abattoir qui traitent les demandes, et les outils d'envoi d'e-mails utilisés pour acheminer votre demande.</p>
    <h2>Durée de conservation</h2>
    <p>Vos données sont conservées {c("conservation")} au plus, puis supprimées.</p>
    <h2>Vos droits</h2>
    <p>Vous pouvez demander l'accès à vos données, leur rectification ou leur suppression en écrivant à <a data-cfg-mail href="mailto:{MAIL}">{MAIL}</a> ou en appelant le <a data-cfg-tel href="{TEL_HREF}">{c("tel")}</a>. Vous pouvez aussi saisir la CNIL (cnil.fr).</p>
    <h2>Cookies</h2>
    <p>Ce site n'utilise aucun cookie publicitaire ni outil de mesure d'audience.</p>
  </div>
</section>"""
    return page("confidentialite.html", "Politique de confidentialité | Abattoir de Neuvy",
                "Politique de confidentialité et protection des données (RGPD) du site de l'Abattoir de Neuvy.", corps, noindex=True)


if __name__ == "__main__":
    for nom, fn in [("index.html", accueil), ("histoire.html", histoire), ("services.html", services),
                    ("contact.html", contact), ("mentions-legales.html", mentions),
                    ("confidentialite.html", confidentialite)]:
        (ROOT / nom).write_text(fn(), encoding="utf-8")
        print("ok", nom)
