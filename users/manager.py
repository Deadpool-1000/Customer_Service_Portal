from utils.input_utils import menu, simple_prompt
from os import system
from ticket.manager_section.manager_ticket_section import ManagerTicketSection
from DBUtils.connection.database_connection import DatabaseConnection
from DBUtils.customer.feedbackdao import FeedbackDAO
from utils.utils import view_list_generator, print_feedbacks_formatted


MANAGER_PROMPT = """
Press:
't': access tickets section
'f': access feedback section
'q': logout
Your Choice: """
COMPANY_LOGO = '----------------------------------ABC Company Service Portal----------------------------------'
MANAGER_WELCOME_MESSAGE = "Welcome {}"
FEEDBACK_HANDLER_TITLE = "---------------------------Feedback-------------------------------"
EMPTY_FEEDBACKS = "There are no feedbacks to show"
FEEDBACK_PROMPT = """
Press:
'n': next page
'q': back 
"""
FEEDBACK_CONTINUE_PROMPT = "Do you want to see the feedbacks again?(y/n): "
END_OF_FEEDBACKS = "That's all the feedback we have"


class Manager:
    def __init__(self, e_id, name, phn_num, address, email):
        self.e_id = e_id
        self.name = name
        self.phn_num = phn_num
        self.address = address
        self.email = email
        self.ticket_section = ManagerTicketSection(self)

    def menu(self):
        manager_functionalities = {
            't': self.tickets_section_handler,
            'f': self.customer_feedback_section_handler
        }
        m = menu(MANAGER_PROMPT, allowed=('t', 'f'))
        system('cls')
        print(COMPANY_LOGO)
        print(MANAGER_WELCOME_MESSAGE.format(self.name))
        for user_choice in m:
            manager_function = manager_functionalities.get(user_choice)
            system('cls')
            manager_function()

    def tickets_section_handler(self):
        self.ticket_section.menu()

    @staticmethod
    def customer_feedback_section_handler():
        print(FEEDBACK_HANDLER_TITLE)
        with DatabaseConnection() as conn:
            f_dao = FeedbackDAO(conn)
            all_feedbacks = f_dao.get_feedback()
        if len(all_feedbacks) == 0:
            print(EMPTY_FEEDBACKS)
        while True:
            feedback_generator = view_list_generator(all_feedbacks)
            did_quit = False
            for tickets in feedback_generator:
                print_feedbacks_formatted(tickets)
                user_choice = simple_prompt(FEEDBACK_PROMPT, ('n', 'q'))
                if user_choice == 'n':
                    continue
                else:
                    did_quit = True
                    break
            if not did_quit:
                print(END_OF_FEEDBACKS)
            user_choice = simple_prompt(FEEDBACK_CONTINUE_PROMPT, ('y', 'n'))
            if user_choice == 'y':
                system('cls')
                continue
            else:
                break
