import MYSQLdb


class DatabaseConnection:
      def __init__(self , host="localhost" , user="root" , password="imane" , database="ALX_prodev"):
          self.host=host
          self.user=user,
          self.password=password,
          self.database=database
 

     def __enter__(self):
         # Connexion à la base de données
         self.connection=MYSQLdb.connect(
              host=self.host
              user=self.user
              password=self.password
              database=self.database
              )
         # Création d’un curseur
         self.cursor =self.connection.cursor()
         self self.cursor
         return self.cursor

     def __exit__(self , exc_type , exc_value,traceback):
         if exc_type:
            print("Une exception a été levée !")
            print(f"Type : {exc_type}")
            print(f"Message : {exc_value}")
            #exc_type	Le type de l’exception levée (ex: ZeroDivisionError, ValueError, etc.)
            #exc_value	Le message ou l’objet de l’exception levée
            #traceback	L’objet traceback qui contient l’emplacement exact où l’erreur s’est produite
           
            self.cursor.close()
            self.connection.close()



if __name__ == "__main__":
    with DatabaseConnection() as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        for row in results:
            print(row)
