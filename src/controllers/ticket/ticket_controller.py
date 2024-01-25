from flask_smorest import abort

from src.handlers.ticket.ticket_handler import TicketHandler
from src.authentication.config.auth_config_loader import AuthConfig
from src.schemas.ticket import TicketCustomerView, TicketHelpdeskView, TicketManagerView, TicketSchema
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketController:
    @classmethod
    def get_ticket_detailed_view(cls, t_id, role, identity):
        # Get ticket by t_id
        # Check role and provide only the necessary details
        # return the correctly formed view of the ticket to the route
        try:
            ticket = TicketHandler.ticket_detail(t_id)

            # Check role and further authorization checks
            if role == AuthConfig.CUSTOMER:
                if ticket['c_id'] != identity:
                    abort(403, message='You are not allowed to view this resource.')
                return cls.get_customers_view(ticket)

            # In case it is a helpdesk member check if the ticket is related to his/her department
            elif role == AuthConfig.HELPDESK:
                dept_id = TicketHandler.get_dept_from_e_id(identity)
                if ticket['d_id'] != dept_id:
                    abort(403, message="You are not authorized to view this resource.")
                return cls.get_helpdesk_view(ticket)

            #  Manager gets the view of all tickets across all departments
            elif role == AuthConfig.MANAGER:
                return cls.get_managers_view(ticket)

        except DataBaseException:
            abort(500, message="There was some problem getting your ticket. Please try again later.")

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

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
                'dept_id': ticket['d_id'],
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

    @classmethod
    def get_all_tickets_concise_view(cls, identity, role):
        if role == AuthConfig.CUSTOMER:
            tickets = TicketHandler.get_ticket_by_c_id(identity)
            return [cls.ticket_to_ticket_schema(ticket) for ticket in tickets]

        elif role == AuthConfig.HELPDESK:
            tickets = TicketHandler.get_tickets_by_e_id(identity)
            return [cls.ticket_to_ticket_schema(ticket) for ticket in tickets]

        elif role == AuthConfig.MANAGER:
            tickets = TicketHandler.get_all_tickets()
            return [cls.ticket_to_ticket_schema(ticket) for ticket in tickets]

    @staticmethod
    def ticket_to_ticket_schema(ticket):
        return TicketSchema().load({
                    't_id': ticket['t_id'],
                    'title': ticket['title'],
                    'description': ticket['t_desc'],
                    'created_on': str(ticket['created_on']),
                    'status': ticket['t_status']
                })
