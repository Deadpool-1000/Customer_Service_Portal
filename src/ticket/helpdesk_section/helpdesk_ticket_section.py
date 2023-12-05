import logging
from os import system
from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.ticket.helpdesk_section.config.helpdesk_ticket_config_loader import HelpdeskTicketConfig
from src.utils.inputs.input_utils import menu, simple_input, input_message_from_helpdesk
from src.utils.tickets.ticket_utils import tid_is_valid, print_ticket_details, tickets_menu

logger = logging.getLogger('main.help_section')


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
        m = menu(HelpdeskTicketConfig.HELPDESK_TICKET_PROMPT, allowed=['u', 'r', 'c'])
        print(HelpdeskTicketConfig.WELCOME_HELPDESK_SECTION)
        for user_choice in m:
            helpdesk_function = helpdesk_ticket_functionalities.get(user_choice)
            system('cls')
            helpdesk_function()
            print(HelpdeskTicketConfig.WELCOME_HELPDESK_SECTION)

    def resolved_tickets_handler(self, all_tickets):
        t_id = input(HelpdeskTicketConfig.RESOLVE_TICKET_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input(HelpdeskTicketConfig.INVALID_T_ID)

        if t_id == 'q':
            return

        self.resolve_ticket_by_id(t_id)

    def close_tickets_handler(self, all_tickets):
        t_id = input(HelpdeskTicketConfig.CLOSE_TICKET_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input(HelpdeskTicketConfig.INVALID_T_ID)

        if t_id == 'q':
            return
        logger.info(f'ticket_id:{t_id} is closed by {self.helpdesk.e_id}')

        self.close_ticket_by_id(t_id)

    def unresolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_raised_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(HelpdeskTicketConfig.EMPTY_UNRESOLVED_TICKETS)
            return

        unresolved_ticket_functionalities = {
            'r': lambda: self.resolved_tickets_handler(all_tickets),
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=HelpdeskTicketConfig.UNRESOLVED_TICKETS_WELCOME,
            continue_prompt=HelpdeskTicketConfig.UNRESOLVED_TICKET_CONTINUE_PROMPT,
            functionalities_prompt=HelpdeskTicketConfig.UNRESOLVED_TICKETS_PROMPT,
            functionalities=unresolved_ticket_functionalities
        )

    def resolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_in_progress_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(HelpdeskTicketConfig.EMPTY_RESOLVED_TICKETS)
            return

        resolved_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
            'c': lambda: self.close_tickets_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=HelpdeskTicketConfig.RESOLVED_TICKET_WELCOME,
            continue_prompt=HelpdeskTicketConfig.RESOLVED_TICKETS_CONTINUE_PROMPT,
            functionalities_prompt=HelpdeskTicketConfig.RESOLVED_TICKETS_PROMPT,
            functionalities=resolved_ticket_functionalities
        )

    def closed_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.view_all_closed_tickets(self.helpdesk.dept_id)

        if len(all_tickets) == 0:
            print(HelpdeskTicketConfig.EMPTY_CLOSED_TICKETS)
            return

        closed_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=HelpdeskTicketConfig.CLOSED_TICKETS_WELCOME,
            continue_prompt=HelpdeskTicketConfig.CLOSED_TICKETS_CONTINUE_PROMPT,
            functionalities_prompt=HelpdeskTicketConfig.CLOSED_TICKETS_PROMPT,
            functionalities=closed_ticket_functionalities
        )
        system('cls')

    def resolve_ticket_by_id(self, t_id):
        #  print formatted ticket
        message = input_message_from_helpdesk()
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.change_ticket_status(t_id, HelpdeskTicketConfig.IN_PROGRESS)
            t_dao.assign_repr_id(t_id, self.helpdesk.e_id)
            t_dao.update_message_from_helpdesk(message, t_id)
        logger.info(f'ticket_id:{t_id} is resolved by {self.helpdesk.e_id}')
        print(HelpdeskTicketConfig.SUCCESS_SENT)

    @staticmethod
    def close_ticket_by_id(t_id):
        message = input_message_from_helpdesk()
        logger.debug(f"Closing ticket with t_id {t_id}")
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.change_ticket_status(t_id, HelpdeskTicketConfig.CLOSED)
            t_dao.update_message_from_helpdesk(message, t_id)
        print(HelpdeskTicketConfig.SUCCESS_SENT)

    def view_ticket_detail_handler(self, all_tickets):

        t_id = input('Enter the ticket id of ticket you want to see in detail: ')

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input('Enter valid ticket id or press q to go back: ')

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_ticket_details(found_ticket[0])

        if found_ticket[0].status == HelpdeskTicketConfig.IN_PROGRESS:
            # In progress tickets can be closed or helpdesk member can go back
            user_choice = simple_input(HelpdeskTicketConfig.IN_PROGRESS_DETAILS_PROMPT, allowed=('c', 'q'))
            if user_choice == 'c':
                self.close_tickets_handler(all_tickets)
            else:
                return

        elif found_ticket[0].status == HelpdeskTicketConfig.RAISED:
            # Raised tickets can be resolved or helpdesk member can go back
            user_choice = simple_input(HelpdeskTicketConfig.RAISED_TICKETS_DETAIL_PROMPT, allowed=('r', 'q'))
            if user_choice == 'r':
                self.resolved_tickets_handler(all_tickets)
            else:
                return

        else:
            # In case of closed ticket there is only one option to go back
            _ = simple_input(HelpdeskTicketConfig.GO_BACK_PROMPT, allowed=['q'])
            return
