import sqlite3


class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect(r"C:\Users\mbhatnagar\PycharmProjects\CSM\DBUtils\data\csm.db")

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            return False

        self.conn.commit()
        self.conn.close()
