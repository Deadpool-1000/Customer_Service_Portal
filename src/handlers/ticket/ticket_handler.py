import logging

from flask import current_app
import pymysql

from src.dbutils.connection.database_connection import DatabaseConnection
from src.dbutils.employee.employee_dao import EmployeeDAO
from src.dbutils.ticket.ticket_dao import TicketDAO
from src.utils.exceptions import DataBaseException, ApplicationError

logger = current_app.logger

ALLOWED_STATUSES = ['raised', 'closed', 'in_progress']


class TicketHandler:
    @staticmethod
    def ticket_detail(t_id):
        """Fetches a detailed view for a ticket with identification number t_id."""
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_detailed_ticket_view(t_id)

                    # Invalid t_id provided
                    if ticket is None:
                        current_app.logger.info(f"Ticket detail: Invalid ticket number provided {t_id}")
                        raise ApplicationError(code=404,
                                               message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    # Helpdesk member is assigned
                    if ticket['repr_id'] is not None:
                        # get employee details
                        with EmployeeDAO(conn) as e_dao:
                            employee = e_dao.get_employee_details_by_id(ticket['repr_id'])

                            if employee is None:
                                current_app.logger.info(f"Ticket detail: Invalid repr id found in database.")
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
                    current_app.logger.info(f"Ticket detail: Ticket {t_id} fetched.")
                    return ticket
        except pymysql.Error as e:
            logger.error(f'Ticket detail: Database error {e.args[0]}: {e.args[1]} while fetching ticket: {t_id}')
            raise DataBaseException(current_app.config['TICKET_DETAIL_FETCH_ERROR_MESSAGE'])

    @staticmethod
    def is_allowed_to_view_ticket(ticket, role, identity):
        """Check if the user with the give identity and role is allowed to access the ticket"""
        # Check role and further authorization checks
        if role != current_app.config['CUSTOMER'] and role != current_app.config['HELPDESK'] and role != \
                current_app.config['MANAGER']:
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
    def get_tickets_by_identity_and_role(cls, role, identity, status, page, page_size):
        """Get tickets based of identity and role
            1. If role == Manager, then all tickets in the system are returned.
            2. If role == Customer, then tickets that the customer has created is returned
            3. if role == Helpdesk, then tickets that belong to the helpdesk member's department are returned.
        """
        offset = (page-1)*page_size
        try:
            if role == current_app.config['CUSTOMER']:
                tickets = cls.get_tickets_by_c_id(identity, page_size, offset, status=status)
                return tickets

            elif role == current_app.config['HELPDESK']:
                tickets = cls.get_tickets_by_e_id(identity, page_size, offset, status=status)
                return tickets

            elif role == current_app.config['MANAGER']:
                tickets = cls.get_all_tickets(page_size, offset, status=status)
                return tickets
        except pymysql.Error as e:
            logger.error(f"There was an error while fetching tickets for identity {identity}, Error {e.args[0]}: {e.args[1]}")
            raise DataBaseException("There was a problem while fetching tickets. Please try again later.")

    @classmethod
    def get_dept_from_e_id(cls, e_id):
        """Returns department identification number for helpdesk members employee id"""
        with DatabaseConnection() as conn:
            with EmployeeDAO(conn) as e_dao:
                emp_dept_detail = e_dao.get_department_by_employee_id(e_id)
        return emp_dept_detail['dept_id']

    @classmethod
    def get_tickets_by_c_id(cls, c_id, page_size, offset, status=None):
        """Get tickets that customer with c_id has created."""
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_c_id_and_status(c_id, status, page_size, offset)
                else:
                    tickets = t_dao.get_all_tickets_by_c_id(c_id, page_size, offset)
        return tickets

    @classmethod
    def get_tickets_by_e_id(cls, e_id, page_size, offset, status=None):
        """Get tickets that belong to employee's department"""
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                dept_id = cls.get_dept_from_e_id(e_id)
                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_d_id_and_status(dept_id, status, page_size, offset)
                else:
                    tickets = t_dao.get_all_tickets_by_d_id(dept_id, page_size, offset)
        return tickets

    @staticmethod
    def get_all_tickets(page_size, offset, status=None):
        """Get all tickets that are in the system"""
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:

                if status in ALLOWED_STATUSES:
                    tickets = t_dao.get_tickets_by_status(status, page_size, offset)

                else:
                    tickets = t_dao.get_all_tickets(page_size, offset)

        return tickets
