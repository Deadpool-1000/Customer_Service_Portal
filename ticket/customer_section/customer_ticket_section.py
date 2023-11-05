from os import system
from utils.input_utils import simple_prompt, input_feedback_body
from utils.ticket_utils import tid_is_valid, input_ticket, print_ticket_details, tickets_menu
from DBUtils.connection.database_connection import DatabaseConnection
from DBUtils.ticket.ticketDAO import TicketDAO
from DBUtils.customer.feedbackdao import FeedbackDAO


TICKET_RAISE_WELCOME_MESSAGE = "Please enter the following details so that we can raise your ticket: "
VIEW_IN_PROGRESS_TICKETS_WELCOME = "Here are your in-progress tickets: "
NO_TICKETS_YET = "No tickets yet, please stay tuned"
CLOSED_TICKETS_WELCOME = "Here are your closed tickets"
UNRESOLVED_TICKETS_WELCOME = "Here are your unresolved tickets"
EMPTY_CLOSED_TICKETS = "There are no closed tickets"
END_OF_TICKETS = "---------------------------That's all the tickets we have---------------------------"
CLOSED_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'f': give feedback
'n': next page
'q': back
"""
IN_PROGRESS_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'n': next page
'q': back   
"""
UNRESOLVED_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'n': next page
'q': back 
Your choice: """
UNRESOLVED_TICKETS_CONTINUE_PROMPT = "Do you want to see the unresolved tickets again?(y/n): "
CLOSED_TICKETS_CONTINUE_PROMPT = "Do you want to see the closed tickets again?(y/n): "
FEEDBACK_TICKET_PROMPT = "Please enter the ticket_id of the ticket you want to close: "
TRY_AGAIN = "Do you want to try again?(y/n)"
FEEDBACK_LOGO = "---------------------------Feedback-------------------------------"
NO_IN_PROG_TICKETS = "There are no in-progress tickets"
NO_UNRESOLVED_TICKETS = "No Unresolved tickets yet."
SUCCESS_FEEDBACK = "Feedback submitted."
TICKET_DETAIL_PROMPT = """
Press:
'f': give feedback
'q': back
Your choice: """
IN_PROGRESS_CONTINUE_PROMPT = "Do you want to see the in-progress tickets again?(y/n): "


class CustomerTicketSection:
    def __init__(self, customer):
        self.customer = customer

    def raise_ticket(self):
        print(TICKET_RAISE_WELCOME_MESSAGE)
        department, title, description = input_ticket()
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.create_new_ticket(d_id=department, c_id=self.customer.c_id, desc=description, title=title)

    def view_in_progress_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_in_progress_ticket(self.customer.c_id)

        if len(all_tickets) == 0:
            system('cls')
            print(NO_IN_PROG_TICKETS)
            return

        in_progress_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=VIEW_IN_PROGRESS_TICKETS_WELCOME,
            continue_prompt=IN_PROGRESS_CONTINUE_PROMPT,
            functionalities=in_progress_ticket_functionalities,
            functionalities_prompt=IN_PROGRESS_TICKETS_PROMPT
        )
        system('cls')

    def view_closed_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_closed_tickets(self.customer.c_id)

        if len(all_tickets) == 0:
            print(EMPTY_CLOSED_TICKETS)
            return

        closed_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
            'f': lambda: self.give_feedback_handler(all_tickets),
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=CLOSED_TICKETS_WELCOME,
            continue_prompt=CLOSED_TICKETS_CONTINUE_PROMPT,
            functionalities=closed_ticket_functionalities,
            functionalities_prompt=CLOSED_TICKETS_PROMPT
        )
        system('cls')

    def view_unresolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_raised_tickets(self.customer.c_id)

        if len(all_tickets) == 0:
            print(NO_UNRESOLVED_TICKETS)
            return

        unresolved_tickets_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=UNRESOLVED_TICKETS_WELCOME,
            continue_prompt=UNRESOLVED_TICKETS_CONTINUE_PROMPT,
            functionalities=unresolved_tickets_functionalities,
            functionalities_prompt=UNRESOLVED_TICKETS_PROMPT,
        )
        system('cls')

    def give_feedback_handler(self, all_tickets):
        t_id = input('Enter the ticket id of ticket you want to see in detail or press q to go back: ')

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        self.register_feedback(t_id)

    def view_ticket_detail_handler(self, all_tickets):
        t_id = input('Enter the ticket id of ticket you want to see in detail: ')

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_ticket_details(found_ticket[0])

        if found_ticket[0].status == 'closed':
            user_choice = simple_prompt(TICKET_DETAIL_PROMPT, allowed=('f', 'q'))
            if user_choice == 'f':
                self.register_feedback(t_id)
            else:
                return
        else:
            _ = simple_prompt('Press q to go back: ', allowed=['q'])
            return

    @staticmethod
    def register_feedback(t_id):
        print(FEEDBACK_LOGO)
        stars, desc = input_feedback_body()
        with DatabaseConnection() as conn:
            f_dao = FeedbackDAO(conn)
            f_dao.add_feedback(stars, desc, t_id)
        system('cls')
        print(SUCCESS_FEEDBACK)
