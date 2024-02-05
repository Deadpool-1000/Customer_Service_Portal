import logging
from flask import current_app
from flask_smorest import abort

from src.handlers.ticket.ticket_handler import TicketHandler
from src.utils.exceptions import DataBaseException, ApplicationError


DEFAULT_HELPDESK_MESSAGE = 'We will get back to you soon 🙂.'

logger = logging.getLogger('main.ticket_controller')


class TicketController:
    @classmethod
    def get_ticket_detailed_view(cls, t_id, role, identity):
        try:
            ticket = TicketHandler.ticket_detail(t_id)
            is_allowed = TicketHandler.is_allowed_to_view_ticket(ticket, role, identity)

            if not is_allowed:
                logger.info(f"User with role {role} and identity {identity} tried to access a protected resource for which user is unauthorized.")
                abort(403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

            return cls.ticket_detailed_view(ticket)

        except DataBaseException as db:
            abort(500, message=str(db))

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
                'customer': {
                    'full_name': ticket['cust_name'],
                    'email': ticket['cust_email'],
                    'phn_num': ticket['cust_phn_num']
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
                'message_from_helpdesk': DEFAULT_HELPDESK_MESSAGE
            }

    @classmethod
    def get_all_tickets(cls, identity, role, status):
        tickets = TicketHandler.get_tickets_by_identity_and_role(role, identity, status)
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
