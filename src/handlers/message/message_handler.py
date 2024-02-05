import logging
from flask import current_app
from mysql.connector import Error

from src.dbutils.connection import DatabaseConnection
from src.dbutils.message.messagedao import MessageDAO
from src.dbutils.ticket.ticketDAO import TicketDAO
from src.dbutils.customer.feedbackdao import FeedbackDAO
from src.utils.exceptions import DataBaseException, ApplicationError


logger = logging.getLogger('main.message_handler')


class MessageHandler:
    @staticmethod
    def update_message_from_manager(message, t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)

                    if ticket is None:
                        raise ApplicationError(code=404, message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    if ticket['t_status'] != current_app.config['CLOSED']:
                        raise ApplicationError(code=400, message=current_app.config['CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE'])

                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

                    if feedback is None:
                        raise ApplicationError(code=404, message=current_app.config['CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE'])

                with MessageDAO(conn) as m_dao:
                    m_dao.update_message_from_manager(t_id, message)

        except Error as e:
            logger.error(f'There was some problem while registering message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(current_app.config['UPDATE_MESSAGE_ERROR_MESSAGE'])

    @staticmethod
    def get_message_from_manager(identity, role, t_id):
        try:
            with DatabaseConnection() as conn:
                if role == current_app.config['HELPDESK']:
                    with TicketDAO(conn) as t_dao:
                        ticket = t_dao.get_ticket_by_tid(t_id)

                        if ticket is None:
                            raise ApplicationError(code=404, message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                        if ticket['repr_id'] != identity:
                            raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

                with MessageDAO(conn) as m_dao:
                    message_from_manager = m_dao.get_message_from_manager(t_id)

            if message_from_manager is None:
                raise ApplicationError(code=404, message=current_app.config['NO_MESSAGE_FOUND_MESSAGE'])

            return message_from_manager

        except Error as e:
            logger.error(f'There was some problem while getting message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(current_app.config['FETCH_MESSAGE_ERROR_MESSAGE'])
