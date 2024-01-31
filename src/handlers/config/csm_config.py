from os import path
import yaml

path_current_directory = path.dirname(__file__)
AUTH_CONFIG_FILE_PATH = path.join(path_current_directory, 'csm.yml')


class CSMConfig:
    EMP_AUTH = None
    CUST_AUTH = None
    PLEASE_TRY_AGAIN = None
    HELPDESK = None
    MANAGER = None
    CUSTOMER = None
    IN_PROGRESS = None
    RAISED = None
    CLOSED = None
    REGISTER_SUCCESS_MESSAGE = None
    LOGIN_ERROR_MESSAGE = None
    LOGOUT_SUCCESS_MESSAGE = None
    FEEDBACK_REGISTERED_SUCCESS= None
    UNAUTHORIZED_ERROR_MESSAGE = None
    MESSAGE_UPDATE_SUCCESS_MESSAGE = None
    INVALID_DEPARTMENT_ERROR_MESSAGE = None
    # DEFAULT_MESSAGE_FROM_HELPDESK= None
    CREATE_TICKET_ERROR_MESSAGE = None
    DETAILED_TICKET_ERROR_MESSAGE = None
    RESOLVED_SUCCESS_MESSAGE = None
    RESOLVED_ERROR_MESSAGE = None
    CLOSED_SUCCESS_MESSAGE = None
    CLOSED_ERROR_MESSAGE = None

    @classmethod
    def load(cls):
        with open(AUTH_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.EMP_AUTH = data['EMP_AUTH']
            cls.CUST_AUTH = data['CUST_AUTH']
            cls.PLEASE_TRY_AGAIN = data['PLEASE_TRY_AGAIN']
            cls.HELPDESK = data['HELPDESK']
            cls.MANAGER = data['MANAGER']
            cls.CUSTOMER = data['CUSTOMER']
            cls.IN_PROGRESS = data['IN_PROGRESS']
            cls.RAISED = data['RAISED']
            cls.CLOSED = data['CLOSED']
            cls.REGISTER_SUCCESS_MESSAGE = data['REGISTER_SUCCESS_MESSAGE']
            cls.LOGIN_ERROR_MESSAGE = data['LOGIN_ERROR_MESSAGE']
            cls.LOGOUT_SUCCESS_MESSAGE = data['LOGOUT_SUCCESS_MESSAGE']
            cls.FEEDBACK_REGISTERED_SUCCESS = data['FEEDBACK_REGISTERED_SUCCESS']
            cls.UNAUTHORIZED_ERROR_MESSAGE = data['UNAUTHORIZED_ERROR_MESSAGE']
            cls.MESSAGE_UPDATE_SUCCESS_MESSAGE = data['MESSAGE_UPDATE_SUCCESS_MESSAGE']
            cls.INVALID_DEPARTMENT_ERROR_MESSAGE = data['INVALID_DEPARTMENT_ERROR_MESSAGE']
            # csl.DEFAULT_MESSAGE_FROM_HELPDESK = data['DEFAULT_MESSAGE_FROM_HELPDESK']
            cls.CREATE_TICKET_ERROR_MESSAGE = data['CREATE_TICKET_ERROR_MESSAGE']
            cls.DETAILED_TICKET_ERROR_MESSAGE = data['DETAILED_TICKET_ERROR_MESSAGE']
            cls.RESOLVED_SUCCESS_MESSAGE = data['RESOLVED_SUCCESS_MESSAGE']
            cls.RESOLVED_ERROR_MESSAGE = data['RESOLVED_ERROR_MESSAGE']
            cls.CLOSED_SUCCESS_MESSAGE = data['CLOSED_SUCCESS_MESSAGE']
            cls.CLOSED_ERROR_MESSAGE = data['CLOSED_ERROR_MESSAGE']