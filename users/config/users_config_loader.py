import yaml

USERS_CONFIG_FILE_PATH = 'users/config/users.yml'


class UsersConfig:
    COMPANY_LOGO = None
    CUSTOMER_WELCOME_MENU = None
    CUSTOMER_MENU = None
    TICKET_RAISED_SUCCESS = None
    HELPDESK_PROMPT = None
    WELCOME_MESSAGE = None
    MANAGER_PROMPT = None
    MANAGER_WELCOME_MESSAGE = None
    FEEDBACK_HANDLER_TITLE = None
    EMPTY_FEEDBACKS = None
    FEEDBACK_PROMPT = None
    FEEDBACK_CONTINUE_PROMPT = None
    END_OF_FEEDBACKS = None

    @classmethod
    def load(cls):
        with open(USERS_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.COMPANY_LOGO = data['COMPANY_LOGO']
            cls.CUSTOMER_WELCOME_MENU = data['CUSTOMER_WELCOME_MENU']
            cls.CUSTOMER_MENU = data['CUSTOMER_MENU']
            cls.TICKET_RAISED_SUCCESS = data['TICKET_RAISED_SUCCESS']
            cls.HELPDESK_PROMPT = data['HELPDESK_PROMPT']
            cls.WELCOME_MESSAGE = data['WELCOME_MESSAGE']
            cls.MANAGER_PROMPT = data['MANAGER_PROMPT']
            cls.MANAGER_WELCOME_MESSAGE = data['MANAGER_WELCOME_MESSAGE']
            cls.FEEDBACK_HANDLER_TITLE = data['FEEDBACK_HANDLER_TITLE']
            cls.EMPTY_FEEDBACKS = data['EMPTY_FEEDBACKS']
            cls.FEEDBACK_PROMPT = data['FEEDBACK_PROMPT']
            cls.FEEDBACK_CONTINUE_PROMPT = data['FEEDBACK_CONTINUE_PROMPT']
            cls.END_OF_FEEDBACKS = data['END_OF_FEEDBACKS']
