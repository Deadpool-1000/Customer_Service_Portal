from flask_smorest import abort

from src.handlers.ticket.new_ticket_handler import NewTicketHandler
from src.utils.exceptions import DataBaseException, InvalidDepartmentIDException


class NewTicketController:
    @staticmethod
    def create_ticket(ticket_data, c_id):
        # d_id, c_id, title, desc
        d_id = ticket_data["d_id"]
        title = ticket_data["title"]
        description = ticket_data["description"]

        try:
            NewTicketHandler.create_ticket(c_id=c_id, title=title, d_id=d_id, description=description)

        except DataBaseException:
            abort(500, message='There was some problem while creating the ticket. Please try again later')

        except InvalidDepartmentIDException:
            abort(400, message='No ')

