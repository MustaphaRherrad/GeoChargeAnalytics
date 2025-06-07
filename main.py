# main.py

from geocharge.preprocessing import load_data, clean_data
from geocharge.analysis import count_stations
from geocharge.visualization import generate_map, generate_heatmap
from geocharge.regions import extract_departement, filter_by_ville, CENTROIDS

def main():
    # Chargement et nettoyage des données
    df = load_data("data/raw/1-irve-statique.csv")
    df = clean_data(df)
    df = extract_departement(df)

    # Analyse par zones urbaines
    villes = ['paris', 'lyon', 'marseille', 'bordeaux', 'idf']
    for ville in villes:
        df_ville = filter_by_ville(df, ville)
        if df_ville.empty:
            continue
        generate_heatmap(
            df_ville,
            center=CENTROIDS[ville],
            output_file=f'docs/heatmap_{ville}.html',
            radius=12 if ville in ['paris', 'lyon'] else 8
        )

    # Analyse pour les stations sur autoroutes
    df_autoroutes = filter_by_ville(df, 'autoroutes')
    if not df_autoroutes.empty:
        generate_heatmap(
            df_autoroutes,
            center=CENTROIDS['autoroutes'],
            output_file='docs/heatmap_autoroutes.html',
            radius=10
        )

    # Carte globale
    generate_map(df)

if __name__ == "__main__":
    main()