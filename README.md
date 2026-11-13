# SantéFaso

Assistant de santé de proximité pour les familles du Burkina Faso, en français.
Projet réalisé pour le tournoi de développement **CADEV 2026**.

> SantéFaso est un outil d'information et d'orientation. Il ne remplace pas une
> consultation médicale et ne pose aucun diagnostic.

## Le problème

Le paludisme, les diarrhées et les retards de vaccination touchent encore beaucoup de
familles. Beaucoup ne savent pas **quand s'inquiéter** ni **quels vaccins** leur enfant doit
recevoir.

## Les trois modules

1. **Orientation des symptômes** : un court questionnaire (âge, fièvre, durée, symptômes,
   signes de danger, grossesse) donne un niveau d'alerte : *urgence*, *à consulter rapidement*
   ou *à surveiller*, avec les raisons et des conseils. Les règles s'inspirent des signes de
   danger de l'OMS (PCIME) et choisissent toujours le niveau le plus prudent.
2. **Carnet vaccinal de l'enfant** : à partir de la date de naissance et des étapes déjà
   faites, l'application affiche la prochaine étape, les retards et le calendrier détaillé
   (export CSV).
3. **Prévention** : conseils pratiques (paludisme, eau et hygiène, diarrhée, vaccination,
   grossesse).

## Lancer le projet

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Lancer les tests

```bash
python -m pytest -q
```

## Déployer gratuitement (lien public pour le jury)

1. Créer un dépôt GitHub avec les fichiers du projet.
2. Aller sur https://share.streamlit.io, se connecter avec GitHub.
3. « New app » → choisir le dépôt, la branche, et `app.py` comme fichier principal.

## Structure

| Fichier | Rôle |
|---|---|
| `app.py` | Pages et navigation Streamlit (Accueil, Orientation, Carnet vaccinal, Prévention, Le projet) |
| `ui.py` | Identité visuelle (palette, polices, tissage) et composants HTML |
| `regles.py` | Moteur de règles d'orientation des symptômes |
| `vaccins.py` | Calendrier vaccinal (données) et calcul des statuts |
| `contenu.py` | Chiffres sourcés, FAQ, texte de présentation du projet, sources |
| `prevention.py` | Conseils de prévention et avertissement |
| `test_sante.py` | 21 tests unitaires (règles, calendrier, contenus) |
| `requirements.txt` | Dépendances (Streamlit épinglé à 1.67.0 pour un rendu identique en ligne) |
| `.streamlit/config.toml` | Thème clair de l'application (le CSS reste lisible même sans ce fichier) |

## Identité visuelle

La palette vient du Faso Dan Fani, la cotonnade tissée en bandes : indigo profond, jaune mil,
rouge kola, blanc coton. Le « tissage » rayé est le seul motif décoratif. Les titres sont en
Bricolage Grotesque, le texte en Atkinson Hyperlegible (police pensée pour la lisibilité). Les
statuts ne reposent jamais sur la couleur seule : un mot ou un symbole l'accompagne toujours.

## Lisibilité

L'interface force un rendu clair, même si le téléphone ou l'ordinateur est en mode sombre :
libellés, menu, listes, cases, calendrier et graphique restent lisibles. La durée des signes
se choisit dans une liste (« 2 jours », « 1 à 2 semaines »…).

## Points de vigilance (à dire en soutenance)

- **Responsabilité** : aucun diagnostic, appel systématique à consulter, niveau le plus
  prudent en cas de doute.
- **Calendrier vaccinal** : les sources divergent sur les âges des trois contacts du
  nourrisson (8/12/16 semaines dans la thèse INSSA 2016 et les documents du PEV, 6/10/14
  semaines dans d'autres sources). Le calendrier est une simple liste de données dans
  `vaccins.py`, facile à ajuster. Les doses du vaccin antipaludique R21 sont marquées « à
  confirmer au centre de santé » car leur déploiement est progressif.
- **Vie privée** : aucune donnée personnelle n'est enregistrée.

## Pistes d'évolution

- Assistant IA optionnel pour reformuler les conseils en langage simple.
- Version en langues nationales (dioula, mooré).
- Annuaire des centres de santé par commune, rappels par SMS.

## Plan de soutenance (5 minutes)

1. Le problème (30 s) : paludisme, vaccins oubliés, savoir quand consulter.
2. La solution (30 s) : trois modules, en français, sur téléphone.
3. Démo en direct (2 min) : un enfant de 2 ans avec fièvre, puis un signe de danger, puis le
   carnet vaccinal d'un bébé de 5 mois.
4. Choix techniques (1 min) : règles écrites à la main et testées (21 tests), calendrier en
   données, déploiement gratuit.
5. Responsabilité et suite (1 min) : limites, validation par un professionnel de santé,
   langues locales.
