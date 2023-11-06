import yaml

UTILS_CONFIG_FILE_PATH = 'config_files/utils.yml'


class UtilsConfig:
    EMAIL_PROMPT = None
    PASSWORD_PROMPT = None
    FULL_NAME_PROMPT = None
    PHONE_NUMBER_PROMPT = None
    ADDRESS_PROMPT = None
    PHONE_NUMBER_EMPTY = None
    ADDRESS_EMPTY = None
    FULLNAME_EMPTY = None
    EMAIL_EMPTY_PROMPT = None
    PASSWORD_EMPTY_PROMPT = None
    EMAIL_REGEX = None
    PASSWORD_REGEX = None
    STRONG_PASSWORD_PROMPT = None
    INVALID_INPUT = None
    INPUT_MESSAGE_FROM_HELPDESK = None
    MESSAGE_CANT_BE_EMPTY = None
    INPUT_FEEDBACK_STARS = None
    INPUT_FEEDBACK_DESC = None
    VALID_EMAIL = None
    TICKET_ID = None
    STATUS = None
    TITLE = None
    DESC = None
    END_OF_TICKETS = None
    NOT_VALID_EMAIL_PROMPT = None
    TICKET_DEPT_PROMPT = None
    INVALID_DEPT = None
    TICKET_TITLE_PROMPT = None
    TICKET_TITLE_EMPTY = None
    TICKET_DESC_PROMPT = None
    TICKET_DESC_EMPTY = None
    LINE_BREAK = None
    STARS = None
    MESSAGE_FROM_HELPDESK = None
    RAISED_ON = None
    DATE_FORMAT = None
    DEFAULT_MESSAGE = None
    HELPDESK_MEMBER_ASSIGNED = None
    CUSTOMER_ID = None

    @classmethod
    def load(cls):
        with open(UTILS_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.EMAIL_PROMPT = data['EMAIL_PROMPT']
            cls.PASSWORD_PROMPT = data['PASSWORD_PROMPT']
            cls.FULL_NAME_PROMPT = data['FULL_NAME_PROMPT']
            cls.PHONE_NUMBER_PROMPT = data['PHONE_NUMBER_PROMPT']
            cls.ADDRESS_PROMPT = data['ADDRESS_PROMPT']
            cls.PHONE_NUMBER_EMPTY = data['PHONE_NUMBER_EMPTY']
            cls.ADDRESS_EMPTY = data['ADDRESS_EMPTY']
            cls.FULLNAME_EMPTY = data['FULLNAME_EMPTY']
            cls.EMAIL_EMPTY_PROMPT = data['EMAIL_EMPTY_PROMPT']
            cls.PASSWORD_EMPTY_PROMPT = data['PASSWORD_EMPTY_PROMPT']
            cls.EMAIL_REGEX = data['EMAIL_REGEX']
            cls.PASSWORD_REGEX = data['PASSWORD_REGEX']
            cls.STRONG_PASSWORD_PROMPT = data['STRONG_PASSWORD_PROMPT']
            cls.INVALID_INPUT = data['INVALID_INPUT']
            cls.INPUT_MESSAGE_FROM_HELPDESK = data['INPUT_MESSAGE_FROM_HELPDESK']
            cls.MESSAGE_CANT_BE_EMPTY = data['MESSAGE_CANT_BE_EMPTY']
            cls.VALID_EMAIL = data['VALID_EMAIL']
            cls.TICKET_ID = data['TICKET_ID']
            cls.STATUS = data['STATUS']
            cls.TITLE = data['TITLE']
            cls.DESC = data['DESC']
            cls.END_OF_TICKETS = data['END_OF_TICKETS']
            cls.NOT_VALID_EMAIL_PROMPT = data['NOT_VALID_EMAIL_PROMPT']
            cls.TICKET_DEPT_PROMPT = data['TICKET_DEPT_PROMPT']
            cls.INVALID_DEPT = data['INVALID_DEPT']
            cls.TICKET_TITLE_PROMPT = data['TICKET_TITLE_PROMPT']
            cls.TICKET_TITLE_EMPTY = data['TICKET_TITLE_EMPTY']
            cls.TICKET_DESC_PROMPT = data['TICKET_DESC_PROMPT']
            cls.TICKET_DESC_EMPTY = data['TICKET_DESC_EMPTY']
            cls.LINE_BREAK = data['LINE_BREAK']
            cls.STARS = data['STARS']
            cls.MESSAGE_FROM_HELPDESK = data['MESSAGE_FROM_HELPDESK']
            cls.RAISED_ON = data['RAISED_ON']
            cls.DATE_FORMAT = data['DATE_FORMAT']
            cls.INVALID_DEPT = data['INVALID_DEPT']
            cls.DEFAULT_MESSAGE = data['DEFAULT_MESSAGE']
            cls.HELPDESK_MEMBER_ASSIGNED = data['HELPDESK_MEMBER_ASSIGNED']
            cls.CUSTOMER_ID = data['CUSTOMER_ID']
