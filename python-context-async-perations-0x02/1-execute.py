import sqlite3


class ExecuteQuery(self,query , param):
      def __enter__(self):
          self.conn=sqlite3.connect("users.db")
          self.cursor=self.conn.cursor()
          self.cursor.execute(self.query, (self.param,))
          return self.cursor.fetchall

       def __exit__(self,exc_type, exc_val,exc_tab):
           self.conn.commit()
           self.conn.close()


if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    with ExecuteQuery(query, 25) as results:
        for row in results:
            print(row)
