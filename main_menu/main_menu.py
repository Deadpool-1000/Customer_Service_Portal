import logging
from os import system
from users.helpdesk import Helpdesk
from utils.input_utils import menu, simple_prompt
from authentication.login import Login
from authentication.signup import Signup
from users.customer import Customer
from users.manager import Manager
from main_menu.config.main_menu_config_loader import MainMenuConfig

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
            main_function()
            system('cls')

    @classmethod
    def employee_main_menu(cls):
        system('cls')
        print(MainMenuConfig.EMPLOYEE_MAIN_MENU)
        employee = Login.employee_login()

        while employee is None:
            user_choice = simple_prompt(MainMenuConfig.TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                employee = Login.employee_login()
            else:
                return

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
            return

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
                return

            logged_in_customer = Customer(c_id=customer.c_id, name=customer.name, phn_num=customer.phn_num, email=customer.email, address=customer.address)

            system('cls')
            logged_in_customer.menu()

    @classmethod
    def customer_signup_handler(cls):
        print(MainMenuConfig.CUSTOMER_SIGNUP_WELCOME_MESSAGE)
        success = False
        while not success:
            success = Signup.customer_signup()
        system('cls')
        print(MainMenuConfig.SIGNUP_TO_LOGIN_PROMPT)
        return cls.customer_login_handler()

    @staticmethod
    def customer_login_handler():
        print(MainMenuConfig.CUSTOMER_LOGIN_WELCOME_MESSAGE)
        customer = Login.customer_login()
        while customer is None:
            user_choice = simple_prompt(MainMenuConfig.TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                customer = Login.customer_login()
            else:
                logger.info("Customer login failed")
                break
        return customer
