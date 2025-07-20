import time
import sqlite3
import functools


def with_db_connection(func)
    def wrapper(*args , **kwargs):
        conn=sqlite3.connect('users.db')
        try:  return func(conn,*args,**kwargs)
        finally conn.close()
    return wrapper


def cache_query(func):
        def wrapper(*args , **kwargs):
            if query query_cache:
               print("Using cached result")
               return query_cache[query]
            print("Executing and caching result")
            result= func(conn , query, *args , **kwargs)
            query_cache[query]=result
            return result 
        return wrapper



@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

