import hashlib
import shortuuid
from flask import current_app

from src.dbutils.base_dao import BaseDAO

logger = current_app.logger


class AuthDAO(BaseDAO):

    def find_user(self, email, table_name):
        """Searches in table with name: table_name and returns user with email address: email"""
        self.cur.execute(current_app.config['FIND_USER_QUERY'].format(table_name), {
            'email': email
        })
        logger.debug(f"AuthDAO: tried to fetch user with email {email} in table {table_name}")
        return self.cur.fetchone()

    def add_customer_auth_details(self, email, password):
        """Add customer authentication data to the cust_auth table"""
        cust_id = shortuuid.ShortUUID().random(5)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(current_app.config['INSERT_INTO_CUSTOMER_AUTH_TABLE'], (cust_id, email, hashed_password))
        logger.debug(f"AuthDAO: Customer auth details added for email {email}")
        return cust_id

    def add_token_to_blocklist(self, jti, exp):
        """Add token to blocklist"""
        print(current_app.config['REVOKED_TOKEN_INSERT'])
        self.cur.execute(current_app.config['REVOKED_TOKEN_INSERT'], (jti, exp))

    def clear_tokens(self):
        """Clear expired tokens in database"""
        print(current_app.config['CALL_CLEAR_BLOCKLIST_PROCEDURE'])
        self.cur.execute(current_app.config['CALL_CLEAR_BLOCKLIST_PROCEDURE'])

    def get_token_by_jti(self, jti):
        """Checks expired tokens in database"""
        self.cur.execute(current_app.config['GET_TOKEN_BY_JTI'], {
            'jti': jti
        })
        return self.cur.fetchone()

    def get_user_profile(self, user_id, role):
        """Fetch profile from database"""
        profile = {}
        if role == current_app.config['HELPDESK'] or role == current_app.config['MANAGER']:
            self.cur.execute(current_app.config['GET_EMPLOYEE_PROFILE'], {
                'user_id': user_id
            })
            profile = self.cur.fetchone()
            profile['role'] = current_app.config['HELPDESK_'] if role == current_app.config['HELPDESK'] else current_app.config['MANAGER_']
        elif role == current_app.config['CUSTOMER']:
            self.cur.execute(current_app.config['GET_CUSTOMER_PROFILE'], {
                'user_id': user_id
            })
            profile = self.cur.fetchone()
            profile['role'] = current_app.config['CUSTOMER__']

        return profile

    def put_customer_profile(self, new_user_data):
        """Update user Profile"""
        self.cur.execute(current_app.config['UPDATE_CUSTOMER_DETAIL'], {
            'address': new_user_data['address'],
            'phn_num': new_user_data['phn_num'],
            'full_name': new_user_data['full_name'],
            'c_id': new_user_data['c_id']
        })
        self.cur.execute(current_app.config['UPDATE_CUSTOMER_EMAIL'], {
            'email': new_user_data['email'],
            'c_id': new_user_data['c_id']
        })

