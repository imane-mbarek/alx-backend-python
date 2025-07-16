import sqlite3
import functools
from datetime import datetime

def log_queries(func):
    def wrapper(*args , **kwargs):
        # on récupère la requête passée à la fonction
        query = kwargs.get("query")
        
        # on affiche la requête
        print(f"{datetime.now()} - SQL Query: {query}")

        # on exécute la vraie fonction
        return func(*args , **kwargs)

    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
