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


class MessageHandler:
    @staticmethod
    def update_message_from_manager(message, t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)

                    if ticket is None:
                        raise ApplicationError(code=404, message='No such ticket found.')

                    if ticket['t_status'] != DBConfig.CLOSED:
                        raise ApplicationError(code=400, message='You cannot give message for this ticket.')

                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

                    if feedback is None:
                        raise ApplicationError(code=404, message='You cannot give message for this ticket.')

                with MessageDAO(conn) as m_dao:
                    m_dao.update_message_from_manager(t_id, message)

        except Error as e:
            logger.error(f'There was some problem while registering message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException('There was some problem updating your message')

    @staticmethod
    def get_message_from_manager(identity, role, t_id):
        try:
            with DatabaseConnection() as conn:
                if role == CSMConfig.HELPDESK:
                    with TicketDAO(conn) as t_dao:
                        ticket = t_dao.get_ticket_by_tid(t_id)

                        if ticket is None:
                            raise ApplicationError(code=404, message='No such ticket found.')

                        if ticket['repr_id'] != identity:
                            raise ApplicationError(code=403, message='You are not allowed to view this resource.')

                with MessageDAO(conn) as m_dao:
                    message_from_manager = m_dao.get_message_from_manager(t_id)

            if message_from_manager is None:
                raise ApplicationError(code=404, message='There is no message for the ticket.')

            return message_from_manager

        except Error as e:
            logger.error(f'There was some problem while getting message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException('There was some problem getting your message')
