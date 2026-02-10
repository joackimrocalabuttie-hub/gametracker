import mysql.connector
import time
import os
from contextlib import contextmanager

# Configuration
DB_HOST = os.getenv("DB_HOST", "db")
DB_USER = os.getenv("DB_USER", "root")
DB_PASSWORD = os.getenv("DB_PASSWORD", "root")
DB_NAME = os.getenv("DB_NAME", "gametracker")

def get_connection():
    """Tente une connexion unique."""
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error:
        return None

def get_connection_with_retry(max_retries=20, delay=3):
    """Insiste LOURDEMENT jusqu'à ce que la base réponde."""
    for attempt in range(max_retries):
        conn = get_connection()
        if conn is not None:
            print(f"✅ Connexion réussie à la tentative {attempt+1} !")
            return conn
        print(f"⏳ La BDD n'est pas encore prête... (Tentative {attempt+1}/{max_retries})")
        time.sleep(delay)
    raise Exception("❌ ABANDON : Impossible de se connecter après plusieurs essais.")

@contextmanager
def database_connection():
    """Context manager intelligent qui attend la base."""
    # ICI : On utilise la version avec retry pour ne jamais échouer au démarrage
    conn = get_connection_with_retry()
    if conn is None:
        raise Exception("Impossible d'obtenir une connexion stable")
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()