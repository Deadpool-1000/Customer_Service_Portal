import logging
from flask import current_app
from mysql.connector import Error

from src.dbutils.connection.database_connection import DatabaseConnection
from src.dbutils.ticket.ticketDAO import TicketDAO
from src.dbutils.employee.employeedao import EmployeeDAO
from src.utils.exceptions import DataBaseException, ApplicationError


logger = logging.getLogger('main.ticket_handler')

ALLOWED_STATUSES = ['raised', 'closed', 'in_progress']


class TicketHandler:
    @staticmethod
    def ticket_detail(t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_detailed_ticket_view(t_id)

                    # Invalid t_id provided
                    if ticket is None:
                        logger.info(f"Invalid ticket number provided {t_id}")
                        raise ApplicationError(code=404, message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    # Helpdesk member is assigned
                    if ticket['repr_id'] is not None:
                        # get employee details
                        with EmployeeDAO(conn) as e_dao:
                            employee = e_dao.get_employee_details_by_id(ticket['repr_id'])
                            if employee is None:
                                logger.error("Invalid employee id encountered inside tickets table.")
                                raise ApplicationError(code=500, message=current_app.config['TRY_AGAIN_LATER'])
                            ticket['helpdesk'] = {
                                'full_name': employee['full_name'],
                                'phn_num': employee['phn_num'],
                                'email': employee['email']
                            }

                        # get message from helpdesk
                        message_from_helpdesk = t_dao.get_message_from_helpdesk(t_id)
                        ticket['message_from_helpdesk'] = {
                            'created_at': str(message_from_helpdesk['created_at']),
                            'message': message_from_helpdesk['message']
                        }
                    else:
                        ticket['helpdesk'] = None

                    return ticket
        except Error as e:
            logger.error(f'Database error {e} while fetching ticket: {t_id}')
            raise DataBaseException(current_app.config['TICKET_DETAIL_FETCH_ERROR_MESSAGE'])

    @staticmethod
    def is_allowed_to_view_ticket(ticket, role, identity):
        # Check role and further authorization checks
        if role != current_app.config['CUSTOMER'] and role != current_app.config['HELPDESK'] and role != current_app.config['MANAGER']:
            return False

        # Check if the customer is the creator of the ticket
        if role == current_app.config['CUSTOMER']:
            if ticket['c_id'] != identity:
                return False

        # In case it is a helpdesk member check if the ticket is related to his/her department
        elif role == current_app.config['HELPDESK']:
            dept_id = TicketHandler.get_dept_from_e_id(identity)
            if ticket['d_id'] != dept_id:
                return False

        return True

    @classmethod
    def get_tickets_by_identity_and_role(cls, role, identity, status):
        if role == current_app.config['CUSTOMER']:
            tickets = cls.get_tickets_by_c_id(identity, status)
            return tickets

        elif role == current_app.config['HELPDESK']:
            tickets = cls.get_tickets_by_e_id(identity, status)
            return tickets

        elif role == current_app.config['MANAGER']:
            tickets = cls.get_all_tickets(status)
            return tickets

    @classmethod
    def get_dept_from_e_id(cls, e_id):
        with DatabaseConnection() as conn:
            with EmployeeDAO(conn) as e_dao:
                emp_dept_detail = e_dao.get_department_by_employee_id(e_id)
        return emp_dept_detail['dept_id']

    @classmethod
    def get_tickets_by_c_id(cls, c_id, status=None):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_c_id_and_status(c_id, status)
                else:
                    tickets = t_dao.get_all_tickets_by_c_id(c_id)
        return tickets

    @classmethod
    def get_tickets_by_e_id(cls, e_id, status=None):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                dept_id = cls.get_dept_from_e_id(e_id)

                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_d_id_and_status(dept_id, status)

                else:
                    tickets = t_dao.get_all_tickets_by_d_id(dept_id)
        return tickets

    @staticmethod
    def get_all_tickets(status=None):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:

                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_status(status)

                else:
                    tickets = t_dao.get_all_tickets()

        return tickets
