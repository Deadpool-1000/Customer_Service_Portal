from flask_smorest import abort

from src.handlers import CSMConfig
from src.handlers.ticket.ticket_operation_handler import TicketOperationHandler
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketOperationController:
    @staticmethod
    def resolve_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.resolve_ticket(ticket_id, ticket_data, identity)
            return {
                "message": CSMConfig.RESOLVED_SUCCESS_MESSAGE
            }
        except DataBaseException:
            abort(500, message=CSMConfig.RESOLVED_ERROR_MESSAGE)

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

    @staticmethod
    def close_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.close_ticket(ticket_id, ticket_data, identity)

            return {
                "message": CSMConfig.CLOSED_SUCCESS_MESSAGE
            }

        except DataBaseException:
            abort(500, message=CSMConfig.CLOSED_ERROR_MESSAGE)

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)
