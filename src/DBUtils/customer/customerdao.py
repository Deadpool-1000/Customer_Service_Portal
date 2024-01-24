import logging

from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.utils.exceptions.exceptions import InvalidCustomerIDException

logger = logging.getLogger('main.customer_dao')


class CustomerDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor(dictionary=True)
        if self.singleton != 0:
            self.cur.execute(QueriesConfig.CREATE_TABLE_CUST_DETAILS)
            self.singleton -= 1

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_val or exc_tb:
            return False

        self.cur.close()

    def get_customer_details_by_id(self, cust_id):
        rws = self.cur.execute(QueriesConfig.GET_CUST_DETAILS_BY_ID, (cust_id,)).fetchone()
        if rws is None:
            logger.info(DBConfig.INVALID_CUST_ID)
            raise InvalidCustomerIDException(DBConfig.INVALID_CUST_ID)
        # 'c_id', 'full_name', 'phn_num', 'address'
        return rws

    def add_customer_details(self, cust_id, fullname, phn_num, address):
        self.cur.execute(QueriesConfig.INSERT_INTO_CUST_DETAILS, (cust_id, fullname, phn_num, address))
