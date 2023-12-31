from os import path

import yaml

path_current_directory = path.dirname(__file__)
CUSTOMER_TICKET_CONFIG_FILE_PATH = path.join(path_current_directory, 'customer_ticket.yml')


class CustomerTicketConfig:
    TICKET_RAISE_WELCOME_MESSAGE = None
    VIEW_IN_PROGRESS_TICKETS_WELCOME = None
    NO_TICKETS_YET = None
    CLOSED_TICKETS_WELCOME = None
    UNRESOLVED_TICKETS_WELCOME = None
    EMPTY_CLOSED_TICKETS = None
    END_OF_TICKETS = None
    CLOSED_TICKETS_PROMPT = None
    IN_PROGRESS_TICKETS_PROMPT = None
    UNRESOLVED_TICKETS_PROMPT = None
    UNRESOLVED_TICKETS_CONTINUE_PROMPT = None
    CLOSED_TICKETS_CONTINUE_PROMPT = None
    FEEDBACK_TICKET_PROMPT = None
    TRY_AGAIN = None
    FEEDBACK_LOGO = None
    NO_IN_PROG_TICKETS = None
    NO_UNRESOLVED_TICKETS = None
    SUCCESS_FEEDBACK = None
    TICKET_DETAIL_PROMPT = None
    IN_PROGRESS_CONTINUE_PROMPT = None
    GO_BACK_PROMPT = None
    DETAIL_TICKET_ID_PROMPT = None
    INVALID_T_ID_PROMPT = None
    FEEDBACK_TICKET_ID_PROMPT = None

    @classmethod
    def load(cls):
        with open(CUSTOMER_TICKET_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.TICKET_RAISE_WELCOME_MESSAGE = data['TICKET_RAISE_WELCOME_MESSAGE']
            cls.VIEW_IN_PROGRESS_TICKETS_WELCOME = data['VIEW_IN_PROGRESS_TICKETS_WELCOME']
            cls.NO_TICKETS_YET = data['NO_TICKETS_YET']
            cls.CLOSED_TICKETS_WELCOME = data['CLOSED_TICKETS_WELCOME']
            cls.UNRESOLVED_TICKETS_WELCOME = data['UNRESOLVED_TICKETS_WELCOME']
            cls.EMPTY_CLOSED_TICKETS = data['EMPTY_CLOSED_TICKETS']
            cls.END_OF_TICKETS = data['END_OF_TICKETS']
            cls.CLOSED_TICKETS_PROMPT = data['CLOSED_TICKETS_PROMPT']
            cls.IN_PROGRESS_TICKETS_PROMPT = data['IN_PROGRESS_TICKETS_PROMPT']
            cls.UNRESOLVED_TICKETS_PROMPT = data['UNRESOLVED_TICKETS_PROMPT']
            cls.UNRESOLVED_TICKETS_CONTINUE_PROMPT = data['UNRESOLVED_TICKETS_CONTINUE_PROMPT']
            cls.CLOSED_TICKETS_CONTINUE_PROMPT = data['CLOSED_TICKETS_CONTINUE_PROMPT']
            cls.FEEDBACK_TICKET_PROMPT = data['FEEDBACK_TICKET_PROMPT']
            cls.TRY_AGAIN = data['TRY_AGAIN']
            cls.FEEDBACK_LOGO = data['FEEDBACK_LOGO']
            cls.NO_IN_PROG_TICKETS = data['NO_IN_PROG_TICKETS']
            cls.NO_UNRESOLVED_TICKETS = data['NO_UNRESOLVED_TICKETS']
            cls.SUCCESS_FEEDBACK = data['SUCCESS_FEEDBACK']
            cls.TICKET_DETAIL_PROMPT = data['TICKET_DETAIL_PROMPT']
            cls.IN_PROGRESS_CONTINUE_PROMPT = data['IN_PROGRESS_CONTINUE_PROMPT']
            cls.GO_BACK_PROMPT = data['GO_BACK_PROMPT']
            cls.DETAIL_TICKET_ID_PROMPT = data['DETAIL_TICKET_ID_PROMPT']
            cls.INVALID_T_ID_PROMPT = data['INVALID_T_ID_PROMPT']
            cls.FEEDBACK_TICKET_ID_PROMPT = data['FEEDBACK_TICKET_ID_PROMPT']
