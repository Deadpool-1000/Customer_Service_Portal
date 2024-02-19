import pymysql
from flask import current_app

from src.dbutils.connection import DatabaseConnection
from src.dbutils.customer import FeedbackDAO
from src.dbutils.ticket import TicketDAO
from src.utils.exceptions import ApplicationError, DataBaseException


class FeedbackHandler:
    @staticmethod
    def update_feedback_for_ticket(c_id, stars, description, t_id):
        """
        Register feedback for a particular ticket
        Three verification steps are performed:
            1. Ticket identification number is checked.
            2. Check if the customer identification matches the id number of the creator.
            3. Check if the ticket status is closed.
        """
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket = t_dao.get_ticket_by_tid(t_id)

                if ticket is None:
                    current_app.logger.error(f"Add Feedback: Invalid Ticket Identification number {t_id}")
                    raise ApplicationError(code=404,
                                           message=current_app.config['INVALID_TICKET_NUMBER_ERROR_MESSAGE'])

                if ticket['c_id'] != c_id:
                    current_app.logger.error(
                        f"Add Feedback: Customer {c_id}, tried to access ticket {t_id} not belonging to him/her.")
                    raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

                if ticket['t_status'] != current_app.config['CLOSED']:
                    current_app.logger.error(
                        f"Add Feedback: Customer {c_id}, tried to add feedback for an unclosed ticket {t_id}")
                    raise ApplicationError(code=400, message=current_app.config['TICKET_NOT_CLOSED_MESSAGE'])

                with FeedbackDAO(conn) as f_dao:
                    f_dao.add_feedback(stars, description, t_id)

        except pymysql.Error as e:
            current_app.logger.error(f'Error while adding feedback for ticket {t_id}. Error {e.args[0]}: {e.args[1]}')
            raise DataBaseException(current_app.config['FEEDBACK_REGISTER_ERROR_MESSAGE'])

    @staticmethod
    def get_feedback_for_ticket(identity, role, t_id):
        """
        Fetches feedback for a particular ticket with ticket identification number t_id.
        Also verifies if the role and identity is allowed to view the ticket.
        Raises HTTPException if the feedback for that ticket is empty.
        """
        try:
            with DatabaseConnection() as conn:
                with TicketDAO(conn) as t_dao:
                    ticket_and_feedback = t_dao.get_ticket_and_feedback(t_id)

            if ticket_and_feedback is None:
                raise ApplicationError(code=404, message=current_app.config['NO_FEEDBACK_ERROR_MESSAGE'])

            if role == current_app.config['HELPDESK'] and ticket_and_feedback['repr_id'] != identity:
                current_app.logger.error(f"Identity {identity} and role {role} tried to access feedback for ticket {t_id} for which they are not allowed")
                raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

            if role == current_app.config['CUSTOMER'] and ticket_and_feedback['c_id'] != identity:
                current_app.logger.error(f"Identity {identity} and role {role} tried to access feedback for ticket {t_id} for which they are not allowed")
                raise ApplicationError(code=403, message=current_app.config['UNAUTHORIZED_ERROR_MESSAGE'])

            return {
                'ticket_id': ticket_and_feedback['t_id'],
                'stars': ticket_and_feedback['stars'],
                'description': ticket_and_feedback['description'],
                'created_on': ticket_and_feedback['created_on']
            }
        except pymysql.Error as e:
            current_app.logger.error(f'Error while getting feedback for ticket:{t_id}. Error {e}')
            raise DataBaseException(current_app.config['FEEDBACK_FETCH_ERROR_MESSAGE'])
