from DBUtils.auth.authdao import AuthDAO
from utils.input_utils import input_email_password, simple_prompt
from utils.named_tuples import Customer, Employee
from utils.exceptions import InvalidUsernameOrPasswordException, InvalidEmployeeIDException, InvalidDepartmentIDException
from DBUtils.customer.customerdao import CustomerDAO
from DBUtils.employee.employeedao import EmployeeDAO
from DBUtils.connection.database_connection import DatabaseConnection


class Login:

    @classmethod
    def employee_login(cls):
        email, password = input_email_password()

        try:
            with DatabaseConnection() as conn:
                a_dao = AuthDAO(conn)
                e_id = a_dao.login_user(email, password, 'emp_auth')
                e_dao = EmployeeDAO(conn)
                employee = e_dao.get_employee_details_by_id(e_id)
                department_details = e_dao.get_department_by_id(employee[3])
                e = Employee(name=employee[1], e_id=employee[0], phn_num=employee[2], address=employee[4], email=email, dept_id=employee[3], dept_name=department_details[1], designation=employee[5])
            return e

        except InvalidUsernameOrPasswordException as ie:
            print(ie)
            return None
        except InvalidEmployeeIDException as ei:
            print(ei)
            return None
        except InvalidDepartmentIDException as idi:
            print(idi)
            return None

    @staticmethod
    def customer_login():

        email, password = input_email_password()
        try:
            with DatabaseConnection() as conn:
                a_dao = AuthDAO(conn)
                c_id = a_dao.login_user(email, password, 'cust_auth')
                c_dao = CustomerDAO(conn)
                customer = c_dao.get_customer_details_by_id(c_id)
                c = Customer(name=customer[1], c_id=customer[0], phn_num=customer[2], address=customer[3], email=email)
            return c
        except InvalidUsernameOrPasswordException as iup:
            print(iup)
            return None

