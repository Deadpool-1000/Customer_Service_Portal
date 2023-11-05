from datetime import datetime
from os import system

from utils.utils import DEFAULT_MESSAGE, view_list_generator
from utils.input_utils import simple_prompt


def tid_is_valid(t_id, all_tickets):
    return len(list(filter(lambda x: x.t_id == t_id, all_tickets))) != 0


def input_ticket():
    dept_id = input(TICKET_DEPT_PROMPT)
    while dept_id not in ['1', '2', '3']:
        dept_id = input(INVALID_DEPT).strip()

    title = input(TICKET_TITLE_PROMPT).strip()
    while len(title) == 0:
        title = input(TICKET_TITLE_PROMPT).strip()

    desc = input(TICKET_DESC_PROMPT).strip()
    while len(desc) == 0:
        desc = input(TICKET_DESC_EMPTY).strip()

    return dept_id, title, desc


def print_ticket_details(ticket):
    print(LINE_BREAK)
    print(TICKET_ID, ticket.t_id)
    print(TITLE, ticket.title)
    print(DESC, ticket.description)
    print(STATUS, ticket.status)
    print(MESSAGE_FROM_HELPDESK, DEFAULT_MESSAGE if ticket.message is None else ticket.message)
    print(RAISED_ON, format_date(ticket.created_on))
    print(LINE_BREAK)


def print_tickets_brief(tickets):
    print(LINE_BREAK)
    for ticket in tickets:
        print(TICKET_ID, ticket.t_id)
        print(TITLE, ticket.title)
        print(LINE_BREAK)


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

        if not did_quit:
            print(END_OF_TICKETS)
        user_choice = simple_prompt(continue_prompt, ['y', 'n'])
        if user_choice == 'y':
            system('cls')
            continue
        else:
            break


TICKET_ID = "Ticket ID: "
STATUS = "Status: "
TITLE = "Title: "
DESC = "Description: "
END_OF_TICKETS = "---------------------------That's all the tickets we have---------------------------"
NOT_VALID_EMAIL_PROMPT = "Please enter a valid email address: "
TICKET_DEPT_PROMPT = """
Your issue related to:
Press:
'1': IT department
'2': Sales department
'3': Quality Assurance department
Your choice: """
INVALID_DEPT = "Please enter a valid department: "
TICKET_TITLE_PROMPT = "Title: "
TICKET_TITLE_EMPTY = "Please provide a title: "
TICKET_DESC_PROMPT = "Description: \n"
TICKET_DESC_EMPTY = "Please provide some description: \n"
LINE_BREAK = "----------------------------------------"
STARS = "Stars: "
MESSAGE_FROM_HELPDESK = "Message from helpdesk: "
RAISED_ON = "Raised on: "
DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'


def format_date(date: str) -> str:
    date = datetime.strptime(date, DATE_FORMAT)
    return f"{date.day}/{date.month}/{date.year} at {date.hour}:{date.minute}"
