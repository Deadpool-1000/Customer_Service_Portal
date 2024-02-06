from datetime import datetime

import shortuuid
from flask import current_app


class MessageDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_MESSAGE_FROM_MANAGER'])
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def get_message_from_manager(self, t_id):
        self.cur.execute(current_app.config['GET_MESSAGE_FROM_MANAGER'], {
            't_id': t_id
        })
        return self.cur.fetchone()

    def update_message_from_manager(self, t_id, message):
        existing_message = self.get_message_from_manager(t_id)
        if existing_message:
            self.cur.execute(current_app.config['UPDATE_MESSAGE_FROM_MANAGER'], {
                't_id': t_id,
                'message': message
            })

        else:
            mm_id = shortuuid.ShortUUID().random(5)
            self.cur.execute(current_app.config['INSERT_MESSAGE_FROM_MANAGER'], (mm_id, message, datetime.now(), t_id))
