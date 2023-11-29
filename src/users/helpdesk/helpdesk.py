from os import system

from src.ticket.helpdesk_section.helpdesk_ticket_section import HelpDeskTicketSection
from src.users.config.users_config_loader import UsersConfig
from src.utils.inputs.input_utils import menu


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
        print(UsersConfig.COMPANY_LOGO)
        print(UsersConfig.WELCOME_MESSAGE.format(self.name))
        m = menu(UsersConfig.HELPDESK_PROMPT, allowed=['t', 'm'])
        for user_choice in m:
            helpdesk_function = helpdesk_functionalities.get(user_choice)
            system('cls')
            helpdesk_function()

    def tickets_section_handler(self):
        self.ticket_section.menu()

    def message_box_handler(self):
        raise NotImplementedError('Not implemented yet stay tuned')

