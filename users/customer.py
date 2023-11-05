from os import system
from utils.input_utils import menu
from ticket.customer_section.customer_ticket_section import CustomerTicketSection
COMPANY_LOGO = '----------------------------------ABC Customer Service Portal----------------------------------'
CUSTOMER_WELCOME_MENU = "Welcome {} how can we help you?"
CUSTOMER_MENU = """
Press:
'r': for raising a ticket or complaint
'p': for viewing your existing in-progress tickets
'u': for viewing unresolved/raised tickets
'c': for viewing requests that have been closed by our representatives
'q': logout
Your Choice: """
TICKET_RAISED_SUCCESS = "Ticket raised successfully"


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
        print(COMPANY_LOGO)
        print(CUSTOMER_WELCOME_MENU.format(self.name))
        m = menu(CUSTOMER_MENU, allowed=('r', 'p', 'c', 'u'))
        for user_choice in m:
            customer_function = customer_functionalities.get(user_choice)
            system('cls')
            customer_function()

    def ticket_raising_handler(self):
        self.ticket_section.raise_ticket()
        print(TICKET_RAISED_SUCCESS)

    def in_progress_tickets_handler(self):
        self.ticket_section.view_in_progress_tickets()

    def closed_tickets_handler(self):
        self.ticket_section.view_closed_tickets()

    def raised_tickets_handler(self):
        self.ticket_section.view_unresolved_tickets()
