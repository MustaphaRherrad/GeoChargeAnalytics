# ⚡ GeoChargeAnalytics

**GeoChargeAnalytics** est un projet d'analyse géospatiale et statistique des infrastructures de recharge pour véhicules électriques (IRVE) en France. Ce projet a pour objectif de comprendre la répartition, la densité, l'accessibilité et les inégalités territoriales liées à l'électromobilité, à partir des données ouvertes disponibles.

---

## 🎯 Objectifs

- Étudier la répartition géographique des bornes de recharge sur le territoire français
- Identifier les zones bien et mal desservies (zones blanches)
- Analyser la diversité de l’offre (types de recharge, opérateurs, accessibilité)
- Fournir des visualisations interactives et des indicateurs pertinents pour orienter les politiques publiques ou les initiatives privées

---

## 🧠 Méthodologie

Le projet suit une approche rigoureuse en quatre grandes étapes :

1. **Préparation des données** : nettoyage, standardisation, enrichissement géographique
2. **Exploration statistique** : comptage, distributions, ratios par habitant et par km²
3. **Analyse géospatiale** : cartographies, clustering, détection de zones mal couvertes
4. **Restitution visuelle** : graphiques statiques et cartes interactives avec `folium`, `plotly`, `seaborn` et `matplotlib`

---

## 📦 Données

Ce projet s’appuie sur les données ouvertes relatives aux infrastructures de recharge pour véhicules électriques (IRVE) en France. Ces données sont fournies par le gouvernement français via le portail [data.gouv.fr](https://www.data.gouv.fr/fr/datasets/)🔗.

### 🗃️ Source principale
- **Jeu de données** : Bornes de recharge pour véhicules électriques - Données ouvertes
- **Fournisseur** : Ministère de la Transition écologique
- **Lien direct** : [https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/](https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/)🔗
- **Taille** : 82,1 Mo
- **Format** : CSV
- **Nombre de lignes**: 129065
- **Licence** : Licence Ouverte / Etalab 2.0

### 🧹 Pré-traitement des données
Avant l’analyse, les opérations suivantes ont été appliquées :
- Nettoyage des doublons et lignes vides
- Standardisation des formats (coordonnées, dates, noms de colonnes)
- Géocodage et enrichissement des données géographiques
- Formatage des puissances et des types de bornes

### 🧭 Champs principaux analysés
- **Localisation** : Commune, département, région, coordonnées GPS
- **Caractéristiques techniques** : puissance de recharge, type de prise, nombre de points de charge
- **Accessibilité** : horaires d’ouverture, accessibilité PMR, gratuité
- **Exploitant / Opérateur** : nom, statut, réseau

### Recoupement avec des données de l'INSEE pour la géolocalisation
Pour améliorer la contextualisation géographique et enrichir les métadonnées locales (comme le nom des communes), nous exploitons également un fichier de correspondance des communes fourni par l'INSEE :

- 🗂️ **Fichier INSEE :** `v_commune_2023.dbf` (format DBF, 6 Mo)
- 📍 Contenu : correspondances entre codes INSEE (`code_insee_commune`) et noms des communes (`nom_commune`), ainsi que des informations complémentaires sur les départements, cantons et régions.
- 🌐 Source officielle : [https://www.insee.fr/fr/information/6800675](https://www.insee.fr/fr/information/6800675)

Ce fichier est situé dans le dossier `./data/raw/` du projet, et est automatiquement fusionné avec les données IRVE dans le pipeline de traitement pour compléter les localisations manquantes dans les cartes régionales.

Malheureusement, le recoupement n'a pas été possible puisque la colonne du Code_ISEE pour les communes n'est pas suffisament renseignée dans le fichier de données des bornes.


### 📌 Mise à jour
Le jeu de données principal est régulièrement mis à jour sur data.gouv.fr. La version utilisée dans ce projet a été téléchargée le : **[08/06/2025]**.


### Qualité des Données et Traitement des Erreurs
[Document_principal_Data_Quality](docs/data_quality.md)

#### Problèmes identifiés
1. **Extraction du nom de la ville**

* **Cas particulier : adresse terminant par un chiffre**

 * Exemple :
 Parking Casino, 51269 Giffaumont Champaubert 1

 * Problème :
 Le chiffre final est considéré comme faisant partie du nom de la ville, ce qui conduit à une  extraction incorrecte (ex : Champaubert 1 au lieu de Giffaumont Champaubert).

 * Statut :
Non corrigé automatiquement (2 lignes concernées).

2. **Extraction du code postal**

* **Codes postaux incorrects ou incomplets**

 * Exemple :
 4240 SAINT-CHAMOND, 51 SUIPPES, 5& VERZY

 * Problème :
 Les codes postaux comportant moins de 5 chiffres ou des caractères non numériques ne sont pas extraits correctement.
 72 lignes concernées : la colonne code_postal reste alors vide pour ces adresses.

 * Statut :
 Non corrigé automatiquement.

#### Actions réalisées
* Suppression des codes d’autoroute dans l’adresse avant extraction.

* Suppression des codes postaux dupliqués.

* Extraction robuste du nom de la ville (gestion des apostrophes, tirets, abréviations courantes).

* Extraction du code postal uniquement si celui-ci est valide (5 chiffres).

* Extraction du nom de la ville à partir du dernier mot/groupe de l’adresse en cas d’absence de code postal valide (méthode de repli).

#### Perspectives
* Pour les adresses terminant par un chiffre :

 * Une solution manuelle ou une règle spécifique pourrait être ajoutée pour ignorer les chiffres finaux lors de l’extraction du nom de la ville.

* Pour les codes postaux incorrects :

 * Une vérification manuelle ou une correction automatisée (si possible) pourrait être envisagée pour les cas restants.


---

## 🛠️ Stack technique

- **Langage principal** : Python 3.10+
- **Analyse de données** : `pandas`, `numpy`, `scikit-learn`
- **Visualisation** : `matplotlib`, `seaborn`, `plotly`, `folium`
- **Traitement géospatial** : `geopandas`, `shapely`
- **Cartes interactives** : `folium`, `geopandas`, `plotly.express`
- **Notebooks Jupyter** pour les explorations pas à pas

---

## 📊 Résultats attendus

- Statistiques par commune, département et région
- Carte de chaleur de la couverture nationale
- Classement des zones les plus et les moins équipées
- Visualisations du lien entre densité de population et densité de bornes
- Tableau comparatif des opérateurs selon leur part de marché
- Visualisations interactives accessibles via notebooks ou déploiement (optionnel)

---

## 🔄 Reproductibilité

Pour exécuter ce projet sur mon laptop :

```bash
git clone https://github.com/MustaphaRherrad/GeoChargeAnalytics.git
cd GeoChargeAnalytics
pip install -r requirements.txt
jupyter notebook
```
---
## 🗺️ Cartes interactives

- 🔗 [Carte nationale](https://iana-data.org/html_pages/map.html) La carte nationale comporte plus de 129.000 données ce qui va ralentir relativement son chargement en fonction de votre débit internet. Je vous incite à patienter jusqu'à sa mise en cache. Ainsi vous pourrez visualiser sur la carte de France tous les emplacements des bornes de charge se trouvant sur le territoire nationale.
- 🗼 [Carte de chaleur - Paris](https://MustaphaRherrad.github.io/GeoChargeAnalytics/heatmap_paris.html)
- 🦁 [Carte de chaleur - Lyon](https://MustaphaRherrad.github.io/GeoChargeAnalytics/heatmap_lyon.html)
- 🌊 [Carte de chaleur - Marseille](https://MustaphaRherrad.github.io/GeoChargeAnalytics/heatmap_marseille.html)
- 🍷 [Carte de chaleur - Bordeaux](https://MustaphaRherrad.github.io/GeoChargeAnalytics/heatmap_bordeaux.html)
- 🏙️ [Carte de chaleur - Île-de-France](https://MustaphaRherrad.github.io/GeoChargeAnalytics/heatmap_idf.html)

---

## 🔄 Exécution sur machine locale

La **procédure étape par étape** pour exécuter correctement le projet **GeoChargeAnalytics** localement :

---

### ✅ Étape 1 : Créer un environnement virtuel (optionnel mais recommandé)

Dans le terminal, à la racine du projet :

```bash
python -m venv venv
source venv/bin/activate  # Sur macOS/Linux
venv\Scripts\activate     # Sur Windows
```

---

### ✅ Étape 2 : Installer les dépendances

Crée un fichier `requirements.txt` avec au minimum :

```
pandas
folium
```

Puis installe-les :

```bash
pip install -r requirements.txt
```

(Si tu utilises aussi `matplotlib`, `seaborn`, ou `plotly`, ajoute-les à `requirements.txt`.)

---

### ✅ Étape 3 : Vérifie que les modules sont bien présents

le dossier `geocharge/` doit contenir :

* `__init__.py`
* `preprocessing.py`
* `analysis.py`
* `visualization.py`

Et dans la racine, il faut avoir :

* `main.py`
* le dossier `data/` avec le fichier `irve.csv`

---

### ✅ Étape 4 : Lancer le programme principal

Dans le terminal :

```bash
python main.py
```

👉 Cela doit :

* charger et nettoyer le fichier CSV `irve.csv`,
* générer des statistiques,
* créer une carte interactive `output/carte_interactive.html`.

---

### 🧪 Étape 5 : Tester et explorer

* Ouvre le fichier `output/carte_interactive.html` dans le navigateur pour voir la carte.
* on peux ajouter un `print(stats)` dans `main.py` pour vérifier les sorties de `compute_stats()`.

---

### ❗ Conseils si erreur :

* Si jamais on obtient une erreur du type `ModuleNotFoundError`, on doit vérifie que  la commande **depuis la racine** du projet est bien executée.
* Si le CSV ne se charge pas, on vérifie que son nom exact est bien `irve.csv` (casse comprise).

---


