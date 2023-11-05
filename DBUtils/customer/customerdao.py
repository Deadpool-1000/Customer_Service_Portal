import logging
from utils.exceptions import InvalidCustomerIDException

CREATE_TABLE_CUST_DETAILS = 'CREATE TABLE IF NOT EXISTS cust_details (cid TEXT PRIMARY KEY,full_name TEXT, phn_num TEXT,address TEXT, FOREIGN KEY(cid) REFERENCES cust_auth(cid))'
GET_CUST_DETAILS_BY_ID = 'SELECT * FROM cust_details WHERE cid = ?'
INSERT_INTO_CUST_DETAILS = 'INSERT INTO cust_details VALUES(?, ?, ?, ?)'
INVALID_CUST_ID = 'Invalid CustomerID(cid) Provided'

logger = logging.getLogger('main.customer_dao')


class CustomerDAO:
    singleton = 1

    def __init__(self, conn):
        self.cur = conn.cursor()
        if self.singleton != 0:
            self.cur.execute(CREATE_TABLE_CUST_DETAILS)
            self.singleton -= 1

    def get_customer_details_by_id(self, cust_id):
        rws = self.cur.execute(GET_CUST_DETAILS_BY_ID, (cust_id,)).fetchone()
        if rws is None:
            logger.info(INVALID_CUST_ID)
            raise InvalidCustomerIDException(INVALID_CUST_ID)
        # 'c_id', 'full_name', 'phn_num', 'address'
        return rws

    def add_customer_details(self, cust_id, fullname, phn_num, address):
        self.cur.execute(INSERT_INTO_CUST_DETAILS, (cust_id, fullname, phn_num, address))
