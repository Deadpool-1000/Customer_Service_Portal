import logging
from flask_smorest import abort
from mysql.connector import Error

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.DBUtils.employee.employeedao import EmployeeDAO
from src.DBUtils.config.db_config_loader import DBConfig
from src.utils.exceptions import DataBaseException, ApplicationError

logger = logging.getLogger('main.ticket_operation_handler')

INVALID_TICKET_NUMBER_MESSAGE = 'Invalid Ticket Identification Number provided.'
ALREADY_RESOLVED_OR_CLOSED = 'This ticket cannot be resolve as either it is already resolved or closed.'
UNAUTHORIZED_MESSAGE = 'You are not authorized to use this resource.'
RESOLVE_TICKET_ERROR_MESSAGE = 'There was some problem resolving the ticket. Please try again later.'
ALREADY_CLOSED_OR_RAISED = 'This ticket cannot be closed as either it is already closed or still in raised condition.'
CLOSE_TICKET_ERROR_MESSAGE = 'There was some problem closing the ticket. Please try again later.'


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
                        logger.error(f"Invalid ticket id provided: {t_id}")
                        raise ApplicationError(code=404, message=INVALID_TICKET_NUMBER_MESSAGE)

                    # Ticket is already closed or in_progress
                    if ticket['t_status'] == DBConfig.IN_PROGRESS or ticket['t_status'] == DBConfig.CLOSED:
                        logger.error(f"User tried to resolve an already resolved ticket for Ticket Id: {t_id}")
                        raise ApplicationError(code=400, message=ALREADY_RESOLVED_OR_CLOSED)

                    with EmployeeDAO(conn) as e_dao:
                        dept_id = e_dao.get_department_by_employee_id(identity)
                        if dept_id['dept_id'] != ticket['d_id']:
                            logger.error(f"There was an error while resolving a ticket{t_id} {e.msg}")
                            raise ApplicationError(code=403, message=UNAUTHORIZED_MESSAGE)

                    t_dao.assign_repr_id(t_id, identity)
                    t_dao.change_ticket_status(t_id, DBConfig.IN_PROGRESS)
                    t_dao.update_message_from_helpdesk(ticket_data['message_from_helpdesk'], t_id)

        except Error as e:
            logger.error(f"There was an error while resolving a ticket{t_id} {e.msg}")
            raise DataBaseException(RESOLVE_TICKET_ERROR_MESSAGE)

    @staticmethod
    def close_ticket(t_id, ticket_data, identity):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)
                    # Invalid t_id provided
                    if ticket is None:
                        logger.error(f"Invalid ticket id provided: {t_id}")
                        raise ApplicationError(code=404, message=INVALID_TICKET_NUMBER_MESSAGE)

                    # Ticket is already closed or in raised condition
                    if ticket['t_status'] == DBConfig.RAISED or ticket['t_status'] == DBConfig.CLOSED:
                        logger.error(f"User tried to resolve an already closed or just raised ticket for Ticket Id: {t_id}")
                        raise ApplicationError(code=400, message=ALREADY_CLOSED_OR_RAISED)

                    with EmployeeDAO(conn) as e_dao:
                        dept_id = e_dao.get_department_by_employee_id(identity)
                        if dept_id['dept_id'] != ticket['d_id']:
                            logger.error(f"There was an error while closing a ticket{t_id} {e.msg}")
                            raise ApplicationError(code=403, message=UNAUTHORIZED_MESSAGE)

                    t_dao.change_ticket_status(t_id, DBConfig.CLOSED)
                    t_dao.update_message_from_helpdesk(ticket_data['message_from_helpdesk'], t_id)

        except Error as e:
            logger.error(f"There was an error while closing a ticket{t_id} {e.msg}")
            raise DataBaseException(CLOSE_TICKET_ERROR_MESSAGE)
