from flask_smorest import abort

from src.handlers.ticket.ticket_handler import TicketHandler
from src.authentication.config.auth_config_loader import AuthConfig
from src.schemas.ticket import TicketCustomerView, TicketHelpdeskView, TicketManagerView
from src.utils.exceptions import DataBaseException


class TicketController:
    @classmethod
    def get_ticket_detailed_view(cls, t_id, role, identity):
        # Get ticket by t_id
        # Get customer by c_id if e_id is provided
        # Get representative details if c_id is provided
        # Get department details by dept_id
        try:
            ticket = TicketHandler.ticket_detail(t_id)
            if role == AuthConfig.CUSTOMER:
                if ticket['c_id'] != identity:
                    abort(403, message='You are not allowed to view this resource.')
                return cls.get_customers_view(ticket)
            elif role == AuthConfig.HELPDESK:
                return cls.get_helpdesk_view(ticket)
            elif role == AuthConfig.MANAGER:
                return cls.get_managers_view(ticket)

        except DataBaseException:
            abort(500, message="There was some problem getting your ticket. Please try again later.")

    @staticmethod
    def get_customers_view(ticket):
        if ticket['repr_id'] is not None:
            return TicketCustomerView().load({
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_id': ticket['t_id'],
                    'dept_name': ticket['dept_name'],
                },
                'helpdesk_assigned': {
                    'phn_num': ticket['helpdesk']['phn_num'],
                    'full_name': ticket['helpdesk']['full_name'],
                    'email': ticket['helpdesk']['email']
                }
            })
        else:
            return TicketCustomerView().load({
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_id': ticket['t_id'],
                    'dept_name': ticket['dept_name'],
                }
            })

    @staticmethod
    def get_helpdesk_view(ticket):
        return TicketHelpdeskView().load({
            't_id': ticket['t_id'],
            'title': ticket['title'],
            'description': ticket['t_desc'],
            'status': ticket['t_status'],
            'created_on': str(ticket['created_on']),
            'department': {
                'dept_id': ticket['t_id'],
                'dept_name': ticket['dept_name'],
            }
        })

    @staticmethod
    def get_managers_view(ticket):
        if ticket['repr_id'] is not None:
            return TicketManagerView().load({
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_id': ticket['d_id'],
                    'dept_name': ticket['dept_name'],
                },
                'customer': {
                    'full_name': ticket['cust_name'],
                    'phn_num': ticket['cust_phn_num'],
                    'email': ticket['cust_email']
                },
                'helpdesk_assigned': {
                    'phn_num': ticket['helpdesk']['phn_num'],
                    'full_name': ticket['helpdesk']['full_name'],
                    'email': ticket['helpdesk']['email']
                }
            })
        else:
            return TicketManagerView().load({
                't_id': ticket['t_id'],
                'title': ticket['title'],
                'description': ticket['t_desc'],
                'status': ticket['t_status'],
                'created_on': str(ticket['created_on']),
                'department': {
                    'dept_id': ticket['d_id'],
                    'dept_name': ticket['dept_name'],
                },
                'customer': {
                    'full_name': ticket['cust_name'],
                    'phn_num': ticket['cust_phn_num'],
                    'email': ticket['cust_email']
                }
            })

