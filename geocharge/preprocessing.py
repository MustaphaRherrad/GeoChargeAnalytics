import pandas as pd
import ast
import re

def load_data(filepath: str) -> pd.DataFrame:
    """Charge les données depuis un fichier CSV."""
    return pd.read_csv(filepath)

def parse_coords(val):
    """Parse les coordonnées au format liste."""
    if isinstance(val, str):
        try:
            result = ast.literal_eval(val)
            if isinstance(result, list) and len(result) == 2:
                return result
        except Exception:
            pass
    return None

def split_coordinates(df: pd.DataFrame) -> pd.DataFrame:
    """Sépare les coordonnées en latitude et longitude."""
    coords = df['coordonneesXY'].apply(parse_coords).dropna()
    coords_df = pd.DataFrame(coords.tolist(), index=coords.index, columns=['longitude', 'latitude'])
    df_clean = df.loc[coords_df.index].copy()
    df_clean[['latitude', 'longitude']] = coords_df[['latitude', 'longitude']]
    return df_clean

def normalize_city_name(adresse: str) -> str:
    """Normalise le nom de la ville à partir de l'adresse."""
    if pd.isna(adresse):
        return None
    adresse = adresse.upper()
    # Cas spéciaux Paris/Lyon
    if re.search(r'750\d{2}\s+PARIS', adresse):
        return 'PARIS'
    if re.search(r'690\d{2}\s+LYON', adresse):
        return 'LYON'
    # Supprime les codes d'autoroute
    adresse = re.sub(r'\b(A\d+|RN\d+)\b', '', adresse)
    # Supprime les codes postaux dupliqués
    adresse = re.sub(r'(\d{5})\s+\1', r'\1', adresse)
    # Nettoie les espaces
    adresse = re.sub(r'\s+', ' ', adresse.strip())
    # Extrait code postal + ville (gère apostrophes, tirets, etc.)
    match = re.search(r'.*\b(\d{5})\s+([A-ZÀ-ÿ\'\- ]+)$', adresse)
    if match:
        ville = match.group(2).strip()
        # Normalise les abréviations courantes
        ville = re.sub(r"\bST\b", "SAINT", ville)
        ville = re.sub(r"\bSTE\b", "SAINTE", ville)
        ville = ville.title()
        return ville
    # Si pas de code postal valide, essaie d'extraire le dernier mot/groupe
    else:
        mots = [m.strip() for m in re.split(r'[,\s]+', adresse) if m.strip()]
        if mots:
            ville = mots[-1].upper()
            ville = re.sub(r"\bST\b", "SAINT", ville)
            ville = re.sub(r"\bSTE\b", "SAINTE", ville)
            ville = ville.title()
            return ville
    return None

def extract_highway_info(adresse: str) -> str:
    """Extrait les informations d'autoroute."""
    match = re.search(r'(A\d+|RN\d+)', adresse.upper())
    return match.group(1) if match else None

def extract_ville_code_postal(df: pd.DataFrame) -> pd.DataFrame:
    """Extrait code postal et ville."""
    # Extraction code postal
    df['code_postal'] = df['adresse_station'].str.extract(r'(\d{5})')[0]
    # Extraction ville normalisée (on utilise la nouvelle version robuste)
    df['ville'] = df['adresse_station'].apply(normalize_city_name)
    return df

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Nettoie et prépare les données."""
    df = split_coordinates(df)  # Sépare les coordonnées et ne garde que les lignes valides
    df['ville_normalisee'] = df['adresse_station'].apply(normalize_city_name)
    df['autoroute'] = df['adresse_station'].apply(extract_highway_info)
    df = extract_ville_code_postal(df)
    df.dropna(subset=['latitude', 'longitude'], inplace=True)
    return df

import re
import pandas as pd

def normalize_ville_adresse(adresse: str) -> str:
    """Extrait et normalise le nom de la ville à partir d'une adresse IRVE."""
    if pd.isna(adresse):
        return None
    # 1. Supprime les codes d'autoroute (Axx, RNxx)
    adresse = re.sub(r'\b(A\d+|RN\d+)\b', '', adresse, flags=re.IGNORECASE)
    # 2. Supprime les codes postaux dupliqués (ex: 19600 19600)
    adresse = re.sub(r'(\d{5})\s+\1', r'\1', adresse)
    # 3. Nettoie les espaces et virgules
    adresse = re.sub(r'\s+', ' ', adresse.strip())
    # 4. Extrait code postal + ville (gère apostrophes, tirets, etc.)
    match = re.search(r'(\d{5})\s+([A-ZÀ-ÿ\'\- ]+)$', adresse.upper())
    if match:
        ville = match.group(2).strip()
        # Normalise les abréviations courantes
        ville = re.sub(r"\bST\b", "SAINT", ville)
        ville = re.sub(r"\bSTE\b", "SAINTE", ville)
        ville = ville.title()
        return ville
    # 5. Si pas de code postal valide, essaie d'extraire le dernier mot/groupe
    else:
        # Découpe selon virgules ou espaces, prend le dernier élément non vide
        mots = [m.strip() for m in re.split(r'[, ]+', adresse) if m.strip()]
        if mots:
            # On prend le dernier mot, en upper puis title
            ville = mots[-1].upper()
            ville = re.sub(r"\bST\b", "SAINT", ville)
            ville = re.sub(r"\bSTE\b", "SAINTE", ville)
            ville = ville.title()
            return ville
    return None

def extract_code_postal_et_ville(df: pd.DataFrame, col_adresse='adresse_station') -> pd.DataFrame:
    """Ajoute les colonnes code_postal et ville_normalisee."""
    df = df.copy()
    # Extraction code postal
    df['code_postal'] = df[col_adresse].str.extract(r'(\d{5})')[0]
    # Extraction ville normalisée
    df['ville_normalisee'] = df[col_adresse].apply(normalize_ville_adresse)
    return df

# Exemple d'utilisation :
# df = pd.read_csv('data/irve.csv')
# df = extract_code_postal_et_ville(df)
# print(df[['adresse_station', 'code_postal', 'ville_normalisee']].head())
