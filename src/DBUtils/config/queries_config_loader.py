from os import path

import yaml

path_current_directory = path.dirname(__file__)
QUERIES_CONFIG_FILE_PATH = path.join(path_current_directory, 'queries.yml')


class QueriesConfig:
    CREATE_TABLE_CUST_AUTH = None
    CREATE_TABLE_EMP = None
    FIND_USER_QUERY = None
    FIND_DEPT_BY_DEPTID = None
    INSERT_INTO_CUSTOMER_AUTH_TABLE = None
    CREATE_TABLE_CUST_DETAILS = None
    INSERT_INTO_CUST_DETAILS = None
    CREATE_TABLE_FEEDBACK = None
    INSERT_INTO_TICKETS = None
    GET_ALL_FEEDBACK = None
    GET_CUST_DETAILS_BY_ID = None
    CREATE_TABLE_DEPT_DETAILS = None
    CREATE_TABLE_EMP_DETAILS = None
    GET_EMPLOYEE_DETAILS_BY_ID = None
    DEPT_TABLE_MAPPING_QUERY = None
    GET_DEPT_DETAILS_BY_ID = None
    CREATE_TABLE_TICKETS = None
    INSERT_INTO_TICKETS_TABLE = None
    VIEW_TICKETS = None
    VIEW_TICKETS_BY_STATUS = None
    VIEW_ALL_TICKETS = None
    UPDATE_MESSAGE_FROM_HELPDESK = None
    UPDATE_TICKET_STATUS = None
    ASSIGN_REPR = None

    @classmethod
    def load(cls):
        with open(QUERIES_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.CREATE_TABLE_CUST_AUTH = data['CREATE_TABLE_CUST_AUTH']
            cls.CREATE_TABLE_EMP = data['CREATE_TABLE_EMP']
            cls.FIND_USER_QUERY = data['FIND_USER_QUERY']
            cls.FIND_DEPT_BY_DEPTID = data['FIND_DEPT_BY_DEPTID']
            cls.INSERT_INTO_CUSTOMER_AUTH_TABLE = data['INSERT_INTO_CUSTOMER_AUTH_TABLE']
            cls.CREATE_TABLE_CUST_DETAILS = data['CREATE_TABLE_CUST_DETAILS']
            cls.GET_CUST_DETAILS_BY_ID = data['GET_CUST_DETAILS_BY_ID']
            cls.INSERT_INTO_CUST_DETAILS = data['INSERT_INTO_CUST_DETAILS']
            cls.CREATE_TABLE_FEEDBACK = data['CREATE_TABLE_FEEDBACK']
            cls.INSERT_INTO_TICKETS = data['INSERT_INTO_TICKETS']
            cls.GET_ALL_FEEDBACK = data['GET_ALL_FEEDBACK']
            cls.GET_CUST_DETAILS_BY_ID = data['GET_CUST_DETAILS_BY_ID']
            cls.CREATE_TABLE_DEPT_DETAILS = data['CREATE_TABLE_DEPT_DETAILS']
            cls.CREATE_TABLE_EMP_DETAILS = data['CREATE_TABLE_EMP_DETAILS']
            cls.GET_EMPLOYEE_DETAILS_BY_ID = data['GET_EMPLOYEE_DETAILS_BY_ID']
            cls.DEPT_TABLE_MAPPING_QUERY = data['DEPT_TABLE_MAPPING_QUERY']
            cls.GET_DEPT_DETAILS_BY_ID = data['GET_DEPT_DETAILS_BY_ID']
            cls.CREATE_TABLE_TICKETS = data['CREATE_TABLE_TICKETS']
            cls.INSERT_INTO_TICKETS_TABLE = data['INSERT_INTO_TICKETS_TABLE']
            cls.VIEW_TICKETS = data['VIEW_TICKETS']
            cls.VIEW_TICKETS_BY_STATUS = data['VIEW_TICKETS_BY_STATUS']
            cls.VIEW_ALL_TICKETS = data['VIEW_ALL_TICKETS']
            cls.UPDATE_MESSAGE_FROM_HELPDESK = data['UPDATE_MESSAGE_FROM_HELPDESK']
            cls.UPDATE_TICKET_STATUS = data['UPDATE_TICKET_STATUS']
            cls.ASSIGN_REPR = data['ASSIGN_REPR']
