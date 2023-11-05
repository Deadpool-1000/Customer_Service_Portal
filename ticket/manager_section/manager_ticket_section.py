from os import system
from utils.utils import print_managers_view
from utils.input_utils import menu, simple_prompt
from utils.ticket_utils import tid_is_valid, tickets_menu
from DBUtils.ticket.ticketDAO import TicketDAO
from DBUtils.connection.database_connection import DatabaseConnection
MANAGER_TICKET_SECTION_MENU = """
Press:
'a': view all tickets
'q': back
Your choice: """
EMPTY_TICKETS = "No tickets to show"
ALL_TICKETS_WELCOME = "Here are the latest tickets raised by customers in our organization"
END_OF_TICKETS = "---------------------------That's all the tickets we have---------------------------"
ALL_TICKETS_PROMPT = """
Press:
'n': next page
'q': back
Your choice: """
ALL_TICKETS_CONTINUE_PROMPTS = "Do you want to see all the tickets again?(y/n)"


class ManagerTicketSection:
    def __init__(self, manager):
        self.manager = manager

    def menu(self):
        manager_ticket_section_functionalities = {
            'a': self.view_all_tickets
        }
        m = menu(MANAGER_TICKET_SECTION_MENU, allowed=['a', 'q'])
        for user_choice in m:
            manager_ticket_section_function = manager_ticket_section_functionalities.get(user_choice)
            system('cls')
            manager_ticket_section_function()
            system('cls')

    def view_all_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_tickets()

        if len(all_tickets) == 0:
            print(EMPTY_TICKETS)

        unresolved_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=ALL_TICKETS_WELCOME,
            continue_prompt=ALL_TICKETS_CONTINUE_PROMPTS,
            functionalities_prompt=ALL_TICKETS_PROMPT,
            functionalities=unresolved_ticket_functionalities
        )

    @staticmethod
    def view_ticket_detail_handler(self, all_tickets):
        t_id = input('Enter the ticket id of ticket you want to see in detail: ')

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_managers_view(found_ticket[0])

        if found_ticket[0].status == 'closed':
            pass
        else:
            # In case of closed ticket there is only one option to go back
            _ = simple_prompt('Press q to go back: ', allowed=['q'])
            return

