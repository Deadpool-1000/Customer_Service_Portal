from flask_smorest import abort

from src.handlers.message.message_handler import MessageHandler
from src.utils.exceptions import DataBaseException, ApplicationError


class MessageController:
    @staticmethod
    def update_message_from_manager(message_data, t_id):
        try:
            message = message_data['message_from_manager']
            MessageHandler.update_message_from_manager(message, t_id)
            return {
                'message': 'Message Updated Successfully.'
            }
        except DataBaseException as db:
            abort(500, message=db)

        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

    @staticmethod
    def get_message_from_manager(role, identity, t_id):
        try:
            message_from_manager = MessageHandler.get_message_from_manager(identity, role, t_id)
            return message_from_manager
        except ApplicationError as ae:
            abort(ae.code, message=ae.message)

        except DataBaseException as db:
            abort(500, message=db)
