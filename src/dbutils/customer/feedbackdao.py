import shortuuid
from flask import current_app



class FeedbackDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_FEEDBACK'])
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_val:
            return False
        self.cur.close()

    def add_feedback(self, stars, desc, t_id):
        f_id = shortuuid.ShortUUID().random(length=5)
        self.cur.execute(current_app.config['INSERT_INTO_FEEDBACK'], (f_id, stars, desc, t_id))

    def get_feedback_by_tid(self, t_id):
        # (f_id, stars, description, t_id)
        self.cur.execute(current_app.config['GET_FEEDBACK_BY_TID'], {'t_id': t_id})
        return self.cur.fetchone()
