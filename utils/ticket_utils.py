from os import system
from utils.utils import view_list_generator, format_date
from utils.input_utils import simple_prompt
from utils.config.utils_config_loader import UtilsConfig


def tid_is_valid(t_id, all_tickets):
    return len(list(filter(lambda x: x.t_id == t_id, all_tickets))) != 0


def input_ticket():
    dept_id = input(UtilsConfig.TICKET_DEPT_PROMPT)
    while dept_id not in ['1', '2', '3']:
        dept_id = input(UtilsConfig.INVALID_DEPT).strip()

    title = input(UtilsConfig.TICKET_TITLE_PROMPT).strip()
    while len(title) == 0:
        title = input(UtilsConfig.TICKET_TITLE_PROMPT).strip()

    desc = input(UtilsConfig.TICKET_DESC_PROMPT).strip()
    while len(desc) == 0:
        desc = input(UtilsConfig.TICKET_DESC_EMPTY).strip()

    return dept_id, title, desc


def print_ticket_details(ticket):
    print(UtilsConfig.LINE_BREAK)
    print(UtilsConfig.TICKET_ID, ticket.t_id)
    print(UtilsConfig.TITLE, ticket.title)
    print(UtilsConfig.DESC, ticket.description)
    print(UtilsConfig.STATUS, ticket.status)
    print(UtilsConfig.MESSAGE_FROM_HELPDESK, UtilsConfig.DEFAULT_MESSAGE if ticket.message is None else ticket.message)
    print(UtilsConfig.RAISED_ON, format_date(ticket.created_on))
    print(UtilsConfig.LINE_BREAK)


def print_tickets_brief(tickets):
    print(UtilsConfig.LINE_BREAK)
    for ticket in tickets:
        print(UtilsConfig.TICKET_ID, ticket.t_id)
        print(UtilsConfig.TITLE, ticket.title)
        print(UtilsConfig.LINE_BREAK)


def tickets_menu(tickets, main_prompt, functionalities_prompt, continue_prompt, functionalities=None):
    if functionalities is None:
        functionalities = {}

    while True:
        print(main_prompt)
        ticket_view_generator = view_list_generator(tickets)
        did_quit = False

        for tickets in ticket_view_generator:
            print_tickets_brief(tickets)
            user_choice = simple_prompt(functionalities_prompt, [*functionalities.keys(), 'n', 'q'])
            if user_choice == 'n':
                continue
            elif user_choice == 'q':
                did_quit = True
                break
            else:
                functionalities.get(user_choice)()
            system('cls')

        if not did_quit:
            print(UtilsConfig.END_OF_TICKETS)
        user_choice = simple_prompt(continue_prompt, ['y', 'n'])
        if user_choice == 'y':
            system('cls')
            continue
        else:
            break
