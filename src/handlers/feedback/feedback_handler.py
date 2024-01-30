import logging
from mysql.connector import Error

from src.DBUtils.connection import DatabaseConnection
from src.DBUtils.customer import FeedbackDAO
from src.DBUtils.ticket import TicketDAO
from src.utils.exceptions import ApplicationError, DataBaseException
from src.DBUtils.config.db_config_loader import DBConfig
from src.handlers import CSMConfig

logger = logging.getLogger('main.feedback_handler')


class FeedbackHandler:
    @staticmethod
    def add_feedback_for_ticket(c_id, stars, description, t_id):
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)
                    if ticket is None:
                        raise ApplicationError(code=404, message='Invalid Ticket Identification provided')

                    if ticket['c_id'] != c_id:
                        raise ApplicationError(code=403, message='You are not authorized to use this resource.')

                    if ticket['t_status'] != DBConfig.CLOSED:
                        raise ApplicationError(code=400, message='The ticket is not closed. So feedback cannot be registered.')

                with FeedbackDAO(conn) as f_dao:
                    f_dao.add_feedback(stars, description, t_id)

        except Error as e:
            logger.error(f'Error while adding feedback for ticket {t_id}. Error {e}')
            raise DataBaseException('There was some problem while registering the feedback.')

    @staticmethod
    def get_feedback_for_ticket(t_id):
        try:
            with DatabaseConnection() as conn:
                with FeedbackDAO(conn) as f_dao:
                    feedback = f_dao.get_feedback_by_tid(t_id)

            if feedback is None:
                raise ApplicationError(code=404, message='No message for this ticket.')

            return feedback
        except Error as e:
            logger.error(f'Error while getting feedback for ticket:{t_id}. Error {e}')
            raise DataBaseException('There was some problem while getting the feedback')

    @staticmethod
    def access_allowed(identity, role, t_id):
        if role == CSMConfig.MANAGER:
            return True

        with DatabaseConnection() as conn:
            with TicketDAO(conn) as t_dao:
                ticket = t_dao.get_ticket_by_tid(t_id)

        if identity == ticket['c_id']:
            return True

        return False
