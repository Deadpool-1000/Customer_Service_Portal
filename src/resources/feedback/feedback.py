from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt_identity, get_jwt

from src.controllers import FeedbackController
from src.utils.rbac.rbac import access_required
from src.schemas.ticket import FeedbackSchema


blp = Blueprint('Feedback', 'feedbacks', description='Operation on feedback for a particular ticket')


@blp.route('/tickets/<string:ticket_id>/feedback')
class Feedback(MethodView):
    @blp.arguments(FeedbackSchema)
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @access_required(['CUSTOMER'])
    def post(self, feedback_data, ticket_id):
        c_id = get_jwt_identity()
        success_message = FeedbackController.register_feedback(c_id, feedback_data, ticket_id)
        return success_message, 201

    @access_required(['CUSTOMER', 'MANAGER'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self, ticket_id):
        identity = get_jwt_identity()
        role = get_jwt()['role']
        feedback = FeedbackController.get_feedback(identity, role, ticket_id)
        return feedback
