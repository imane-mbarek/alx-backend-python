import time 
import sqlite3
import functools


def retry_on_failure(retries=3 ,delay=2):
    def decorator(func):
        def wrapper(*args,**kwargs):
            for attemp in range(retries):
                try:  return func(*args,**kwargs)
                except Exception as e:
                       print("Attempt {attempt +1} failled {e}")
                       time.sleep(delay)
            # après les tentatives, on relance l'erreur
            raise Exception("Function failed after {retries} retries")
        return wrapper
    return decorator



@with_db_connection
@retry_on_failure(retries=3, delay=1)

def fetch_users_with_retry(conn):
cursor = conn.cursor()
cursor.execute("SELECT * FROM users")
return cursor.fetchall()

#### attempt to fetch users with automatic retry on failure

users = fetch_users_with_retry()
print(users)
