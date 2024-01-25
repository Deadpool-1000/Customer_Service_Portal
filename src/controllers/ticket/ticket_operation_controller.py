from flask_smorest import abort
from src.handlers.ticket.ticket_operation_handler import TicketOperationHandler
from src.utils.exceptions import DataBaseException, ApplicationError


class TicketOperationController:
    @staticmethod
    def resolve_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.resolve_ticket(ticket_id, ticket_data, identity)
            return {
                "message": "Resolved Successfully."
            }
        except DataBaseException:
            abort(500, message="There was some problem resolving the ticket. Please try again later.")

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

    @staticmethod
    def close_ticket(ticket_data, ticket_id, identity):
        try:
            TicketOperationHandler.close_ticket(ticket_id, ticket_data, identity)

            return {
                "message": "Closed Successfully."
            }

        except DataBaseException:
            abort(500, message="There was some problem closing the ticket. Please try again later.")

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)
