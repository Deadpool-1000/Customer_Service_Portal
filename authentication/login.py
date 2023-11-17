import logging
import sqlite3

from DBUtils.auth.authdao import AuthDAO
from utils.input_utils import input_email_password
from utils.named_tuples import Customer, Employee
from utils.exceptions import InvalidUsernameOrPasswordException, InvalidEmployeeIDException, InvalidDepartmentIDException
from DBUtils.customer.customerdao import CustomerDAO
from DBUtils.employee.employeedao import EmployeeDAO
from DBUtils.connection.database_connection import DatabaseConnection
from authentication.config.auth_config_loader import AuthConfig

logger = logging.getLogger('main.login')


class Login:
    @classmethod
    def employee_login(cls):
        email, password = input_email_password()

        try:
            with DatabaseConnection() as conn:
                a_dao = AuthDAO(conn)
                e_id = a_dao.login_user(email, password, AuthConfig.EMP_AUTH)
                e_dao = EmployeeDAO(conn)
                employee = e_dao.get_employee_details_by_id(e_id)
                department_details = e_dao.get_department_by_id(employee[3])
                e = Employee(name=employee[1], e_id=employee[0], phn_num=employee[2], address=employee[4], email=email, dept_id=employee[3], dept_name=department_details[1], designation=employee[5])
                logger.info(f"Employee with e_id:{e.e_id}, name:{e.name} logged in")
            return e

        except InvalidUsernameOrPasswordException as ie:
            logger.error(f'[Employee]: {ie} with email:{email} and password:{password}')
            print(ie)
            return False
        except InvalidEmployeeIDException as ei:
            logger.error(f'{ei} with email:{email} and password:{password}')
            print(ei)
            return False
        except InvalidDepartmentIDException as idi:
            logger.error(f'{idi} with email:{email} and password:{password}')
            print(idi)
            return False
        except sqlite3.Error as err:
            logger.error(f'Employee login: {err.sqlite_errorname}')
            print('There was a problem logging you in')
            print('Please try again after some time')
            return None

    @staticmethod
    def customer_login():
        email, password = input_email_password()
        try:
            with DatabaseConnection() as conn:
                a_dao = AuthDAO(conn)
                c_id = a_dao.login_user(email, password, AuthConfig.CUST_AUTH)
                c_dao = CustomerDAO(conn)
                customer = c_dao.get_customer_details_by_id(c_id)
                c = Customer(name=customer[1], c_id=customer[0], phn_num=customer[2], address=customer[3], email=email)
                logger.info(f"Employee with e_id:{c.c_id}, name:{c.name} logged in")
            return c
        except InvalidUsernameOrPasswordException as iup:
            logger.error(f'[Customer]: {iup} with email:{email} and password:{password}')
            print(iup)
            return False
        except sqlite3.Error as err:
            logger.error(f'Customer login: {err.sqlite_errorname}')
            print('There was a problem logging you in')
            print('Please try again after some time')
            return None

