import pandas as pd
import numpy as np

def transform_players(df):
    print("--- Transformation Players ---")
    initial = len(df)
    
    # 1. Doublons
    df = df.drop_duplicates(subset=['player_id'])
    
    # 2. Nettoyage pseudos
    df['username'] = df['username'].str.strip()
    
    # 3. Dates (Gère 'date_inconnue', '30-02-2024' -> NaT)
    # dayfirst=True aide pour le format 15/03/2023
    df['registration_date'] = pd.to_datetime(df['registration_date'], errors='coerce', dayfirst=True)
    
    # 4. Emails (Gère 'nightwolf' sans @ et les NaN)
    def clean_email(email):
        if pd.isna(email) or '@' not in str(email):
            return None
        return str(email)
    df['email'] = df['email'].apply(clean_email)
    
    # Remplacement des NaN par None pour MySQL
    df = df.where(pd.notnull(df), None)
    
    print(f"Joueurs : {initial} -> {len(df)}")
    return df

def transform_scores(df, valid_player_ids):
    print("--- Transformation Scores ---")
    initial = len(df)
    
    # 1. Doublons
    df = df.drop_duplicates(subset=['score_id'])
    
    # 2. Conversion numérique (Gère les NaN dans score)
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    df['duration_minutes'] = pd.to_numeric(df['duration_minutes'], errors='coerce')
    df['played_at'] = pd.to_datetime(df['played_at'], errors='coerce')
    
    # 3. Supprimer scores invalides (négatifs ou vides)
    df = df.dropna(subset=['score'])
    df = df[df['score'] >= 0]
    
    # 4. Supprimer orphelins (ID 99 par exemple)
    df = df[df['player_id'].isin(valid_player_ids)]
    
    # Remplacement des NaN restants par None
    df = df.where(pd.notnull(df), None)
    
    print(f"Scores : {initial} -> {len(df)}")
    return df