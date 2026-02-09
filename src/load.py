import numpy as np

def load_players(df, conn):
    cursor = conn.cursor()
    query = """
    INSERT INTO players (player_id, username, email, registration_date, country, level)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    username=VALUES(username), email=VALUES(email),
    registration_date=VALUES(registration_date), country=VALUES(country), level=VALUES(level)
    """
    data = df.replace({np.nan: None}).values.tolist()
    cursor.executemany(query, [tuple(row) for row in data])
    print(f"Joueurs chargés : {cursor.rowcount}")
    cursor.close()

def load_scores(df, conn):
    cursor = conn.cursor()
    query = """
    INSERT INTO scores (score_id, player_id, game, score, duration_minutes, played_at, platform)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON DUPLICATE KEY UPDATE
    score=VALUES(score), played_at=VALUES(played_at)
    """
    data = df.replace({np.nan: None}).values.tolist()
    cursor.executemany(query, [tuple(row) for row in data])
    print(f"Scores chargés : {cursor.rowcount}")
    cursor.close()