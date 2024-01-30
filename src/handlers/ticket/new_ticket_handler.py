import logging

from mysql.connector import Error

from src.DBUtils.connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.utils.exceptions import DataBaseException
from src.DBUtils.department.departmentDAO import DepartmentDAO

CREATE_TICKET_ERROR_MESSAGE = 'There was some problem creating the ticket'

logger = logging.getLogger('main.new_ticket_handler')


class NewTicketHandler:
    @staticmethod
    def create_ticket(d_id, c_id, title, description):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket_id = t_dao.create_new_ticket(d_id, c_id, title, description)
                    return ticket_id

        except Error as e:
            logger.error(f'Database error {e} while creating new ticket.')
            raise DataBaseException(CREATE_TICKET_ERROR_MESSAGE)

    @staticmethod
    def get_ticket_by_id(ticket_id):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                ticket = t_dao.get_ticket_by_tid(ticket_id)
                return ticket

    @staticmethod
    def verify_dept_id(dept_id):
        with DatabaseConnection() as conn:
            with DepartmentDAO(conn) as d_dao:
                department = d_dao.get_department_by_id(dept_id)
                return department is not None
