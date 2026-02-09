from src.database import database_connection
from datetime import datetime

def generate_report():
    print("Génération du rapport...")
    with database_connection() as conn:
        cursor = conn.cursor()
        
        # Requêtes statistiques
        cursor.execute("SELECT COUNT(*) FROM players")
        nb_players = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scores")
        nb_scores = cursor.fetchone()[0]
        
        cursor.execute("""
            SELECT p.username, s.game, s.score 
            FROM scores s JOIN players p ON s.player_id = p.player_id 
            ORDER BY s.score DESC LIMIT 5
        """)
        top_5 = cursor.fetchall()
        
        cursor.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform")
        platforms = cursor.fetchall()

    with open("output/rapport.txt", "w") as f:
        f.write("=== RAPPORT GAMETRACKER ===\n")
        f.write(f"Date: {datetime.now()}\n\n")
        f.write(f"Joueurs total: {nb_players}\n")
        f.write(f"Scores total: {nb_scores}\n\n")
        f.write("TOP 5 SCORES:\n")
        for p, g, s in top_5:
            f.write(f"- {p} sur {g}: {s}\n")
        f.write("\nPAR PLATEFORME:\n")
        for plat, count in platforms:
            f.write(f"- {plat}: {count}\n")