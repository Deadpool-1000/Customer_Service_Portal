import yaml

MANAGER_TICKET_CONFIG_FILE_PATH = 'ticket/manager_section/config/manager_ticket.yml'


class ManagerTicketConfig:
    MANAGER_TICKET_SECTION_MENU = None
    EMPTY_TICKETS = None
    ALL_TICKETS_WELCOME = None
    END_OF_TICKETS = None
    ALL_TICKETS_PROMPT = None
    ALL_TICKETS_CONTINUE_PROMPTS = None
    DETAIL_T_ID_PROMPT = None
    INVALID_T_ID = None
    CLOSED = None
    GO_BACK_PROMPT = None

    @classmethod
    def load(cls):
        with open(MANAGER_TICKET_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.MANAGER_TICKET_SECTION_MENU = data['MANAGER_TICKET_SECTION_MENU']
            cls.EMPTY_TICKETS = data['EMPTY_TICKETS']
            cls.ALL_TICKETS_WELCOME = data['ALL_TICKETS_WELCOME']
            cls.END_OF_TICKETS = data['END_OF_TICKETS']
            cls.ALL_TICKETS_PROMPT = data['ALL_TICKETS_PROMPT']
            cls.ALL_TICKETS_CONTINUE_PROMPTS = data['ALL_TICKETS_CONTINUE_PROMPTS']
            cls.DETAIL_T_ID_PROMPT = data['DETAIL_T_ID_PROMPT']
            cls.INVALID_T_ID = data['INVALID_T_ID']
            cls.CLOSED = data['CLOSED']
            cls.GO_BACK_PROMPT = data['GO_BACK_PROMPT']
