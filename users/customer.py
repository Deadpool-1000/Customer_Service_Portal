import logging
from os import system
from utils.input_utils import menu
from ticket.customer_section.customer_ticket_section import CustomerTicketSection
from users.config.users_config_loader import UsersConfig

logger = logging.getLogger('main.customer')


class Customer:
    def __init__(self, c_id, name, phn_num, address, email):
        self.c_id = c_id
        self.name = name
        self.phn_num = phn_num
        self.address = address
        self.email = email
        self.ticket_section = CustomerTicketSection(self)

    def menu(self):
        customer_functionalities = {
            'r': self.ticket_raising_handler,
            'u': self.raised_tickets_handler,
            'p': self.in_progress_tickets_handler,
            'c': self.closed_tickets_handler
        }
        system('cls')
        print(UsersConfig.COMPANY_LOGO)
        print(UsersConfig.CUSTOMER_WELCOME_MENU.format(self.name))
        m = menu(UsersConfig.CUSTOMER_MENU, allowed=('r', 'p', 'c', 'u'))
        for user_choice in m:
            customer_function = customer_functionalities.get(user_choice)
            system('cls')
            customer_function()

    def ticket_raising_handler(self):
        self.ticket_section.raise_ticket()
        logger.info(f'Customer:{self.c_id} is trying to raise a ticket')
        print(UsersConfig.TICKET_RAISED_SUCCESS)

    def in_progress_tickets_handler(self):
        self.ticket_section.view_in_progress_tickets()

    def closed_tickets_handler(self):
        self.ticket_section.view_closed_tickets()

    def raised_tickets_handler(self):
        self.ticket_section.view_unresolved_tickets()
