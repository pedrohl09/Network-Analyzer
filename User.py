import sqlite3
class User():
    def __init__(self, name = "system.db", sys_log = "system_log.db") -> None:
        self.name = name
        self.sys_log = sys_log
        self.connection = sqlite3.connect(self.name)
        self.cursor = self.connection.cursor()
        self.connection2 = sqlite3.connect(self.sys_log)
        self.cursor2 = self.connection2.cursor()

    def check_login(self):
        pass
    def extract_data(self):
        import pandas as pd

        tabela = pd.read_sql_query("SELECT * FROM userslog", self.connection2)
        df = pd.DataFrame(tabela, columns=['usuario', 'data'])
        print(df)

    def select_db(self, username, password):
        return self.cursor.execute("""
            SELECT * FROM users WHERE usuario = ? AND senha = ?;
        """, (username, password)).fetchone()

    def login(self):
        print("Entre com o usuário")
        username = input('Username: ')
        password = input('Password: ')
        user = self.select_db(username, password)

        if user:
            print('Welcome to system!')
            from datetime import datetime
            date = datetime.now()
            date.replace(microsecond=0)
            print(date)
            self.cursor2.execute("""
                INSERT INTO userslog(usuario, data) VALUES(?,?)
            """, (username, date))
            self.connection2.commit()
            return True         
        else:
            print('Authentication failed')
            return False

    def close_connection(self):
        return self.connection.close(), self.connection2.close()
