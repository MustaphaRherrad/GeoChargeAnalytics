import pandas as pd
import ast

def load_data(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)


def split_coordinates(df):
    def parse_coords(val):
        if isinstance(val, list) and len(val) == 2:
            return val
        if isinstance(val, str):
            try:
                result = ast.literal_eval(val)
                if isinstance(result, list) and len(result) == 2:
                    return result
            except Exception:
                return None
        return None

    # Application du parsing
    coords_parsed = df['coordonneesXY'].apply(parse_coords)

    # Création d'un DataFrame à 2 colonnes
    coords_df = coords_parsed.dropna().apply(pd.Series)
    coords_df.columns = ['longitude', 'latitude'] 

    # Ne garder que les lignes valides (même index que coords_df)
    df_clean = df.loc[coords_df.index].copy()
    df_clean['latitude'] = coords_df['latitude']
    df_clean['longitude'] = coords_df['longitude']

    return df_clean


def clean_data(df):
    df = split_coordinates(df)
    df = df.dropna(subset=['latitude', 'longitude'])
    return df
