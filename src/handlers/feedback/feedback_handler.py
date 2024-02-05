import logging
from flask import current_app
from mysql.connector import Error

from src.dbutils.connection import DatabaseConnection
from src.dbutils.customer import FeedbackDAO
from src.dbutils.ticket import TicketDAO
from src.utils.exceptions import ApplicationError, DataBaseException


logger = logging.getLogger('main.feedback_handler')


class FeedbackHandler:
    @staticmethod
    def add_feedback_for_ticket(c_id, stars, description, t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)
                    if ticket is None:
                        raise ApplicationError(code=404, message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                    if ticket['c_id'] != c_id:
                        raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

                    if ticket['t_status'] != current_app.config['CLOSED']:
                        raise ApplicationError(code=400, message=current_app.config['TICKET_NOT_CLOSED_MESSAGE'])

                with FeedbackDAO(conn) as f_dao:
                    f_dao.add_feedback(stars, description, t_id)

        except Error as e:
            logger.error(f'Error while adding feedback for ticket {t_id}. Error {e}')
            raise DataBaseException(current_app.config['FEEDBACK_REGISTER_ERROR_MESSAGE'])

    @staticmethod
    def get_feedback_for_ticket(t_id):
        try:
            with DatabaseConnection() as conn:
                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

            if feedback is None:
                raise ApplicationError(code=404, message=current_app.config['NO_FEEDBACK_ERROR_MESSAGE'])

            return feedback
        except Error as e:
            logger.error(f'Error while getting feedback for ticket:{t_id}. Error {e}')
            raise DataBaseException(current_app.config['FEEDBACK_FETCH_ERROR_MESSAGE'])

    @staticmethod
    def access_allowed(identity, role, t_id):
        if role == current_app.config['MANAGER']:
            return True

        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                ticket = t_dao.get_ticket_by_tid(t_id)

        if identity == ticket['c_id']:
            return True

        return False
