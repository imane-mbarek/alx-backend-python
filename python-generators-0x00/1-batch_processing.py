import mysql.connector

def stream_users_in_batches(batch_size):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="ALX_prodev"
    )
    cursor=connection.cursor(dictionary=True)
 
    cursor.execute("SELECT * FROM user_data")

    while True:
          batch= cursor.fetchmany(batch_size)
          if not batch: break
          yield batch

    cursor.close()
    connection.close()



#Fonction batch_processing(batch_size)

#Appelle stream_users_in_batches(batch_size)

#Pour chaque batch reçu :

#Parcourt les utilisateurs

#Filtre ceux dont age > 25

#Les affiche un par un



def batch_processing(batch_size):
    for batch in stream_users_in_batches(batch_size):
        for user in batch
            if (user['age'] > 25 :
               return user
