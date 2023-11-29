from datetime import datetime

from src.utils.config.utils_config_loader import UtilsConfig


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
        print(UtilsConfig.TICKET_ID, feedback.t_id)
        print(UtilsConfig.STARS, '* ' * feedback.stars)
        print(UtilsConfig.DESC, feedback.desc)
        print(UtilsConfig.LINE_BREAK)


def print_managers_view(tickets):
    print(UtilsConfig.LINE_BREAK)
    for ticket in tickets:
        print(UtilsConfig.TICKET_ID, ticket.t_id)
        print(UtilsConfig.CUSTOMER_ID, ticket.c_id)
        print(UtilsConfig.HELPDESK_MEMBER_ASSIGNED, ticket.repr_id if ticket.repr_id is not None else "Yet to be assigned")
        print(UtilsConfig.TITLE, ticket.title)
        print(UtilsConfig.DESC, ticket.description)
        print(UtilsConfig.STATUS, ticket.status)
        print(UtilsConfig.MESSAGE_FROM_HELPDESK, UtilsConfig.DEFAULT_MESSAGE if ticket.message is None else ticket.message)
        print(UtilsConfig.RAISED_ON, format_date(ticket.created_on))
        print(UtilsConfig.LINE_BREAK)


def format_date(date):
    try:
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        raise ValueError('There was some problem please try again later')
    else:
        return f"{date.day}/{date.month}/{date.year} at {date.hour}:{date.minute}"
