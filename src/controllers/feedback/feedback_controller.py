from flask import current_app
from flask_smorest import abort

from src.handlers.feedback.feedback_handler import FeedbackHandler
from src.utils.exceptions import ApplicationError, DataBaseException

logger = current_app.logger


class FeedbackController:
    @staticmethod
    def update_feedback(c_id, feedback_data, t_id):
        try:
            stars = feedback_data['stars']
            description = feedback_data['description']

            FeedbackHandler.update_feedback_for_ticket(c_id, stars, description, t_id)
            logger.info(f"Customer {c_id} added feedback for ticket {t_id}")
            return {
                "message": current_app.config['FEEDBACK_REGISTERED_SUCCESS']
            }

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=str(db))

    @staticmethod
    def get_feedback(identity, role, t_id):
        try:
            """
            is_allowed = FeedbackHandler.access_allowed(identity, role, t_id)
            if not is_allowed:
                logger.error(
                    f"Identity {identity} tried to access feedback for ticket {t_id} for which they are not allowed")
                abort(401, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])
            """

            feedback = FeedbackHandler.get_feedback_for_ticket(identity, role, t_id)
            logger.info(f"Identity {identity} fetched feedback for ticket {t_id}")
            return feedback

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=str(db))
