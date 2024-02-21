from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_smorest import Blueprint

from src.controllers import FeedbackController
from src.schemas.ticket import FeedbackSchema
from src.utils.rbac.rbac import access_required

blp = Blueprint('Feedback', 'feedbacks', description='Operation on feedback for a particular ticket')


# blp doc , status code

@blp.route('/tickets/<string:ticket_id>/feedback')
class Feedback(MethodView):
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.arguments(FeedbackSchema)
    @access_required([current_app.config['CUSTOMER']])
    def put(self, feedback_data, ticket_id):
        """update or register  feedback for a particular ticket"""
        current_app.logger.debug(f"POST /tickets/{ticket_id}/feedback")
        c_id = get_jwt_identity()
        success_message = FeedbackController.update_feedback(c_id, feedback_data, ticket_id)
        return success_message, 201

    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @access_required([current_app.config['CUSTOMER'], current_app.config['MANAGER']])
    def get(self, ticket_id):
        """Get feedback for particular ticket"""
        current_app.logger.debug(f"GET /tickets/{ticket_id}/feedback")
        identity = get_jwt_identity()
        role = get_jwt()['role']
        feedback = FeedbackController.get_feedback(identity, role, ticket_id)
        return feedback, 200
