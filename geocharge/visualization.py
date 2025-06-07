# geocharge/visualization.py

import folium
from folium.plugins import HeatMap

def generate_map(df, output_file='docs/map.html'):
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

def generate_heatmap(df, center, output_file):
    m = folium.Map(location=center, zoom_start=11)
    heat_data = df[['latitude', 'longitude']].dropna().values.tolist()
    HeatMap(heat_data, radius=8, blur=15).add_to(m)
    m.save(output_file)
