from datetime import datetime

import shortuuid
from flask import current_app

from src.dbutils.base_dao import BaseDAO

logger = current_app.logger


class FeedbackDAO(BaseDAO):
    """Context manager for performing operation on feedback. On exit, it closes the cursor it uses."""

    def add_feedback(self, stars, desc, t_id):
        """Add/Update feedback for ticket identification number t_id"""
        existing_feedback = self.get_feedback_by_tid(t_id)
        if existing_feedback:
            self.cur.execute(current_app.config['UPDATE_FEEDBACK'], {
                'stars': stars,
                'description': desc,
                't_id': t_id,
                'created_at': datetime.now()
            })
            logger.debug(f"FeedbackDAO: feedback updated for ticket {t_id}")
        else:
            f_id = shortuuid.ShortUUID().random(length=5)
            self.cur.execute(current_app.config['INSERT_INTO_FEEDBACK'], (f_id, stars, desc, t_id, datetime.now()))
            logger.debug(f"FeedbackDAO: feedback registered for ticket {t_id}")

    def get_feedback_by_tid(self, t_id):
        """Fetch feedback for ticket with ticket identification number t_id"""
        self.cur.execute(current_app.config['GET_FEEDBACK_BY_TID'], {'t_id': t_id})
        logger.debug(f"FeedbackDAO: fetched feedback for ticket {t_id}")
        return self.cur.fetchone()
