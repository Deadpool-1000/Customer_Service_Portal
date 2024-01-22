from flask.views import MethodView
from flask_smorest import Blueprint

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO

blp = Blueprint('Ticket', 'tickets', description='Operation on tickets')


@blp.route('/tickets')
class Tickets(MethodView):
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self):
        pass

    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def post(self):
        pass


@blp.route('/tickets/<string:ticket_id>')
class TicketDetails(MethodView):
    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def get(self, ticket_id):
        pass

    @blp.doc(parameters=[{'name': 'Authorization', 'in': 'header', 'description': 'Authorization: Bearer <access_token>', 'required': 'true'}])
    def put(self, ticket_id):
        pass

