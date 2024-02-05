from flask_smorest import abort

from src.handlers.ticket.new_ticket_handler import NewTicketHandler
from src.utils.exceptions import DataBaseException, ApplicationError


DEFAULT_MESSAGE_FROM_HELPDESK = 'We will get back to you soon 🙂.'


class NewTicketController:
    @staticmethod
    def create_ticket(ticket_data, c_id):
        # d_id, c_id, title, desc
        d_id = ticket_data["d_id"]
        title = ticket_data["title"]
        description = ticket_data["description"]

        try:
            ticket_id = NewTicketHandler.create_ticket(c_id=c_id, title=title, d_id=d_id, description=description)
            new_ticket = NewTicketHandler.get_ticket_by_id(ticket_id)

            return {
                "message_from_helpdesk": DEFAULT_MESSAGE_FROM_HELPDESK,
                "status": new_ticket['t_status'],
                "description": new_ticket['t_desc'],
                "t_id": new_ticket['t_id'],
                "title": new_ticket['title'],
                "created_on": str(new_ticket['created_on'])
            }

        except DataBaseException as db:
            abort(500, message=str(db))

        except ApplicationError as ae:
            abort(400, message=ae.message)
