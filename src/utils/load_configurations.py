from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.authentication.config.auth_config_loader import AuthConfig
from src.ticket.customer_section.config.customer_ticket_config_loader import CustomerTicketConfig
from src.ticket.helpdesk_section.config.helpdesk_ticket_config_loader import HelpdeskTicketConfig
from src.ticket.manager_section.config.manager_ticket_config_loader import ManagerTicketConfig
from src.utils.config.utils_config_loader import UtilsConfig


def load_configurations():
    AuthConfig.load()
    DBConfig.load()
    QueriesConfig.load()
    CustomerTicketConfig.load()
    HelpdeskTicketConfig.load()
    ManagerTicketConfig.load()
    UtilsConfig.load()
