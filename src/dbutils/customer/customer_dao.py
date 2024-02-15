import logging

from flask import current_app

from src.dbutils.base_dao import BaseDAO

logger = current_app.logger


class CustomerDAO(BaseDAO):
    """Context manager that can be used to perform operation on customer's data. On exit it closes the cursor."""

    def add_customer_details(self, cust_id, fullname, phn_num, address):
        """Add customer details to the database"""
        logger.debug(f"CustomerDAO: Customer details added cust_id {cust_id} full name {fullname} phone number {phn_num} address {address}")
        self.cur.execute(current_app.config['INSERT_INTO_CUST_DETAILS'], (cust_id, fullname, phn_num, address))
