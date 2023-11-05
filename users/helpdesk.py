from utils.input_utils import menu
from ticket.helpdesk_section.helpdesk_ticket_section import HelpDeskTicketSection
from os import system

COMPANY_LOGO = '----------------------------------ABC Company Service Portal----------------------------------'
HELPDESK_PROMPT = """
Press: 
't': tickets section
'm': message box
'q': logout
Your Choice: """
WELCOME_MESSAGE = "Hey {}"


class Helpdesk:
    def __init__(self, e_id, name, phn_num, address, email, dept_id):
        self.e_id = e_id
        self.name = name
        self.phn_num = phn_num
        self.address = address
        self.email = email
        self.dept_id = dept_id
        self.ticket_section = HelpDeskTicketSection(self)

    def menu(self):
        helpdesk_functionalities = {
            't': self.tickets_section_handler,
            'm': self.message_box_handler,
        }
        system('cls')
        print(COMPANY_LOGO)
        print(WELCOME_MESSAGE.format(self.name))
        m = menu(HELPDESK_PROMPT, allowed=['t', 'm'])
        for user_choice in m:
            helpdesk_function = helpdesk_functionalities.get(user_choice)
            system('cls')
            helpdesk_function()

    def tickets_section_handler(self):
        self.ticket_section.menu()

    def message_box_handler(self):
        pass
