from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt, get_jwt_identity
from flask_smorest import Blueprint

from src.controllers.message.message_controller import MessageController
from src.schemas.ticket import MessageFromManager
from src.utils.rbac.rbac import access_required

blp = Blueprint('Message', 'messages', description='Operation on messages for a particular ticket')


@blp.route('/tickets/<string:ticket_id>/message')
class Message(MethodView):
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @access_required(['HELPDESK', 'MANAGER'])
    def get(self, ticket_id):
        current_app.logger.debug(f"GET /tickets/{ticket_id}/message")
        role = get_jwt()['role']
        identity = get_jwt_identity()
        message_from_manager = MessageController.get_message_from_manager(role, identity, ticket_id)
        return message_from_manager

    @blp.arguments(MessageFromManager)
    @blp.doc(parameters=[
        {'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>',
         'required': 'true'}])
    @access_required(['MANAGER'])
    def put(self, message_data, ticket_id):
        current_app.logger.debug(f"PUT /tickets/{ticket_id}/message")
        success_message = MessageController.update_message_from_manager(message_data, ticket_id)
        return success_message
