import yaml

DB_CONFIG_FILE_PATH = 'DBUtils/config/db.yml'


class DBConfig:
    DB_FILE_PATH = None
    ALREADY_EXISTS_EXCEPTION = None
    INVALID_USERNAME_OR_PASSWORD = None
    INVALID_USERNAME_LOG = None
    INVALID_PASSWORD_LOG = None
    INVALID_CUST_ID = None
    INVALID_DEPT_ID = None
    INVALID_EMP_ID = None
    THERE_WAS_SOME_PROBLEM = None
    WE_WILL_GET_BACK = None
    IN_PROGRESS = None
    RAISED = None
    CLOSED = None

    @classmethod
    def load(cls):
        with open(DB_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.ALREADY_EXISTS_EXCEPTION = data['ALREADY_EXISTS_EXCEPTION']
            cls.DB_FILE_PATH = data['DB_FILE_PATH']
            cls.INVALID_USERNAME_OR_PASSWORD = data['INVALID_USERNAME_OR_PASSWORD']
            cls.INVALID_USERNAME_LOG = data['INVALID_USERNAME_LOG']
            cls.INVALID_PASSWORD_LOG = data['INVALID_PASSWORD_LOG']
            cls.INVALID_CUST_ID = data['INVALID_CUST_ID']
            cls.INVALID_DEPT_ID = data['INVALID_DEPT_ID']
            cls.INVALID_EMP_ID = data['INVALID_EMP_ID']
            cls.THERE_WAS_SOME_PROBLEM = data['THERE_WAS_SOME_PROBLEM']
            cls.WE_WILL_GET_BACK = data['WE_WILL_GET_BACK']
            cls.IN_PROGRESS = data['IN_PROGRESS']
            cls.RAISED = data['RAISED']
            cls.CLOSED = data['CLOSED']
