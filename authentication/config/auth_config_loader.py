import yaml

AUTH_CONFIG_FILE_PATH = 'authentication/config/auth.yml'


class AuthConfig:
    EMP_AUTH = None
    CUST_AUTH = None
    PLEASE_TRY_AGAIN = None

    @classmethod
    def load(cls):
        with open(AUTH_CONFIG_FILE_PATH, 'r') as file:
            data = yaml.safe_load(file)
            cls.EMP_AUTH = data['EMP_AUTH']
            cls.CUST_AUTH = data['CUST_AUTH']
            cls.PLEASE_TRY_AGAIN = data['PLEASE_TRY_AGAIN']

