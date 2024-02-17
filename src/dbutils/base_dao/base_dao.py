class BaseDAO:
    """Base class for every DAO. Acts as a context manager. On exit, it closes the cursor"""
    def __init__(self, conn):
        self.cur = conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()
