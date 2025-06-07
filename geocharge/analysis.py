# geocharge/analysis.py

import folium
import pandas as pd

def count_stations(df: pd.DataFrame) -> int:
    """Compte le nombre unique de stations."""
    return df['nom_station'].nunique()

def generate_map(df: pd.DataFrame, output_file='map.html') -> None:
    """Génère une carte classique avec des marqueurs."""
    m = folium.Map(location=[46.5, 2.5], zoom_start=6)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row.get('nom_amenageur', 'Inconnu')
        ).add_to(m)
    m.save(output_file)
