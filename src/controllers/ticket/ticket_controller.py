from flask_smorest import abort

from src.handlers.ticket.ticket_handler import TicketHandler
from src.authentication.config.auth_config_loader import AuthConfig
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketController:
    @classmethod
    def get_ticket_detailed_view(cls, t_id, role, identity):
        # Get ticket by t_id
        # Check role and provide only the necessary details
        # return the correctly formed view of the ticket to the route
        try:
            ticket = TicketHandler.ticket_detail(t_id)
            print(ticket)
            is_allowed = TicketHandler.is_allowed_to_view_ticket(ticket, role, identity)

            if not is_allowed:
                abort(403, message='You are not authorized to view this resource.')

            return cls.ticket_detailed_view(ticket)

        except DataBaseException:
            abort(500, message="There was some problem getting your ticket. Please try again later.")

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

    @staticmethod
    def ticket_detailed_view(ticket):
        if ticket['repr_id'] is not None:
            return {
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_name': ticket['dept_name']
                },
                'helpdesk_assigned': {
                    **ticket['helpdesk']
                },
                "message_from_helpdesk": {
                    **ticket['message_from_helpdesk']
                }
            }
        else:
            return {
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_id': ticket['t_id'],
                    'dept_name': ticket['dept_name'],
                },
                'message_from_helpdesk': "We will get back to you soon. 🙂"
            }

    @classmethod
    def get_all_tickets_concise_view(cls, identity, role):
        tickets = TicketHandler.get_tickets_by_identity_and_role(role, identity)
        return [cls.ticket_concise_view(ticket) for ticket in tickets]

    @staticmethod
    def ticket_concise_view(ticket):
        return {
            't_id': ticket['t_id'],
            'title': ticket['title'],
            'description': ticket['t_desc'],
            'created_on': str(ticket['created_on']),
            'status': ticket['t_status']
        }
