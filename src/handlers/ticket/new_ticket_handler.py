from flask import current_app
from mysql.connector import Error

from src.dbutils.connection import DatabaseConnection
from src.dbutils.department.departmentDAO import DepartmentDAO
from src.dbutils.ticket.ticketDAO import TicketDAO
from src.utils.exceptions import ApplicationError
from src.utils.exceptions import DataBaseException


class NewTicketHandler:
    @classmethod
    def create_ticket(cls, d_id, c_id, title, description):
        try:
            with DatabaseConnection() as conn:
                # Checking whether department id is valid or not
                is_dept_id_valid = cls.verify_dept_id(conn, d_id)

                if not is_dept_id_valid:
                    current_app.logger.error(f"Create Ticket: Invalid dept identification {d_id} provided.")
                    raise ApplicationError(code=400, message=current_app.config['INVALID_DEPARTMENT_ERROR_MESSAGE'])

                with TicketDAO(conn) as t_dao:
                    ticket_id = t_dao.create_new_ticket(d_id, c_id, title, description)
                    return ticket_id

        except Error as e:
            current_app.logger.error(f'Create Ticket: Database error {e} while creating new ticket.')
            raise DataBaseException(current_app.config['CREATE_TICKET_ERROR_MESSAGE'])

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
