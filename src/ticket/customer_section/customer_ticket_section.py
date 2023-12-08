import logging
from os import system
from src.DBUtils.connection.database_connection import DatabaseConnection
from src.DBUtils.customer.feedbackdao import FeedbackDAO
from src.DBUtils.ticket.ticketDAO import TicketDAO
from src.ticket.customer_section.config.customer_ticket_config_loader import CustomerTicketConfig
from src.utils.inputs.input_utils import simple_input, input_feedback_body
from src.utils.tickets.ticket_utils import tid_is_valid, input_ticket, print_ticket_details, tickets_menu

logger = logging.getLogger('main.customer_ticket_section')


class CustomerTicketSection:
    def __init__(self, customer):
        self.customer = customer

    def raise_ticket(self):
        print(CustomerTicketConfig.TICKET_RAISE_WELCOME_MESSAGE)
        department, title, description = input_ticket()
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            t_dao.create_new_ticket(d_id=department, c_id=self.customer.c_id, desc=description, title=title)

    def view_in_progress_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.get_in_progress_tickets_with_cid(self.customer.c_id)

        if len(all_tickets) == 0:
            system('cls')
            print(CustomerTicketConfig.NO_IN_PROG_TICKETS)
            return

        in_progress_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets)
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=CustomerTicketConfig.VIEW_IN_PROGRESS_TICKETS_WELCOME,
            continue_prompt=CustomerTicketConfig.IN_PROGRESS_CONTINUE_PROMPT,
            functionalities=in_progress_ticket_functionalities,
            functionalities_prompt=CustomerTicketConfig.IN_PROGRESS_TICKETS_PROMPT
        )
        system('cls')

    def view_closed_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.get_closed_tickets_by_cid(self.customer.c_id)

        if len(all_tickets) == 0:
            print(CustomerTicketConfig.EMPTY_CLOSED_TICKETS)
            return

        closed_ticket_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
            'f': lambda: self.give_feedback_handler(all_tickets),
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=CustomerTicketConfig.CLOSED_TICKETS_WELCOME,
            continue_prompt=CustomerTicketConfig.CLOSED_TICKETS_CONTINUE_PROMPT,
            functionalities=closed_ticket_functionalities,
            functionalities_prompt=CustomerTicketConfig.CLOSED_TICKETS_PROMPT
        )
        system('cls')

    def view_unresolved_tickets(self):
        with DatabaseConnection() as conn:
            t_dao = TicketDAO(conn)
            all_tickets = t_dao.get_raised_tickets_by_cid(self.customer.c_id)

        if len(all_tickets) == 0:
            print(CustomerTicketConfig.NO_UNRESOLVED_TICKETS)
            return

        unresolved_tickets_functionalities = {
            'd': lambda: self.view_ticket_detail_handler(all_tickets),
        }

        tickets_menu(
            tickets=all_tickets,
            main_prompt=CustomerTicketConfig.UNRESOLVED_TICKETS_WELCOME,
            continue_prompt=CustomerTicketConfig.UNRESOLVED_TICKETS_CONTINUE_PROMPT,
            functionalities=unresolved_tickets_functionalities,
            functionalities_prompt=CustomerTicketConfig.UNRESOLVED_TICKETS_PROMPT,
        )
        system('cls')

    def give_feedback_handler(self, all_tickets):
        t_id = input(CustomerTicketConfig.FEEDBACK_TICKET_ID_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input(CustomerTicketConfig.INVALID_T_ID_PROMPT)

        if t_id == 'q':
            return

        self.register_feedback(t_id)

    def view_ticket_detail_handler(self, all_tickets):
        t_id = input(CustomerTicketConfig.DETAIL_TICKET_ID_PROMPT)

        while not tid_is_valid(t_id, all_tickets) and t_id != 'q':
            t_id = input(CustomerTicketConfig.INVALID_T_ID_PROMPT)

        if t_id == 'q':
            return

        found_ticket = list(filter(lambda x: x.t_id == t_id, all_tickets))
        print_ticket_details(found_ticket[0])

        if found_ticket[0].status == 'closed':
            user_choice = simple_input(CustomerTicketConfig.TICKET_DETAIL_PROMPT, allowed=('f', 'q'))
            if user_choice == 'f':
                self.register_feedback(t_id)
            else:
                return
        else:
            _ = simple_input(CustomerTicketConfig.GO_BACK_PROMPT, allowed=('q',))
            return

    def register_feedback(self, t_id):
        print(CustomerTicketConfig.FEEDBACK_LOGO)
        stars, desc = input_feedback_body()
        with DatabaseConnection() as conn:
            f_dao = FeedbackDAO(conn)
            f_dao.add_feedback(stars, desc, t_id)
        logger.info(f'Feedback generated for ticket_id:{t_id} by {self.customer.c_id}')
        system('cls')
        print(CustomerTicketConfig.SUCCESS_FEEDBACK)
