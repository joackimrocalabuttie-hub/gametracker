from database import get_connection
import datetime

def generate_report():
    print("Génération du rapport...")
    conn = get_connection()
    if not conn:
        print("Erreur: Impossible de se connecter à la base pour le rapport.")
        return

    try:
        cursor = conn.cursor()
        
        # 1. Statistiques générales
        cursor.execute("SELECT COUNT(*) FROM players")
        nb_players = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM scores")
        nb_scores = cursor.fetchone()[0]

        # REQUIS: Nombre de jeux différents
        cursor.execute("SELECT COUNT(DISTINCT game) FROM scores")
        nb_games = cursor.fetchone()[0]

        # 2. Top 5 des meilleurs scores
        cursor.execute("""
            SELECT p.username, s.game, s.score 
            FROM scores s 
            JOIN players p ON s.player_id = p.player_id 
            ORDER BY s.score DESC 
            LIMIT 5
        """)
        top_scores = cursor.fetchall()

        # 3. REQUIS: Score moyen par jeu
        cursor.execute("SELECT game, AVG(score) FROM scores GROUP BY game")
        avg_scores = cursor.fetchall()

        # 4. REQUIS: Répartition des joueurs par pays
        cursor.execute("SELECT country, COUNT(*) FROM players GROUP BY country ORDER BY COUNT(*) DESC")
        players_by_country = cursor.fetchall()

        # 5. Répartition par plateforme
        cursor.execute("SELECT platform, COUNT(*) FROM scores GROUP BY platform")
        platforms = cursor.fetchall()

        # Écriture du rapport
        with open("/app/output/rapport.txt", "w", encoding='utf-8') as f:
            f.write("=== RAPPORT GAMETRACKER ===\n")
            f.write(f"Généré le : {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            f.write("--- STATISTIQUES GENERALES ---\n")
            f.write(f"Nombre de joueurs : {nb_players}\n")
            f.write(f"Nombre de scores  : {nb_scores}\n")
            f.write(f"Nombre de jeux    : {nb_games}\n\n")

            f.write("--- TOP 5 SCORES ---\n")
            for player, game, score in top_scores:
                f.write(f"- {player} sur {game} : {score}\n")
            f.write("\n")

            f.write("--- SCORE MOYEN PAR JEU ---\n")
            for game, avg in avg_scores:
                f.write(f"- {game} : {avg:.2f}\n")
            f.write("\n")

            f.write("--- JOUEURS PAR PAYS ---\n")
            for country, count in players_by_country:
                f.write(f"- {country} : {count}\n")
            f.write("\n")

            f.write("--- PAR PLATEFORME ---\n")
            for platform, count in platforms:
                f.write(f"- {platform} : {count}\n")
            
        print("Rapport généré avec succès dans output/rapport.txt")

    except Exception as e:
        print(f"Erreur lors de la génération du rapport: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    generate_report()