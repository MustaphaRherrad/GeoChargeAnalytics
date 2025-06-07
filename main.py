from geocharge.preprocessing import load_data, clean_data
from geocharge.analysis import count_stations
from geocharge.visualization import generate_map, generate_heatmap
from geocharge.regions import extract_departement, filter_by_ville, CENTROIDS

def main():
    df = load_data("C:/Code/Projets_perso/projets/GeoChargeAnalytics/data/raw/1-irve-statique.csv")
    df = clean_data(df)
    df = extract_departement(df)  # <== très très important pour filtrer

    villes = ['paris', 'lyon', 'marseille', 'bordeaux', 'idf']
    for ville in villes:
        df_ville = filter_by_ville(df, ville)
        center = CENTROIDS[ville]
        output_file = f'docs/heatmap_{ville}.html'
        generate_heatmap(df_ville, center=center, output_file=output_file)
        print(f"Carte de chaleur pour {ville} générée : {output_file}")

    # Optionnel : carte globale classique
    generate_map(df)

if __name__ == "__main__":
    main()
