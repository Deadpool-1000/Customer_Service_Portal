from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.authentication.config.auth_config_loader import AuthConfig
from src.utils.config.utils_config_loader import UtilsConfig
from src.handlers import CSMConfig


def load_configurations():
    AuthConfig.load()
    DBConfig.load()
    QueriesConfig.load()
    UtilsConfig.load()
    CSMConfig.load()
