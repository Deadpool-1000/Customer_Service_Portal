import hashlib
import logging

import shortuuid
from flask import current_app

logger = current_app.logger


class AuthDAO:
    singleton = 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_CUST_AUTH'])
            self.cur.execute(current_app.config['CREATE_TABLE_EMP'])
            logger.debug("AuthDAO: customer auth and employee auth table created")
            self.singleton -= 1

    def find_user(self, email, table_name):
        """Searches in table with name: table_name and returns user with email address: email"""
        self.cur.execute(current_app.config['FIND_USER_QUERY'].format(table_name), {
            'email': email
        })
        logger.debug(f"AuthDAO: tried to fetch user with email {email} in table {table_name}")
        return self.cur.fetchone()

    def add_customer_auth_details(self, email, password) -> str:
        """Add customer authentication data to the cust_auth table"""
        cust_id = shortuuid.ShortUUID().random(5)
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        self.cur.execute(current_app.config['INSERT_INTO_CUSTOMER_AUTH_TABLE'], (cust_id, email, hashed_password))
        logger.debug(f"AuthDAO: Customer auth details added for email {email}")
        return cust_id
