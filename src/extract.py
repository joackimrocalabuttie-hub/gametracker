import pandas as pd
import os

def extract(filepath):
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Fichier introuvable: {filepath}")
    return pd.read_csv(filepath)