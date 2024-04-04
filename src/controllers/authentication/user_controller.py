from src.handlers.user.user_handler import UserHandler


class UserController:
    @staticmethod
    def get_profile(user_id, role):
        return UserHandler.get_profile(user_id, role)