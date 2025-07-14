import mysql.connector

#pour se connecter au serveur MYSQL
def connect_db():
       connection= mysql.connector.connect(
        host="localhost",
        user="root",
        password="password"
        )
    return connection


#créer une base de donnée si elle n'existe pas 
def create_database(connection):
    cursor = connection.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
    connection.commit()
    cursor.close()

#se connecter à la base de donnée
def connect_to_prodev():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )

#créer une table
def create_table(connection):
    cursor =connection.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS user_data (user_id VARCHAR(36) PRIMARY KEY, name VARCHAR(255) NOT NULL, email VARCHAR(255) NOT NULL, age DECIMAL NOT NULL)")
    connection.commit()
    print("table user_data created successfully")
    cursor.close()


#inserer les données depuis le fichier CSV
import csv 
import uuid 

def insert_data(connection,  user_data.csv):
    cursor = connection.cursor()
    with open(user_data.csv, newline='',encoding='utf-8') as file:
         reader = csv.DictReader(file)
         for row in reader:
             cursor.execute(
                 "SELECT * FROM user_data WHERE email = %s", (row['email'])
                 )
             if not cursor.fetchone():
                cursor.execute(
                  "INSERT INTO user_data (user_id, name,email,age) VALUES (%s,%s,%s,%s)",
                  (row['user_id'],row['name'],row['email'],row['age'])
                )
connection.commit()
cursor.close()


