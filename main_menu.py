from os import system
from users.helpdesk import Helpdesk
from utils.input_utils import menu, simple_prompt
from authentication.login import Login
from authentication.signup import Signup
from users.customer import Customer
from users.manager import Manager

COMPANY_LOGO = '----------------------------------ABC Customer Service Portal----------------------------------'
MAIN_PROMPT = """
Press 
'e': if you are an employee
'c': if you are a customer,
'q': quit
Your Choice: """
EMPLOYEE_MAIN_MENU = "Hi there welcome, remember our moto 'Customer satisfaction is our priority'"
CUSTOMER_WELCOME_MESSAGE = "Hi there welcome, please tell us what do you want to do?"
CUSTOMER_MAIN_MENU = """
Press
'l': login
's': signup
'q': quit
Your Choice: """
SIGNUP_TO_LOGIN_PROMPT = "Successfully Signed up, Please Login to continue to our service portal"
PLEASE_TRY_AGAIN = "Please Try Again"
CUSTOMER_SIGNUP_WELCOME_MESSAGE = "Welcome to signup, Please enter the following details, so that we can get you started with our services"
CUSTOMER_LOGIN_WELCOME_MESSAGE = "For Login enter the following details:"
SOME_PROBLEM = "There was some problem, please try again later"
TRY_AGAIN_OR_QUIT = 'Do you want to try again?(y/n): '
HELPDESK = 'helpdesk'
MANAGER = 'manager'


class MainMenu:

    @classmethod
    def start_menu(cls):
        main_functionalities = {
            'e': cls.employee_main_menu,
            'c': cls.customer_main_menu
        }
        print(COMPANY_LOGO)
        m = menu(MAIN_PROMPT, allowed=['e', 'c'])
        for user_choice in m:
            main_function = main_functionalities.get(user_choice)
            system('cls')
            main_function()
            system('cls')

    @classmethod
    def employee_main_menu(cls):
        system('cls')
        print(EMPLOYEE_MAIN_MENU)
        employee = Login.employee_login()

        while employee is None:
            user_choice = simple_prompt(TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                employee = Login.employee_login()
            else:
                return

        if employee.designation == HELPDESK:
            h = Helpdesk(name=employee.name, address=employee.address, phn_num=employee.phn_num, e_id=employee.e_id, email=employee.email, dept_id=employee.dept_id)
            system('cls')
            h.menu()
            system('cls')
        elif employee.designation == MANAGER:
            m = Manager(e_id=employee.e_id, name=employee.name, phn_num=employee.phn_num, address=employee.address, email=employee.email)
            system('cls')
            m.menu()
            system('cls')
        else:
            print(SOME_PROBLEM)
            return

    @classmethod
    def customer_main_menu(cls):
        system('cls')
        print(CUSTOMER_WELCOME_MESSAGE)

        customer_functionalities = {
            'l': cls.customer_login_handler,
            's': cls.customer_signup_handler
        }
        m = menu(CUSTOMER_MAIN_MENU, allowed=('l', 's'))
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
        print(CUSTOMER_SIGNUP_WELCOME_MESSAGE)
        success = False
        while not success:
            success = Signup.customer_signup()
        system('cls')
        print(SIGNUP_TO_LOGIN_PROMPT)
        return cls.customer_login_handler()

    @staticmethod
    def customer_login_handler():
        print(CUSTOMER_LOGIN_WELCOME_MESSAGE)
        customer = Login.customer_login()
        while customer is None:
            user_choice = simple_prompt(TRY_AGAIN_OR_QUIT, allowed=('y', 'n'))
            if user_choice == 'y':
                customer = Login.customer_login()
            else:
                break
        return customer
