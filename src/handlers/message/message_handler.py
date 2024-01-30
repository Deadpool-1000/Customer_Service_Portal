import logging
from mysql.connector import Error

from src.DBUtils.connection import DatabaseConnection
from src.DBUtils.message.messagedao import MessageDAO
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.DBUtils.customer.feedbackdao import FeedbackDAO
from src.utils.exceptions import DataBaseException, ApplicationError
from src.handlers.config.csm_config import CSMConfig
from src.DBUtils.config.db_config_loader import DBConfig


logger = logging.getLogger('main.message_handler')

CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE = 'You cannot give message for this ticket.'
INVALID_TICKET_NUMBER_MESSAGE = 'Invalid Ticket Identification Number provided.'
UPDATE_MESSAGE_ERROR_MESSAGE = 'There was some problem updating your message.'
UNAUTHORIZED_MESSAGE = 'You are not authorized to use this resource.'
NO_MESSAGE_FOUND_MESSAGE = 'There is no message for the ticket.'
FETCH_MESSAGE_ERROR_MESSAGE = 'There was some problem getting your message'


class MessageHandler:
    @staticmethod
    def update_message_from_manager(message, t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)

                    if ticket is None:
                        raise ApplicationError(code=404, message=INVALID_TICKET_NUMBER_MESSAGE)

                    if ticket['t_status'] != DBConfig.CLOSED:
                        raise ApplicationError(code=400, message=CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE)

                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

                    if feedback is None:
                        raise ApplicationError(code=404, message=CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE)

                with MessageDAO(conn) as m_dao:
                    m_dao.update_message_from_manager(t_id, message)

        except Error as e:
            logger.error(f'There was some problem while registering message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(UPDATE_MESSAGE_ERROR_MESSAGE)

    @staticmethod
    def get_message_from_manager(identity, role, t_id):
        try:
            with DatabaseConnection() as conn:
                if role == CSMConfig.HELPDESK:
                    with TicketDAO(conn) as t_dao:
                        ticket = t_dao.get_ticket_by_tid(t_id)

                        if ticket is None:
                            raise ApplicationError(code=404, message=INVALID_TICKET_NUMBER_MESSAGE)

                        if ticket['repr_id'] != identity:
                            raise ApplicationError(code=403, message=UNAUTHORIZED_MESSAGE)

                with MessageDAO(conn) as m_dao:
                    message_from_manager = m_dao.get_message_from_manager(t_id)

            if message_from_manager is None:
                raise ApplicationError(code=404, message=NO_MESSAGE_FOUND_MESSAGE)

            return message_from_manager

        except Error as e:
            logger.error(f'There was some problem while getting message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(FETCH_MESSAGE_ERROR_MESSAGE)
