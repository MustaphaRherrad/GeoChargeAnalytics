# Notebooks

# Scripts d'exploration pour identifier les données manquantes

Je vais utiliser des scripts  qui vont m'aider à explorer pourquoi certaines données ne s'affichent pas sur les cartes secondaires.

* 1. Script d'analyse des données manquantes
* 2. Script de vérification des villes non reconnues
* 3. Script de validation des coordonnées
* 4. Script de comparaison entre données attendues et affichées
* 5. Script d'exploration des données par région


Ces scripts vont m'aider à identifier:
1. Les données manquantes ou incomplètes
2. Les problèmes de normalisation des villes
3. Les coordonnées géographiques invalides
4. Les divergences entre les données attendues et affichées
5. Les problèmes spécifiques à chaque région

# Premieres actions d'amélioration

D'après les résultats des scripts, voici les problèmes identifiés et les pistes d'amélioration correspondantes :

### 1. Problème des coordonnées invalides
**Constats :**
- 513 stations avec latitude suspecte
- 553 stations avec longitude suspecte
- Exemple : Station "SAINT CLEMENT DE RIVIERE" avec longitude 4.649609 (ce qui correspondrait à l'Afrique, pas à la France)

**Pistes d'amélioration :**

**a. Corriger la fonction `parse_coords` dans preprocessing.py :**
```python
def parse_coords(val):
    """Parse les coordonnées au format liste en vérifiant leur validité pour la France."""
    if isinstance(val, str):
        try:
            result = ast.literal_eval(val)
            if isinstance(result, list) and len(result) == 2:
                # Vérification que les coordonnées sont plausibles pour la France
                lat, lon = result
                if (42 <= lat <= 51) and (-5 <= lon <= 9):  # Plage France métropolitaine
                    return [lat, lon]
                else:
                    print(f"Coordonnées hors de France: {result}")
                    return None
        except Exception:
            pass
    return None
```

**b. Ajouter une fonction de correction des coordonnées inversées :**
```python
def correct_inverted_coords(df):
    """Corrige les cas où longitude et latitude sont inversées."""
    mask = (df['longitude'].abs() > 90) | (df['latitude'].abs() > 180)
    df.loc[mask, ['latitude', 'longitude']] = df.loc[mask, ['longitude', 'latitude']].values
    return df
```

**c. Implémenter une validation post-chargement :**
```python
def validate_french_coordinates(df):
    """Marque les coordonnées invalides pour la France."""
    df['coord_valide'] = df['latitude'].between(41, 52) & df['longitude'].between(-5, 10)
    invalid_coords = df[~df['coord_valide']]
    if not invalid_coords.empty:
        print(f"Attention: {len(invalid_coords)} coordonnées invalides détectées")
    return df
```

### 2. Pour les adresses (même si 0 non reconnues)
**Amélioration proactive :**

**a. Améliorer la robustesse de `normalize_city_name` :**
```python
def normalize_city_name(adresse: str) -> str:
    """Version améliorée avec gestion des cas particuliers."""
    if pd.isna(adresse):
        return None
        
    adresse = adresse.upper().strip()
    
    # Cas des DOM-TOM (à adapter selon les besoins)
    dom_tom_codes = {
        '971': 'GUADELOUPE', '972': 'MARTINIQUE', 
        '973': 'GUYANE', '974': 'LA REUNION', '976': 'MAYOTTE'
    }
    
    # Extraction code postal
    cp_match = re.search(r'(\d{5})', adresse)
    if cp_match:
        cp = cp_match.group(1)
        # Vérification DOM-TOM
        if cp[:3] in dom_tom_codes:
            return dom_tom_codes[cp[:3]]
    
    # ... (le reste de la fonction existante)
```

### 3. Mise en œuvre recommandée

Dans votre `main.py`, ajoutez ces étapes :

```python
def main():
    df = load_data("data/raw/consolidation-etalab-schema-irve-statique-v-2.3.1-20250608.csv")
    df = clean_data(df)
    
    # Nouvelles étapes
    df = correct_inverted_coords(df)
    df = validate_french_coordinates(df)
    
    # Traitement des coordonnées invalides (au choix)
    # Option 1: Suppression
    df = df[df['coord_valide']]
    
    # Option 2: Correction manuelle pour les cas connus
    # df.loc[df['nom_station'] == 'SAINT CLEMENT DE RIVIERE', ['latitude', 'longitude']] = [43.683, 3.833]
    
    # Suite du traitement...
```

### 4. Pour aller plus loin

**a. Créer un rapport des anomalies :**
```python
def generate_anomaly_report(df, output_file="reports/coordinate_anomalies.csv"):
    anomalies = df[~df['coord_valide']]
    if not anomalies.empty:
        anomalies[['nom_station', 'adresse_station', 'latitude', 'longitude']]\
            .to_csv(output_file, index=False)
        print(f"Rapport des anomalies généré: {output_file}")
```

**b. Visualisation des anomalies :**
```python
def plot_anomalies(df):
    plt.figure(figsize=(12, 6))
    plt.scatter(df['longitude'], df['latitude'], c='blue', alpha=0.5, label='Valides')
    anomalies = df[~df['coord_valide']]
    if not anomalies.empty:
        plt.scatter(anomalies['longitude'], anomalies['latitude'], c='red', label='Anomalies')
    plt.title('Carte des stations avec anomalies de coordonnées')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.legend()
    plt.grid()
    plt.show()
```

Ces améliorations devraient résoudre :
1. Le problème des coordonnées manifestement erronées
2. La robustesse face aux données des DOM-TOM
3. Fournir un meilleur reporting des problèmes

Pour le cas spécifique de "SAINT CLEMENT DE RIVIERE", les coordonnées correctes devraient être environ [43.683, 3.833] (Hérault), ce qui suggère soit :
- Une inversion longitude/latitude
- Une erreur de saisie dans les données sources

