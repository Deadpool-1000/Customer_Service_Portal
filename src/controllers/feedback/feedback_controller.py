from flask_smorest import abort
from src.handlers.feedback.feedback_handler import FeedbackHandler
from src.utils.exceptions import ApplicationError, DataBaseException


class FeedbackController:
    @staticmethod
    def register_feedback(c_id, feedback_data, t_id):
        try:
            stars = feedback_data['stars']
            description = feedback_data['description']

            FeedbackHandler.add_feedback_for_ticket(c_id, stars, description, t_id)

            return {
                "message": "Feedback Registered successfully."
            }

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=db)

    @staticmethod
    def get_feedback(identity, role, t_id):
        try:
            is_allowed = FeedbackHandler.access_allowed(identity, role, t_id)
            print(role, identity)
            if not is_allowed:
                abort(401, message='You are not authorized to view this resource.')

            feedback = FeedbackHandler.get_feedback_for_ticket(t_id)
            return feedback

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=db)
