from flask import current_app
import logging


logger = logging.getLogger('main.customer_dao')


class CustomerDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_CUST_DETAILS'])
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def add_customer_details(self, cust_id, fullname, phn_num, address):
        self.cur.execute(current_app.config['INSERT_INTO_CUST_DETAILS'], (cust_id, fullname, phn_num, address))
