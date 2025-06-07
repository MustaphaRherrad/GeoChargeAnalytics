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
- **Lien direct** : [https://www.data.gouv.fr/fr/datasets/infrastructures-de-recharge-pour-vehicules-electriques-irve/](https://www.data.gouv.fr/fr/datasets/infrastructures-de-recharge-pour-vehicules-electriques-irve/)🔗
- **Format** : CSV (compressé au format ZIP)
- **Licence** : Licence Ouverte / Etalab 2.0

### 🧹 Pré-traitement des données
Avant l’analyse, les opérations suivantes ont été appliquées :
- Nettoyage des doublons et lignes vides
- Standardisation des formats (coordonnées, dates, noms de colonnes)
- Suppression du dossier `_MACOSX` et des fichiers systèmes inutiles
- Géocodage et enrichissement des données géographiques
- Formatage des puissances et des types de bornes

### 🧭 Champs principaux analysés
- **Localisation** : Commune, département, région, coordonnées GPS
- **Caractéristiques techniques** : puissance de recharge, type de prise, nombre de points de charge
- **Accessibilité** : horaires d’ouverture, accessibilité PMR, gratuité
- **Exploitant / Opérateur** : nom, statut, réseau

### 📌 Mise à jour
Le jeu de données est régulièrement mis à jour sur data.gouv.fr. La version utilisée dans ce projet a été téléchargée le : **[06/06/2025]**.

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
## 📍 Cartes interactives

- 🔗 [Carte nationale](https://MustaphaRherrad.github.io/GeoChargeAnalytics/map.html)
- 🗼 [Carte Paris](https://MustaphaRherrad.github.io/GeoChargeAnalytics/map_paris.html)
- 🦁 [Carte Lyon](https://MustaphaRherrad.github.io/GeoChargeAnalytics/map_lyon.html)
- 🍷 [Carte Bordeaux](https://MustaphaRherrad.github.io/GeoChargeAnalytics/map_bordeaux.html)

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

Et dans la racine, il fauts avoir :

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


