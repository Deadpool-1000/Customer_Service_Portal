from flask import current_app
from mysql.connector import Error

from src.dbutils.connection.database_connection import DatabaseConnection
from src.dbutils.employee.employeedao import EmployeeDAO
from src.dbutils.ticket.ticketDAO import TicketDAO
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketOperationHandler:
    @staticmethod
    def resolve_ticket(t_id, ticket_data, identity):
        # Verify if the user can edit this ticket
        # add message to message_from_helpdesk table
        # add repr id to tickets table
        # change ticket status to in-progress
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)

                    # Invalid t_id provided
                    if ticket is None:
                        current_app.logger.error(f"Resolve Ticket: Invalid ticket id provided: {t_id}")
                        raise ApplicationError(code=404,
                                               message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    # Ticket is already closed or in_progress
                    if ticket['t_status'] == current_app.config['IN_PROGRESS'] or ticket['t_status'] == \
                            current_app.config['CLOSED']:
                        current_app.logger.error(
                            f"Resolve Ticket: User tried to resolve an already resolved ticket for Ticket Id: {t_id}")
                        raise ApplicationError(code=400, message=current_app.config['ALREADY_RESOLVED_OR_CLOSED'])

                    with EmployeeDAO(conn) as e_dao:
                        dept_id = e_dao.get_department_by_employee_id(identity)
                        if dept_id['dept_id'] != ticket['d_id']:
                            current_app.logger.error(
                                f"Resolve Ticket: There was an error while resolving a ticket{t_id}. e_id did not belong to correct department")
                            raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

                    t_dao.assign_repr_id(t_id, identity)
                    t_dao.change_ticket_status(t_id, current_app.config['IN_PROGRESS'])
                    t_dao.update_message_from_helpdesk(ticket_data['message_from_helpdesk'], t_id)

        except Error as e:
            current_app.logger.error(f"There was an error while resolving a ticket{t_id} {e.msg}")
            raise DataBaseException(current_app.config['RESOLVE_TICKET_ERROR_MESSAGE'])

    @staticmethod
    def close_ticket(t_id, ticket_data, identity):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)
                    # Invalid t_id provided
                    if ticket is None:
                        current_app.logger.error(f"Invalid ticket id provided: {t_id}")
                        raise ApplicationError(code=404,
                                               message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    # Ticket is already closed or in raised condition
                    if ticket['t_status'] == current_app.config['RAISED'] or ticket['t_status'] == current_app.config[
                        'CLOSED']:
                        current_app.logger.error(
                            f"User tried to resolve an already closed or just raised ticket for Ticket Id: {t_id}")
                        raise ApplicationError(code=400, message=current_app.config['ALREADY_CLOSED_OR_RAISED'])

                    with EmployeeDAO(conn) as e_dao:
                        dept_id = e_dao.get_department_by_employee_id(identity)
                        if dept_id['dept_id'] != ticket['d_id']:
                            current_app.logger.error(
                                f"There was an error while resolving a ticket{t_id}. e_id did not belong to correct department")
                            raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

                    t_dao.change_ticket_status(t_id, current_app.config['CLOSED'])
                    t_dao.update_message_from_helpdesk(ticket_data['message_from_helpdesk'], t_id)

        except Error as e:
            current_app.logger.error(f"There was an error while closing a ticket{t_id} {e.msg}")
            raise DataBaseException(current_app.config['CLOSE_TICKET_ERROR_MESSAGE'])
