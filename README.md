# Site vitrine Abattoir de Neuvy (V1)

Site statique (HTML, CSS, JavaScript). Aucune dépendance, aucun cookie.

## Structure
- `index.html`, `histoire.html`, `services.html`, `contact.html`, `mentions-legales.html`, `confidentialite.html`
- `data/config.json` : jours, horaires, fermeture, délai, données légales. Utilisé par le formulaire et la page Services (RG-07).
- `data/content.json` : textes modifiables (accroche, histoire, introductions).
- `.pages.yml` : écrans d'administration pour Pages CMS.
- `n8n/workflow-demande.json` : workflow à importer dans n8n (2 e-mails par demande, RG-09).
- `tools/build.py` : régénère les 6 pages HTML. À relancer seulement si on modifie la structure des pages : `python tools/build.py`.

## Mise en ligne (outils gratuits)
1. Créer un dépôt GitHub avec ce dossier. Activer GitHub Pages (ou Cloudflare Pages / Netlify gratuit).
2. Réserver le nom de domaine et créer l'adresse e-mail (seuls coûts).
3. Dans n8n : importer `n8n/workflow-demande.json`, créer les identifiants SMTP, mettre l'adresse de l'abattoir, activer le workflow. Copier l'URL de production du webhook dans `formulaire_webhook` de `data/config.json`.
4. Administration : se connecter sur https://pagescms.org avec le compte GitHub du dépôt. L'abattoir modifie horaires, jours, fermetures et textes dans des formulaires, puis enregistre.

## Avant la mise en ligne
Remplacer toutes les valeurs `[SIMULÉ]` de `data/config.json` (SIRET, agrément, dirigeant, hébergeur, jours, horaires, fermeture, délai, durée de conservation). Puis passer `simule` à `false`.
Les e-mails du workflow n8n contiennent l'adresse, le téléphone et `contact@abattoir-neuvy.fr` : à ajuster si le domaine change.

## Photos
`assets/photos/` contient 6 photos du domaine public (USDA, via Wikimedia Commons), sans obligation d'attribution. Les crédits figurent dans les mentions légales (`tools/build.py`). Elles ne montrent pas l'abattoir : les remplacer par le reportage photo en gardant les mêmes noms de fichier, ou modifier `PHOTOS` dans `tools/build.py` puis relancer `python tools/build.py`. Pas de photo de lapin : aucune photo libre de qualité n'a été trouvée.

## Tester en local
```
python -m http.server 8080
```
Ouvrir http://localhost:8080 (le chargement de `data/*.json` exige un serveur, pas un double-clic).
