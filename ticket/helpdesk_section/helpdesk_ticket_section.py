import logging
from utils.input_utils import menu, simple_prompt, input_message_from_helpdesk
from utils.ticket_utils import tid_is_valid, print_ticket_details, tickets_menu
from os import system
from DBUtils.connection.database_connection import DatabaseConnection
from DBUtils.ticket.ticketDAO import TicketDAO

logger = logging.getLogger('main.help_section')

WELCOME_HELPDESK_SECTION = "---------------------------Welcome to tickets section---------------------------"
UNRESOLVED_TICKETS_WELCOME = 'Here, are the latest unresolved tickets: '
CLOSE_TICKET_WELCOME = "Here are the available tickets please enter the ticket id for which you want to delete: "
TICKET_IN_DETAIL_WELCOME = "Ticket: "
TICKET_MENU = """
Do you want to resolve this ticket?(y/n)
"""
PLEASE_ENTER_VALID_INPUT = "Please enter a valid input: "
RESOLVED_TICKET_WELCOME = "Here are the resolved tickets: "
RESOLVE_TICKET_PROMPT = "Enter ticket id  of the ticket you want to resolve: "
CLOSED_TICKETS_WELCOME = "Here are the latest closed tickets: "
HELPDESK_TICKET_PROMPT = """
Press:
'u': unresolved tickets
'r': resolved tickets
'c': closed tickets
'q': back
"""
UNRESOLVED_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'r': Resolve tickets
'n': next page 
'q': back 
Your Choice: """
RESOLVED_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'c': close ticket
'n': next page
'q': back
Your choice: """
CLOSED_TICKETS_PROMPT = """
Press:
'd': view ticket in detail
'n': next page
'q': back
Your choice: """
LINE_BREAK = "----------------------------------------"
UNRESOLVED_TICKET_CONTINUE_PROMPT = "Do you want to see the unresolved tickets again?(y/n): "
RESOLVED_TICKETS_CONTINUE_PROMPT = "Do you want to see the resolved tickets again?(y/n): "
END_OF_TICKETS = "---------------------------That's all the tickets we have---------------------------"
CLOSE_TICKET_PROMPT = "Enter the ticket id of the ticket you want to close: "
EMPTY_RESOLVED_TICKETS = "There are no resolved tickets currently"
EMPTY_UNRESOLVED_TICKETS = "There are no unresolved tickets currently"
EMPTY_CLOSED_TICKETS = "There are no closed tickets currently"
CLOSED_TICKETS_CONTINUE_PROMPT = "Do you want to see the closed tickets again?(y/n): "
SUCCESS_SENT = "Successfully Sent."


class HelpDeskTicketSection:
    def __init__(self, helpdesk):
        self.helpdesk = helpdesk

    def menu(self):
        system('cls')
        helpdesk_ticket_functionalities = {
            'u': self.unresolved_tickets,
            'r': self.resolved_tickets,
            'c': self.closed_tickets
        }
        m = menu(HELPDESK_TICKET_PROMPT, allowed=['u', 'r', 'c'])
        print(WELCOME_HELPDESK_SECTION)
        for user_choice in m:
            helpdesk_function = helpdesk_ticket_functionalities.get(user_choice)
            system('cls')
            helpdesk_function()
            print(WELCOME_HELPDESK_SECTION)

    def resolve_tickets_handler(self, all_tickets):
        t_id = input(RESOLVE_TICKET_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        self.resolve_ticket_by_id(t_id)

    def close_tickets_handler(self, all_tickets):
        t_id = input(CLOSE_TICKET_PROMPT)

        while not tid_is_valid(t_id, all_tickets) or t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        self.close_ticket_by_id(t_id)

    def unresolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_raised_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(EMPTY_UNRESOLVED_TICKETS)
            return

        unresolved_ticket_functionalities = {
            'r': lambda: self.resolve_tickets_handler(all_tickets),
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=UNRESOLVED_TICKETS_WELCOME,
            continue_prompt=UNRESOLVED_TICKET_CONTINUE_PROMPT,
            functionalities_prompt=UNRESOLVED_TICKETS_PROMPT,
            functionalities=unresolved_ticket_functionalities
        )

    def resolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_in_progress_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(EMPTY_RESOLVED_TICKETS)
            return

        resolved_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
            'c': lambda: self.close_tickets_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=RESOLVED_TICKET_WELCOME,
            continue_prompt=RESOLVED_TICKETS_CONTINUE_PROMPT,
            functionalities_prompt=RESOLVED_TICKETS_PROMPT,
            functionalities=resolved_ticket_functionalities
        )

    def closed_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_closed_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(EMPTY_CLOSED_TICKETS)
            return

        closed_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=CLOSED_TICKETS_WELCOME,
            continue_prompt=CLOSED_TICKETS_CONTINUE_PROMPT,
            functionalities_prompt=CLOSED_TICKETS_PROMPT,
            functionalities=closed_ticket_functionalities
        )
        system('cls')

    def resolve_ticket_by_id(self, t_id):
        #  print formatted ticket
        message = input_message_from_helpdesk()
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.change_ticket_status(t_id, "in_progress")
            t_dao.assign_repr_id(t_id, self.helpdesk.e_id)
            t_dao.update_message_from_helpdesk(message, t_id)
        print(SUCCESS_SENT)

    @staticmethod
    def close_ticket_by_id(t_id):
        message = input_message_from_helpdesk()
        logger.debug(f"Closing ticket with t_id {t_id}")
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.change_ticket_status(t_id, "closed")
            t_dao.update_message_from_helpdesk(message, t_id)
        print(SUCCESS_SENT)

    def view_ticket_detail_handler(self, all_tickets):

        t_id = input('Enter the ticket id of ticket you want to see in detail: ')

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_ticket_details(found_ticket[0])

        if found_ticket[0].status == 'in_progress':
            # In progress tickets can be closed or helpdesk member can go back
            user_choice = simple_prompt(IN_PROGRESS_DETAILS_PROMPT, allowed=('c', 'q'))
            if user_choice == 'c':
                self.close_tickets_handler(all_tickets)
            else:
                return

        elif found_ticket[0].status == 'raised':
            # Raised tickets can be resolved or helpdesk member can go back
            user_choice = simple_prompt(RAISED_TICKETS_DETAIL_PROMPT, allowed=('r', 'q'))
            if user_choice == 'r':
                self.resolve_tickets_handler(all_tickets)
            else:
                return

        else:
            # In case of closed ticket there is only one option to go back
            _ = simple_prompt('Press q to go back: ', allowed=['q'])
            return


IN_PROGRESS_DETAILS_PROMPT = """
Press:
'c': close this ticket,
'q': go back
Your choice: """

RAISED_TICKETS_DETAIL_PROMPT = """
Press:
'r': resolve this ticket
'q': go back
Your choice: """
