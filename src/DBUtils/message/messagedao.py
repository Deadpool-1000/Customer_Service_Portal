import shortuuid
from datetime import datetime

from src.DBUtils.config.queries_config_loader import QueriesConfig


class MessageDAO:

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def get_message_from_manager(self, t_id):
        self.cur.execute(QueriesConfig.GET_MESSAGE_FROM_MANAGER, {
            't_id': t_id
        })
        return self.cur.fetchone()

    def update_message_from_manager(self, t_id, message):
        existing_message = self.get_message_from_manager(t_id)
        if existing_message:
            self.cur.execute(QueriesConfig.UPDATE_MESSAGE_FROM_MANAGER, {
                't_id': t_id,
                'message': message
            })

        else:
            mm_id = shortuuid.ShortUUID().random(5)
            self.cur.execute(QueriesConfig.INSERT_MESSAGE_FROM_MANAGER, (mm_id, message, datetime.now(), t_id))