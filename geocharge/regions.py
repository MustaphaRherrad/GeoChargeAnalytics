# geocharge/regions.py

import pandas as pd

# Constantes de regroupement par zones géographiques
VILLE_DEPARTEMENTS = {
    'paris': ['75'],
    'lyon': ['69'],
    'marseille': ['13'],
    'bordeaux': ['33'],
    'idf': ['75', '77', '78', '91', '92', '93', '94', '95'],
    'autoroutes': None  # Cas spécial
}

CENTROIDS = {
    'paris': [48.8566, 2.3522],
    'lyon': [45.75, 4.85],
    'marseille': [43.3, 5.4],
    'bordeaux': [44.84, -0.58],
    'idf': [48.8, 2.4],
    'autoroutes': [46.5, 2.5]  # Centre géographique pour visualisation
}

def extract_departement(df: pd.DataFrame) -> pd.DataFrame:
    """Ajoute les colonnes code_postal et departement à partir de l’adresse."""
    df = df.copy()
    df['code_postal'] = df['adresse_station'].str.extract(r'(\d{5})')
    df['departement'] = df['code_postal'].str[:2]
    return df

def filter_by_ville(df: pd.DataFrame, ville: str) -> pd.DataFrame:
    """Filtre le DataFrame selon une ville ou les autoroutes."""
    if ville.lower() == 'autoroutes':
        return df[df['autoroute'].notna()].copy()
    deps = VILLE_DEPARTEMENTS.get(ville.lower())
    return df[df['departement'].isin(deps)].copy() if deps else pd.DataFrame()
