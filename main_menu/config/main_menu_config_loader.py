import yaml

MAIN_MENU_CONFIG_FILE_PATH = 'config_files/main_menu.yml'


class MainMenuConfig:
    COMPANY_LOGO = None
    MAIN_PROMPT = None
    EMPLOYEE_MAIN_MENU = None
    CUSTOMER_WELCOME_MESSAGE = None
    CUSTOMER_MAIN_MENU = None
    SIGNUP_TO_LOGIN_PROMPT = None
    PLEASE_TRY_AGAIN = None
    CUSTOMER_SIGNUP_WELCOME_MESSAGE = None
    CUSTOMER_LOGIN_WELCOME_MESSAGE = None
    SOME_PROBLEM = None
    TRY_AGAIN_OR_QUIT = None
    HELPDESK = None
    MANAGER = None

    @classmethod
    def load(cls):
        with open(MAIN_MENU_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.COMPANY_LOGO = data['COMPANY_LOGO']
            cls.MAIN_PROMPT = data['MAIN_PROMPT']
            cls.EMPLOYEE_MAIN_MENU = data['EMPLOYEE_MAIN_MENU']
            cls.CUSTOMER_WELCOME_MESSAGE = data['CUSTOMER_WELCOME_MESSAGE']
            cls.CUSTOMER_MAIN_MENU = data['CUSTOMER_MAIN_MENU']
            cls.SIGNUP_TO_LOGIN_PROMPT = data['SIGNUP_TO_LOGIN_PROMPT']
            cls.PLEASE_TRY_AGAIN = data['PLEASE_TRY_AGAIN']
            cls.CUSTOMER_SIGNUP_WELCOME_MESSAGE = data['CUSTOMER_SIGNUP_WELCOME_MESSAGE']
            cls.CUSTOMER_LOGIN_WELCOME_MESSAGE = data['CUSTOMER_LOGIN_WELCOME_MESSAGE']
            cls.SOME_PROBLEM = data['SOME_PROBLEM']
            cls.TRY_AGAIN_OR_QUIT = data['TRY_AGAIN_OR_QUIT']
            cls.HELPDESK = data['HELPDESK']
            cls.MANAGER = data['MANAGER']
