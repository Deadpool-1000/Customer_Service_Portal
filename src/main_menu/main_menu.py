import logging
from os import system

from src.authentication.login import Login
from src.authentication.signup import Signup
from src.main_menu.config.main_menu_config_loader import MainMenuConfig
from src.users.customer.customer import Customer
from src.users.helpdesk.helpdesk import Helpdesk
from src.users.manager.manager import Manager
from src.utils.inputs.input_utils import menu, simple_input

logger = logging.getLogger('main.main_menu')


class MainMenu:

    @classmethod
    def start_menu(cls):
        main_functionalities = {
            'e': cls.employee_main_menu,
            'c': cls.customer_main_menu
        }
        print(MainMenuConfig.COMPANY_LOGO)
        m = menu(MainMenuConfig.MAIN_PROMPT, allowed=['e', 'c'])
        for user_choice in m:
            main_function = main_functionalities.get(user_choice)
            system('cls')
            success = main_function()
            if success is False:
                return

    @classmethod
    def employee_main_menu(cls):
        system('cls')
        print(MainMenuConfig.EMPLOYEE_MAIN_MENU)
        employee = Login.employee_login()

        while employee is not None and employee is False:
            user_choice = simple_input(MainMenuConfig.TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                employee = Login.employee_login()
            else:
                return False

        if employee is None:
            return False

        logger.info(f'Employee e_id:{employee.e_id} and designation:{employee.designation} logged in')
        if employee.designation == MainMenuConfig.HELPDESK:
            h = Helpdesk(name=employee.name, address=employee.address, phn_num=employee.phn_num, e_id=employee.e_id, email=employee.email, dept_id=employee.dept_id)
            system('cls')
            h.menu()
            system('cls')
        elif employee.designation == MainMenuConfig.MANAGER:
            m = Manager(e_id=employee.e_id, name=employee.name, phn_num=employee.phn_num, address=employee.address, email=employee.email)
            system('cls')
            m.menu()
            system('cls')
        else:
            logger.error(f"Invalid employee designation found for employee_id:{employee.e_id}")
            print(MainMenuConfig.SOME_PROBLEM)
            return False

        return True

    @classmethod
    def customer_main_menu(cls):
        system('cls')
        print(MainMenuConfig.CUSTOMER_WELCOME_MESSAGE)

        customer_functionalities = {
            'l': cls.customer_login_handler,
            's': cls.customer_signup_handler
        }
        m = menu(MainMenuConfig.CUSTOMER_MAIN_MENU, allowed=('l', 's'))
        for user_choice in m:
            customer_function = customer_functionalities.get(user_choice)

            system('cls')
            customer = customer_function()

            if customer is None:
                return False

            logged_in_customer = Customer(c_id=customer.c_id, name=customer.name, phn_num=customer.phn_num, email=customer.email, address=customer.address)

            system('cls')
            logged_in_customer.menu()

        return True

    @classmethod
    def customer_signup_handler(cls):
        print(MainMenuConfig.CUSTOMER_SIGNUP_WELCOME_MESSAGE)
        success = Signup.customer_signup()

        while success is not None and success is False:
            user_choice = simple_input(MainMenuConfig.TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                success = Signup.customer_signup()
            else:
                logger.info("Customer Signup failed")
                return None

        # checks if unrecoverable sqlite error occurred
        if success is None:
            return None

        system('cls')

        print(MainMenuConfig.SIGNUP_TO_LOGIN_PROMPT)
        return cls.customer_login_handler()

    @staticmethod
    def customer_login_handler():
        print(MainMenuConfig.CUSTOMER_LOGIN_WELCOME_MESSAGE)
        customer = Login.customer_login()

        while customer is not None and customer is False:
            user_choice = simple_input(MainMenuConfig.TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                system('cls')
                customer = Login.customer_login()
            else:
                logger.info("Customer login failed")
                return None

        # checks if unrecoverable sqlite error occurred
        if customer is None:
            return None

        return customer
