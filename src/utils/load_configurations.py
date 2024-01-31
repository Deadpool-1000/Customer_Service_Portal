from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.handlers import CSMConfig


def load_configurations():
    QueriesConfig.load()
    CSMConfig.load()


load_configurations()
