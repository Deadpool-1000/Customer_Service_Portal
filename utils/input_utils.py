import re
from typing import Iterable

from maskpass import advpass

EMAIL_PROMPT = "Email: "
PASSWORD_PROMPT = "Password: "
FULL_NAME_PROMPT = "Full Name: "
PHONE_NUMBER_PROMPT = "Phone Number: "
ADDRESS_PROMPT = "Address: "
PHONE_NUMBER_EMPTY = "Phone Number can't be empty: "
ADDRESS_EMPTY = "Address can't be empty: "
FULLNAME_EMPTY = "Full Name can't be empty: "
EMAIL_EMPTY_PROMPT = "Email can't be empty: "
PASSWORD_EMPTY_PROMPT = "Password can't be empty: "
EMAIL_REGEX = r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
PASSWORD_REGEX = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$"
STRONG_PASSWORD_PROMPT = """
Your password must contain:
  1. Minimum eight characters, 
  2. at least one uppercase letter,
  3. one lowercase letter and one number
New Password: """
INVALID_INPUT = "Invalid Input: "
INPUT_MESSAGE_FROM_HELPDESK = "Please enter a message for the customer: "
MESSAGE_CANT_BE_EMPTY = "Message can't be left empty"
INPUT_FEEDBACK_STARS = "Please enter number of stars you want to rate the response: "
INPUT_FEEDBACK_DESC = "Enter description for your feedback: "
VALID_EMAIL = "Please enter a valid email: "


def input_email_password() -> (str, str):
    email = input(EMAIL_PROMPT).strip()
    while len(email) == 0:
        email = input(EMAIL_EMPTY_PROMPT).strip()

    password = advpass(PASSWORD_PROMPT).strip()
    while len(password) == 0:
        password = advpass(PASSWORD_EMPTY_PROMPT).strip()

    return email, password


def validator(rg, txt) -> bool:
    if not re.match(rg, txt):
        return False
    return True


def menu(prompt: str, allowed: Iterable) -> str:
    """
    generator for menu that renders menu prompt repetitively and provides some basic input validation
    :yield str (user choice: a single character)
    """
    user_choice = input(prompt).strip().lower()
    while user_choice != 'q':
        if user_choice not in allowed:
            while user_choice not in allowed and user_choice != 'q':
                user_choice = input(INVALID_INPUT).strip().lower()
            if user_choice == 'q':
                continue
        yield user_choice
        user_choice = input(prompt).strip().lower()


def input_customer_details() -> (str, str, str, str, str):
    email = input(EMAIL_PROMPT).strip()
    while len(email) == 0:
        email = input(EMAIL_EMPTY_PROMPT).strip()
    while not validator(EMAIL_REGEX, email):
        email = input(VALID_EMAIL).strip()

    fullname = input(FULL_NAME_PROMPT).strip()
    while len(fullname) == 0:
        fullname = input(FULLNAME_EMPTY).strip()

    phn_num = input(PHONE_NUMBER_PROMPT).strip()
    while len(phn_num) == 0:
        phn_num = input(PHONE_NUMBER_EMPTY).strip()

    address = input(ADDRESS_PROMPT).strip()
    while len(address) == 0:
        address = input(ADDRESS_EMPTY).strip()

    password = advpass(PASSWORD_PROMPT).strip()
    while len(password) == 0:
        password = advpass(PASSWORD_EMPTY_PROMPT).strip()
    while not validator(PASSWORD_REGEX, password):
        password = advpass(STRONG_PASSWORD_PROMPT).strip()

    return email, fullname, phn_num, address, password


def simple_prompt(prompt, allowed: Iterable) -> str:
    user_choice = input(prompt).strip().lower()

    while user_choice not in allowed:
        user_choice = input(INVALID_INPUT).strip().lower()

    return user_choice


def input_feedback_body() -> (str, str):
    stars = int(input(INPUT_FEEDBACK_STARS))
    desc = input(INPUT_FEEDBACK_DESC)
    return stars, desc


def input_message_from_helpdesk() -> str:
    message = input(INPUT_MESSAGE_FROM_HELPDESK).strip()
    while len(message) == 0:
        message = input(MESSAGE_CANT_BE_EMPTY).strip()
    return message
