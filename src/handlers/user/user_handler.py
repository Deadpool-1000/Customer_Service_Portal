import pymysql
from flask import current_app

from src.dbutils.auth.auth_dao import AuthDAO
from src.dbutils.connection import DatabaseConnection
from src.utils.exceptions import DataBaseException

logger = current_app.logger


class UserHandler:
    @staticmethod
    def get_profile(user_id, role):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    return a_dao.get_user_profile(user_id, role)
        except pymysql.Error as e:
            logger.error(f'Profile: Database error {e.args[0]}: {e.args[1]} while fetching profile for user: {user_id}, {role}')
            raise DataBaseException(current_app.config['PROFILE_FETCH_ERROR_MESSAGE'])

    @staticmethod
    def put_customer_profile(new_user_data):
        try:
            with DatabaseConnection() as conn:
                with AuthDAO(conn) as a_dao:
                    a_dao.put_customer_profile(new_user_data)
        except pymysql.Error as e:
            logger.error(f'Profile: Database error {e.args[0]}: {e.args[1]} while updating profile for user: {new_user_data}')
            raise DataBaseException(current_app.config['PROFILE_UPDATE_ERROR_MESSAGE'])
