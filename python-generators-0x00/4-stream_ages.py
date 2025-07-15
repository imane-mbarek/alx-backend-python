import seed 

#Utiliser un générateur qui lit âge par âge

def stream_user_ages():
    connection=seed.connect_to_prodev()
    cursor=connection.cursor()
    cursor.execute("SELECT age FROM user_data")

    for age in cursor:
        yield age

    cursor.close()
    connection.close()


#Calculer la moyenne
def average_age():
    total = 0
    count =0
    for age in stream_user_ages():
        total+= age
        count+=1

    if count >0
       avg =total / count
       print("Average age of users: {avg:.2f}")
    else:
      print("No users found!!")
