import re
from typing import Iterable
from maskpass import advpass
from utils.config.utils_config_loader import UtilsConfig


def input_email_password() -> (str, str):
    email = input(UtilsConfig.EMAIL_PROMPT).strip()
    while len(email) == 0:
        email = input(UtilsConfig.EMAIL_EMPTY_PROMPT).strip()

    password = advpass(UtilsConfig.PASSWORD_PROMPT).strip()
    while len(password) == 0:
        password = advpass(UtilsConfig.PASSWORD_EMPTY_PROMPT).strip()

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
                user_choice = input(UtilsConfig.INVALID_INPUT).strip().lower()
            if user_choice == 'q':
                continue
        yield user_choice
        user_choice = input(prompt).strip().lower()


def input_customer_details() -> (str, str, str, str, str):
    email = input(UtilsConfig.EMAIL_PROMPT).strip()
    while len(email) == 0:
        email = input(UtilsConfig.EMAIL_EMPTY_PROMPT).strip()
    while not validator(UtilsConfig.EMAIL_REGEX, email):
        email = input(UtilsConfig.VALID_EMAIL).strip()

    fullname = input(UtilsConfig.FULL_NAME_PROMPT).strip()
    while len(fullname) == 0:
        fullname = input(UtilsConfig.FULLNAME_EMPTY).strip()

    phn_num = input(UtilsConfig.PHONE_NUMBER_PROMPT).strip()
    while len(phn_num) == 0:
        phn_num = input(UtilsConfig.PHONE_NUMBER_EMPTY).strip()

    address = input(UtilsConfig.ADDRESS_PROMPT).strip()
    while len(address) == 0:
        address = input(UtilsConfig.ADDRESS_EMPTY).strip()

    password = advpass(UtilsConfig.PASSWORD_PROMPT).strip()
    while len(password) == 0:
        password = advpass(UtilsConfig.PASSWORD_EMPTY_PROMPT).strip()
    while not validator(UtilsConfig.PASSWORD_REGEX, password):
        password = advpass(UtilsConfig.STRONG_PASSWORD_PROMPT).strip()

    return email, fullname, phn_num, address, password


def simple_prompt(prompt, allowed: Iterable) -> str:
    user_choice = input(prompt).strip().lower()

    while user_choice not in allowed:
        user_choice = input(UtilsConfig.INVALID_INPUT).strip().lower()

    return user_choice


def input_feedback_body() -> (str, str):
    stars = int(input(UtilsConfig.INPUT_FEEDBACK_STARS))
    desc = input(UtilsConfig.INPUT_FEEDBACK_DESC)
    return stars, desc


def input_message_from_helpdesk() -> str:
    message = input(UtilsConfig.INPUT_MESSAGE_FROM_HELPDESK).strip()
    while len(message) == 0:
        message = input(UtilsConfig.MESSAGE_CANT_BE_EMPTY).strip()
    return message
