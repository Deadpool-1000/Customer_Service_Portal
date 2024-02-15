import logging

from flask import current_app
from mysql.connector import Error

from src.dbutils.connection import DatabaseConnection
from src.dbutils.customer.feedback_dao import FeedbackDAO
from src.dbutils.message.message_dao import MessageDAO
from src.dbutils.ticket.ticket_dao import TicketDAO
from src.utils.exceptions import DataBaseException, ApplicationError

logger = current_app.logger


class MessageHandler:
    @staticmethod
    def update_message_from_manager(message, t_id):
        """Register message from manager.
        If no message is previously given then, it generates a new message,
        else it overwrites the previous message."""
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket_and_feedback = t_dao.get_ticket_and_feedback(t_id)

                if ticket_and_feedback is None:
                    current_app.logger.error(f"Update message: Invalid ticket Identification number provided")
                    raise ApplicationError(code=404,
                                           message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])
                with MessageDAO(conn) as m_dao:
                    m_dao.update_message_from_manager(t_id, message)

            """
                    if ticket['t_status'] != current_app.config['CLOSED']:
                        current_app.logger.error(
                            "Update message: Tried to add message from manager on an unclosed ticket.")
                        raise ApplicationError(code=400,
                                               message=current_app.config['CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE'])
                   
                    
                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

                    if feedback is None:
                        current_app.logger.error(
                            "Update message: Tried to add message from manager on a ticket with no feedback.")
                        raise ApplicationError(code=404,
                                               message=current_app.config['CANNOT_GIVE_MESSAGE_FOR_TICKET_MESSAGE'])
            """



        except Error as e:
            logger.error(
                f'Update message: There was some problem while registering message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(current_app.config['UPDATE_MESSAGE_ERROR_MESSAGE'])

    @staticmethod
    def get_message_from_manager(identity, role, t_id):
        """Fetches message from manager for ticket with identification t_id"""
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket_and_message = t_dao.get_ticket_and_message(t_id)

            if ticket_and_message is None:
                current_app.logger.error(f"Get message: Invalid ticket Identification number provided")
                raise ApplicationError(code=404,
                                       message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

            if role == current_app.config['HELPDESK'] and ticket_and_message['repr_id'] != identity:
                current_app.logger.error(
                    f"Get message: Helpdesk {identity} tried to access message on a ticket, he/she does not have access to.")
                raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

            """
                with MessageDAO(conn) as m_dao:
                    message_from_manager = m_dao.get_message_from_manager(t_id)

            if message_from_manager is None:
                raise ApplicationError(code=404, message=current_app.config['NO_MESSAGE_FOUND_MESSAGE'])
            """

            return {
                'ticket_id': ticket_and_message['t_id'],
                'message': ticket_and_message['message'],
                'created_at': ticket_and_message['created_at']
            }

        except Error as e:
            logger.error(
                f'Get message: There was some problem while getting message from manager for ticket: {t_id}. Error {e}')
            raise DataBaseException(current_app.config['FETCH_MESSAGE_ERROR_MESSAGE'])
