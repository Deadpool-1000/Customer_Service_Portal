from utils.ticket_utils import TICKET_ID, STATUS, TITLE, DESC, LINE_BREAK, STARS, MESSAGE_FROM_HELPDESK, RAISED_ON, \
    format_date

DEFAULT_MESSAGE = "We will get back to you soon."
HELPDESK_MEMBER_ASSIGNED = "Helpdesk member assigned: "
CUSTOMER_ID = "Customer ID: "


def view_list_generator(lst):
    length = len(lst)
    i = 0
    page = 1
    counter = 0
    data = []
    while i < length and counter < 5:
        data.append(lst[i])
        counter += 1
        i += 1
        if counter > 1 or i == length:
            print(f"------Page: {page}------")
            page += 1
            yield data
            data = []
            counter = 0


def print_feedbacks_formatted(feedbacks) -> None:
    for feedback in feedbacks:
        print(TICKET_ID, feedback.t_id)
        print(STARS, '* ' * feedback.stars)
        print(DESC, feedback.desc)
        print(LINE_BREAK)


def print_managers_view(tickets):
    print(LINE_BREAK)
    for ticket in tickets:
        print(TICKET_ID, ticket.t_id)
        print(CUSTOMER_ID, ticket.c_id)
        print(HELPDESK_MEMBER_ASSIGNED, ticket.repr_id if ticket.repr_id is not None else "Yet to be assigned")
        print(TITLE, ticket.title)
        print(DESC, ticket.description)
        print(STATUS, ticket.status)
        print(MESSAGE_FROM_HELPDESK, DEFAULT_MESSAGE if ticket.message is None else ticket.message)
        print(RAISED_ON, format_date(ticket.created_on))
        print(LINE_BREAK)
