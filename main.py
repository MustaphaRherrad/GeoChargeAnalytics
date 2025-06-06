from geocharge.preprocessing import load_data, clean_data
from geocharge.analysis import count_stations
from geocharge.visualization import generate_map

def main():
    df = load_data("C:/Code/Projets_perso/projets/GeoChargeAnalytics/data/raw/1-irve-statique.csv")
    df = clean_data(df)
    stats = count_stations(df)
    print(df.head())

    generate_map(df)

if __name__ == "__main__":
    main()
