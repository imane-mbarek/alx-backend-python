import seed

def paginate_users(page_size, offset):
    connection = seed.connect_to_prodev()        # 1. Connexion à la base 'ALX_prodev'
    cursor = connection.cursor(dictionary=True)  # 2. Crée un curseur qui retourne les lignes comme des dictionnaires
    cursor.execute("SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}"
                  )                              # 3. Fait une requête SQL pour obtenir une page d'utilisateurs
    
    rows = cursor.fetchall()                     # 4. Récupère toutes les lignes de cette page
    cursor.close()
    connection.close()                           # 6. Ferme la connexion
    return rows 


def lazy_paginate(page_size):
    offset = 0                      # 1. On commence à lire à partir du début de la base
    while True:
          page = paginate_users(page_size , offset)    # 3. On récupère une page d'utilisateurs 
          if not page:
             break                  # 4. Si la page est vide → fin de la base → on quitte
          yield page                # 5. On retourne la page actuelle au fur et à mesure (lazy)
          offst += page_size        # 6. On avance à la prochaine page
