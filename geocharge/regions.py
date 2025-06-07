# geocharge/regions.py

import pandas as pd

VILLE_DEPARTEMENTS = {
    'paris': ['75'],
    'lyon': ['69'],
    'marseille': ['13'],
    'bordeaux': ['33'],
    'idf': ['75', '77', '78', '91', '92', '93', '94', '95']
}

CENTROIDS = {
    'paris': [48.8566, 2.3522],
    'lyon': [45.75, 4.85],
    'marseille': [43.3, 5.4],
    'bordeaux': [44.84, -0.58],
    'idf': [48.8, 2.4]
}

def extract_departement(df):
    df['code_postal'] = df['adresse_station'].str.extract(r'(\d{5})')
    df['departement'] = df['code_postal'].str[:2]
    return df

def filter_by_ville(df, ville):
    deps = VILLE_DEPARTEMENTS.get(ville.lower(), [])
    return df[df['departement'].isin(deps)].copy()
