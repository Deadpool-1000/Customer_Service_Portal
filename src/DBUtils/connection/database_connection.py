import sqlite3

from src.DBUtils.config.db_config_loader import DBConfig


class DatabaseConnection:
    def __init__(self):
        self.conn = sqlite3.connect(fr'{DBConfig.DB_FILE_PATH}')
        self.conn.row_factory = sqlite3.Row

    @staticmethod
    def dict_factory(cur, row):
        d = {}
        for idx, col in enumerate(cur.description):
            d[col[0]] = row[idx]
        return d

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            return False

        self.conn.commit()
        self.conn.close()
