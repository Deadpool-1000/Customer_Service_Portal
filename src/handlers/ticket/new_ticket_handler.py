import logging

from mysql.connector import Error

from src.DBUtils.connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.utils.exceptions import DataBaseException
from src.DBUtils.department.departmentDAO import DepartmentDAO
from src.utils.exceptions import ApplicationError

CREATE_TICKET_ERROR_MESSAGE = 'There was some problem creating the ticket'
INVALID_DEPT_ID_MESSAGE = 'Please provide valid department information.'

logger = logging.getLogger('main.new_ticket_handler')


class NewTicketHandler:
    @classmethod
    def create_ticket(cls, d_id, c_id, title, description):
        try:
            with DatabaseConnection() as conn:
                # Checking whether department id is valid or not
                is_dept_id_valid = cls.verify_dept_id(conn, d_id)

                if not is_dept_id_valid:
                    raise ApplicationError(code=400, message=INVALID_DEPT_ID_MESSAGE)

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
    def verify_dept_id(conn, dept_id):
        with DepartmentDAO(conn) as d_dao:
            department = d_dao.get_department_by_id(dept_id)
            return department is not None
