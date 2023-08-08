import sqlite3

# banco = sqlite3.connect('databaseNA.db')

# cursor = banco.cursor()
# # cursor.execute("CREATE TABLE users(email TEXT NOT NULL, senha TEXT NOT NULL, PRIMARY KEY(email))")
# # cursor.execute("INSERT INTO users VALUES('pedro.lira.074@ufrn.edu.br', '12345')")
# cursor.execute("SELECT * FROM users")

# print(cursor.fetchall())
# banco.commit()

class DataBase():
    def __init__(self, name = "system.db") -> None:
        self.name = name

    def conecta(self):
        self.connection = sqlite3.connect(self.name)

    def close_connection(self):
        try:
            self.connection.close()
        except:
            pass

    def create_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users(id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL, 
                senha TEXT NOT NULL,
                access TEXT NOT NULL);
            """)
        except AttributeError:
            print("Faça conexão")

    def show_db(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT * FROM userslog;
        """)
        print(cursor.fetchall())

    def insert_user(self, usuario, senha, access):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                INSERT INTO users(usuario, senha, access) VALUES(?,?,?)
            """, (usuario, senha, access))
            self.connection.commit()
        except AttributeError:
            print("Faça conexão")

    def create_table2(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS userslog(usuario TEXT NOT NULL, 
                data DATETIME NOT NULL);
            """)
        except AttributeError:
            print("Faça conexão")

    def drop_table(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("""
                DROP TABLE users;
            """)
        except AttributeError:
            print("Faça conexão")    


if __name__ == "__main__":
    db = DataBase("system_log.db")
    db.conecta()
    # db.drop_table()
    db.show_db()
    db.close_connection()
