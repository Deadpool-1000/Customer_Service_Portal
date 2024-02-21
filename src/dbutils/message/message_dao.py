import shortuuid
from datetime import datetime, timezone
from flask import current_app

from src.dbutils.base_dao import BaseDAO

logger = current_app.logger


class MessageDAO(BaseDAO):
    """Context manager for performing operation on message. On exit, it closes the cursor it uses."""

    def get_message_from_manager(self, t_id):
        """Get message from manager for ticket identification number t_id"""
        self.cur.execute(current_app.config['GET_MESSAGE_FROM_MANAGER'], {
            't_id': t_id
        })
        logger.debug(f"MessageDAO: Fetched message from manager for ticket {t_id}")
        return self.cur.fetchone()

    def update_message_from_manager(self, t_id, message):
        """Update message from manager for ticket identification number t_id"""
        existing_message = self.get_message_from_manager(t_id)
        if existing_message:
            self.cur.execute(current_app.config['UPDATE_MESSAGE_FROM_MANAGER'], {
                't_id': t_id,
                'message': message,
                'created_at': datetime.now()
            })
            logger.debug(f"MessageDAO: Message for manager updated for ticket {t_id}")
        else:
            mm_id = shortuuid.ShortUUID().random(5)
            self.cur.execute(current_app.config['INSERT_MESSAGE_FROM_MANAGER'], (mm_id, message, datetime.now(), t_id))
            logger.debug(f"MessageDAO: Message fro manager created for ticket {t_id}")
