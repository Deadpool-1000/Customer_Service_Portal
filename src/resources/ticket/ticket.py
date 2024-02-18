from flask import request, current_app
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, get_jwt
from flask_smorest import Blueprint
from flask_smorest.pagination import PaginationParameters

from src.controllers import NewTicketController
from src.controllers import TicketController
from src.controllers import TicketOperationController
from src.schemas.error import CustomErrorSchema
from src.schemas.ticket import TicketRaisingSchema, TicketSchema, MessageFromHelpdeskSchema, TicketDetailedView
from src.utils.rbac.rbac import access_required

blp = Blueprint('Ticket', 'tickets', description='Operation on tickets')


@blp.route('/tickets')
class Tickets(MethodView):
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.paginate()
    @blp.alt_response(401, schema=CustomErrorSchema)
    @blp.response(200, TicketSchema(many=True))
    @access_required([current_app.config['CUSTOMER'], current_app.config['MANAGER'], current_app.config['HELPDESK']])
    def get(self, pagination_parameters: PaginationParameters):
        """Get all tickets"""
        current_app.logger.debug("GET /tickets")
        identity = get_jwt_identity()
        role = get_jwt()['role']
        ticket_status = request.args.get('ticket_status')
        all_tickets = TicketController.get_all_tickets(identity, role, ticket_status, pagination_parameters)
        return all_tickets

    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.alt_response(403, schema=CustomErrorSchema)
    @blp.alt_response(401, schema=CustomErrorSchema)
    @blp.response(201, TicketSchema)
    @blp.arguments(TicketRaisingSchema)
    @access_required([current_app.config['CUSTOMER']])
    def post(self, ticket_data):
        """Raise a new ticket"""
        current_app.logger.debug("POST /tickets")
        cust_id = get_jwt_identity()
        new_ticket = NewTicketController.create_ticket(ticket_data, c_id=cust_id)
        return new_ticket


@blp.route('/tickets/<string:ticket_id>')
class TicketDetails(MethodView):
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.alt_response(403, schema=CustomErrorSchema)
    @blp.alt_response(401, schema=CustomErrorSchema)
    @blp.response(200, schema=TicketDetailedView)
    @access_required([current_app.config['CUSTOMER'], current_app.config['MANAGER'], current_app.config['HELPDESK']])
    def get(self, ticket_id):
        """Get a detailed view for a particular ticket"""
        current_app.logger.debug(f"GET /tickets/{ticket_id}")
        jwt = get_jwt()
        identity = get_jwt_identity()
        role = jwt['role']
        ticket = TicketController.get_ticket_detailed_view(ticket_id, role, identity)
        return ticket


@blp.route('/tickets/<string:ticket_id>/resolve')
class TicketResolve(MethodView):
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.arguments(MessageFromHelpdeskSchema)
    @access_required([current_app.config['HELPDESK']])
    def put(self, ticket_data, ticket_id):
        """Resolve a particular ticket"""
        current_app.logger.debug(f"PUT /tickets/{ticket_id}/resolve")
        identity = get_jwt_identity()
        response = TicketOperationController.resolve_ticket(ticket_data, ticket_id, identity)
        return response


@blp.route('/tickets/<string:ticket_id>/close')
class TicketClose(MethodView):
    @blp.doc(parameters=[current_app.config['SECURITY_PARAMETERS']])
    @blp.arguments(MessageFromHelpdeskSchema)
    @access_required([current_app.config['HELPDESK']])
    def put(self, ticket_data, ticket_id):
        """Close a particular ticket"""
        current_app.logger.debug(f"PUT /tickets/{ticket_id}/close")
        identity = get_jwt_identity()
        response = TicketOperationController.close_ticket(ticket_data, ticket_id, identity)
        return response
