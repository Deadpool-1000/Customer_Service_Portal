import logging

from flask import current_app

logger = current_app.logger


class CustomerDAO:
    """Context manager that can be used to perform operation on customer's data. On exit it closes the cursor."""
    singleton = 1

    def __init__(self, conn):
        """Expects database connection and creates a cursor from it."""
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(current_app.config['CREATE_TABLE_CUST_DETAILS'])
            logger.debug("CustomerDAO: Customer details table created.")
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False
        self.cur.close()

    def add_customer_details(self, cust_id, fullname, phn_num, address):
        """Add customer details to the database"""
        logger.debug(f"CustomerDAO: Customer details added cust_id {cust_id} full name {fullname} phone number {phn_num} address {address}")
        self.cur.execute(current_app.config['INSERT_INTO_CUST_DETAILS'], (cust_id, fullname, phn_num, address))
