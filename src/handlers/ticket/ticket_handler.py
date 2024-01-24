from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.utils.exceptions import DataBaseException


class TicketHandler:
    @staticmethod
    def ticket_detail(t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_detailed_ticket_view(t_id)
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
