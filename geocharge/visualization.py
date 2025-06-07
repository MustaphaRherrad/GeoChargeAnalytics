import folium

def generate_map(df, output_file='docs/map.html'):
    m = folium.Map(location=[46.5, 2.5], zoom_start=6)
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=3,  # Taille réduite
            color='blue',
            fill=True,
            fill_color='blue',
            fill_opacity=0.5,
            popup=row.get('nom_amenageur', 'Inconnu')
        ).add_to(m)
    m.save(output_file)
