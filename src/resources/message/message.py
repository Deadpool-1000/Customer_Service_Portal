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
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @access_required([current_app.config['HELPDESK'], current_app.config['MANAGER']])
    def get(self, ticket_id):
        """Get message from manager for a particular ticket"""
        current_app.logger.debug(f"GET /tickets/{ticket_id}/message")
        role = get_jwt()['role']
        identity = get_jwt_identity()
        message_from_manager = MessageController.get_message_from_manager(role, identity, ticket_id)
        return message_from_manager

    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.arguments(MessageFromManager)
    @access_required([current_app.config['MANAGER']])
    def put(self, message_data, ticket_id):
        """"Update message from manager on a particular ticket"""
        current_app.logger.debug(f"PUT /tickets/{ticket_id}/message")
        success_message = MessageController.update_message_from_manager(message_data, ticket_id)
        return success_message
