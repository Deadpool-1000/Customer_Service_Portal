from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import get_jwt_identity, get_jwt

from src.utils.rbac.rbac import access_required
from src.authentication.config.auth_config_loader import AuthConfig
from src.controllers.ticket.new_ticket_controller import NewTicketController
from src.controllers.ticket.ticket_controller import TicketController
from src.controllers.ticket.ticket_operation_controller import TicketOperationController
from src.schemas.ticket import TicketRaisingSchema, TicketSchema, MessageFromHelpdeskSchema

blp = Blueprint('Ticket', 'tickets', description='Operation on tickets')


@blp.route('/tickets')
class Tickets(MethodView):
    @blp.response(200, TicketSchema(many=True))
    @access_required(['CUSTOMER', 'MANAGER', 'HELPDESK'])
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self):
        identity = get_jwt_identity()
        role = get_jwt()['role']
        all_tickets = TicketController.get_all_tickets_concise_view(identity, role)
        return all_tickets

    @blp.response(201, TicketSchema)
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @blp.arguments(TicketRaisingSchema)
    @access_required(['CUSTOMER'])
    def post(self, ticket_data):
        cust_id = get_jwt_identity()
        new_ticket = NewTicketController.create_ticket(ticket_data, c_id=cust_id)
        return new_ticket


@blp.route('/tickets/<string:ticket_id>')
class TicketDetails(MethodView):
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    @access_required(['CUSTOMER', 'MANAGER', 'HELPDESK'])
    def get(self, ticket_id):
        jwt = get_jwt()
        identity = get_jwt_identity()
        role = jwt['role']
        ticket = TicketController.get_ticket_detailed_view(ticket_id, role, identity)
        return ticket


@blp.route('/tickets/<string:ticket_id>/resolve')
class TicketResolve(MethodView):
    @blp.arguments(MessageFromHelpdeskSchema)
    @access_required(['HELPDESK'])
    def put(self, ticket_data, ticket_id):
        identity = get_jwt_identity()
        response = TicketOperationController.resolve_ticket(ticket_data, ticket_id, identity)
        return response


@blp.route('/tickets/<string:ticket_id>/close')
class TicketClose(MethodView):
    @blp.arguments(MessageFromHelpdeskSchema)
    @access_required(['HELPDESK'])
    def put(self, ticket_data, ticket_id):
        identity = get_jwt_identity()
        response = TicketOperationController.close_ticket(ticket_data, ticket_id, identity)
        return response
