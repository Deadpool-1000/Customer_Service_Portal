from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketHandler:
    @staticmethod
    def ticket_detail(t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_detailed_ticket_view(t_id)
                    if ticket is None:
                        raise ApplicationError(code=404, message='Invalid ticket id provided')

                    # Helpdesk member is assigned
                    if ticket['repr_id'] is not None:
                        with EmployeeDAO(conn) as e_dao:
                            employee = e_dao.get_employee_details_by_id(ticket['repr_id'])
                            ticket['helpdesk'] = {
                                'full_name': employee['full_name'],
                                'phn_num': employee['phn_num'],
                                'email': employee['email']
                            }
                    else:
                        ticket['helpdesk'] = None

                    return ticket
        except Error as e:
            print(e)
            raise DataBaseException('There was some problem getting your data.')

    @classmethod
    def get_dept_from_e_id(cls, e_id):
        with DatabaseConnection() as conn:
            with EmployeeDAO(conn) as e_dao:
                emp_dept_detail = e_dao.get_department_by_employee_id(e_id)
        return emp_dept_detail['dept_id']

    @classmethod
    def get_ticket_by_c_id(cls, c_id):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                tickets = t_dao.get_all_tickets_by_c_id(c_id)
        return tickets

    @classmethod
    def get_tickets_by_e_id(cls, e_id):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                dept_id = cls.get_dept_from_e_id(e_id)
                tickets = t_dao.get_all_tickets_by_d_id(dept_id)
        return tickets

    @classmethod
    def get_all_tickets(cls):
        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                tickets = t_dao.get_all_tickets()
        return tickets
