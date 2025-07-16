import sqlite3
import functools


def with_db_connection(func):
    def wrapper(*args ,**kwargs):
        connection = sqlite3.connect('users_db')
       try:
          return func(connection , *args , **kwargs)
       finally:
          connection.close()
    return wrapper 

@with_db_connection 
def get_user_by_id(conn, user_id): 
cursor = conn.cursor() 
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,)) 
return cursor.fetchone() 
#### Fetch user by ID with automatic connection handling 

user = get_user_by_id(user_id=1)
print(user)

