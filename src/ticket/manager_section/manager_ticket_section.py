import logging
from os import system

from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.ticket.manager_section.config.manager_ticket_config_loader import ManagerTicketConfig
from src.utils.inputs.input_utils import menu, simple_input
from src.utils.tickets.ticket_utils import tid_is_valid, tickets_menu
from src.utils.utils import print_managers_view

logger = logging.getLogger('main.manager_ticket')


class ManagerTicketSection:
    def __init__(self, manager):
        self.manager = manager

    def menu(self):
        manager_ticket_section_functionalities = {
            'a': self.view_all_tickets
        }
        m = menu(ManagerTicketConfig.MANAGER_TICKET_SECTION_MENU, allowed=('a', ))
        for user_choice in m:
            manager_ticket_section_function = manager_ticket_section_functionalities.get(user_choice)
            system('cls')
            manager_ticket_section_function()
            system('cls')

    def view_all_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.get_all_tickets()

        if len(all_tickets) == 0:
            print(ManagerTicketConfig.EMPTY_TICKETS)

        unresolved_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=ManagerTicketConfig.ALL_TICKETS_WELCOME,
            continue_prompt=ManagerTicketConfig.ALL_TICKETS_CONTINUE_PROMPTS,
            functionalities_prompt=ManagerTicketConfig.ALL_TICKETS_PROMPT,
            functionalities=unresolved_ticket_functionalities
        )
        logger.info('Manager viewed all tickets in the organization')

    @staticmethod
    def view_ticket_detail_handler(all_tickets):
        t_id = input(ManagerTicketConfig.DETAIL_T_ID_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input(ManagerTicketConfig.INVALID_T_ID)

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_managers_view(found_ticket[0])

        if found_ticket[0].status == ManagerTicketConfig.CLOSED:
            pass

        else:
            # In case of closed ticket there is only one option to go back
            _ = simple_input(ManagerTicketConfig.GO_BACK_PROMPT, allowed=['q'])
            return
