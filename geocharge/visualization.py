import folium

def generate_map(df, output_file='map.html'):
    m = folium.Map(location=[46.5, 2.5], zoom_start=6)
    for _, row in df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row.get('nom_amenageur', 'Inconnu')
        ).add_to(m)
    m.save(output_file)
