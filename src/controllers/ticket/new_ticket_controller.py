from flask_smorest import abort

from src.handlers.ticket.new_ticket_handler import NewTicketHandler
from src.utils.exceptions import DataBaseException, InvalidDepartmentIDException
from src.schemas.ticket import TicketSchema


INVALID_DEPARTMENT_ERROR_MESSAGE = 'Please provide valid department information.'


class NewTicketController:
    @staticmethod
    def create_ticket(ticket_data, c_id):
        # d_id, c_id, title, desc
        d_id = ticket_data["d_id"]
        title = ticket_data["title"]
        description = ticket_data["description"]

        try:
            is_dept_id_valid = NewTicketHandler.verify_dept_id(d_id)
            if not is_dept_id_valid:
                abort(400, message='Please provide valid department information.')

            ticket_id = NewTicketHandler.create_ticket(c_id=c_id, title=title, d_id=d_id, description=description)

            new_ticket = NewTicketHandler.get_ticket_by_id(ticket_id)

            return TicketSchema().load({
                "message_from_helpdesk" : "We will get back to you soon.",
                "status": new_ticket['t_status'],
                "description": new_ticket['t_desc'],
                "t_id": new_ticket['t_id'],
                "title": new_ticket['title'],
                "created_on": str(new_ticket['created_on'])
            })

        except DataBaseException:
            abort(500, message='There was some problem while creating the ticket. Please try again later')

        except InvalidDepartmentIDException:
            abort(400, message='No ')
