# geocharge/visualization.py

import folium
from folium.plugins import HeatMap
import pandas as pd

def generate_map(df: pd.DataFrame, output_file='docs/map.html') -> None:
    """Carte interactive avec cercles bleus pour chaque station."""
    m = folium.Map(location=[46.5, 2.5], zoom_start=6)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            popup=row.get('nom_amenageur', 'Inconnu')
        ).add_to(m)
    m.save(output_file)

def generate_heatmap(df: pd.DataFrame, center: list, output_file: str,
                     radius: int = 15, blur: int = 20) -> None:
    """Génère une carte de chaleur avec des paramètres personnalisés."""
    zoom = 12 if 'autoroute' not in df.columns else 8
    m = folium.Map(location=center, zoom_start=zoom)

    if 'autoroute' in df.columns and df['autoroute'].notna().any():
        for autoroute, group in df.groupby('autoroute'):
            HeatMap(
                group[['latitude', 'longitude']].values,
                name=f"Autoroute {autoroute}",
                radius=10,
                blur=15
            ).add_to(m)
    else:
        HeatMap(
            df[['latitude', 'longitude']].values,
            radius=radius,
            blur=blur
        ).add_to(m)

    folium.LayerControl().add_to(m)
    m.save(output_file)
