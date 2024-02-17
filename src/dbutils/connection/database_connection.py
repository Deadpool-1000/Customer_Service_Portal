import os
import pymysql


class DatabaseConnection:
    """Context manager for maintaining a database connection. On exit, it closes the database connection and commits the changes"""
    def __init__(self):
        """Initialize a database connection to mysql server"""
        self.conn = pymysql.connect(
            port=int(os.getenv('DB_PORT')),
            cursorclass=pymysql.cursors.DictCursor,
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            db=os.getenv('DEV_DB_NAME'),
        )

    def __enter__(self):
        return self.conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            return False

        self.conn.commit()
        self.conn.close()
