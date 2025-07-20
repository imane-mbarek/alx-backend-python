import asyncio
import aiosqlite



# Fonction pour récupérer tous les utilisateurs
async def async_fetch_users():
async with aiosqlite.connect("users.db")as db:
      async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall

# Fonction pour récupérer les utilisateurs ayant plus de 40 ans
async def async_fetch_older_users():
async with aiosqlite.connect("users.db")as db:
      async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall


# Fonction principale pour lancer les deux requêtes en parallèle
async def fetch_concurrently():
      users , older_users = await asyncio.gather(
            async_fetch_users(),
            async_fetch_older_users()
      )



# Point d’entrée du script
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
