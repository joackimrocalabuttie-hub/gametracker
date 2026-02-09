from src.extract import extract
from src.transform import transform_players, transform_scores
from src.load import load_players, load_scores
from src.report import generate_report
from src.database import database_connection

def main():
    try:
        # 1. Extraction
        df_players = extract("data/raw/Players.csv")
        df_scores = extract("data/raw/Scores.csv")
        
        # 2. Transformation
        df_players_clean = transform_players(df_players)
        valid_ids = df_players_clean['player_id'].unique().tolist()
        df_scores_clean = transform_scores(df_scores, valid_ids)
        
        # 3. Chargement
        with database_connection() as conn:
            load_players(df_players_clean, conn)
            load_scores(df_scores_clean, conn)
            
        # 4. Rapport
        generate_report()
        print("Succès !")
        
    except Exception as e:
        print(f"Erreur: {e}")
        exit(1)

if __name__ == "__main__":
    main()