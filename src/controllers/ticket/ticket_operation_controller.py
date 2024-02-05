from flask import current_app
from flask_smorest import abort

from src.handlers.ticket.ticket_operation_handler import TicketOperationHandler
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketOperationController:
    @staticmethod
    def resolve_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.resolve_ticket(ticket_id, ticket_data, identity)
            return {
                "message": current_app.config['RESOLVED_SUCCESS_MESSAGE']
            }

        except DataBaseException as db:
            abort(500, message=str(db))

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

    @staticmethod
    def close_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.close_ticket(ticket_id, ticket_data, identity)

            return {
                "message": current_app.config['CLOSED_SUCCESS_MESSAGE']
            }

        except DataBaseException as db:
            abort(500, message=str(db))

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)
