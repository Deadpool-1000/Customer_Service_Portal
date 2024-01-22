from src.DBUtils.config.db_config_loader import DBConfig
from src.DBUtils.config.queries_config_loader import QueriesConfig
from src.authentication.config.auth_config_loader import AuthConfig
from src.main_menu.config.main_menu_config_loader import MainMenuConfig
from src.ticket.customer_section.config.customer_ticket_config_loader import CustomerTicketConfig
from src.ticket.helpdesk_section.config.helpdesk_ticket_config_loader import HelpdeskTicketConfig
from src.ticket.manager_section.config.manager_ticket_config_loader import ManagerTicketConfig
from src.users.config.users_config_loader import UsersConfig
from src.utils.config.utils_config_loader import UtilsConfig


def load_configurations():
    AuthConfig.load()
    DBConfig.load()
    QueriesConfig.load()
    MainMenuConfig.load()
    CustomerTicketConfig.load()
    HelpdeskTicketConfig.load()
    ManagerTicketConfig.load()
    UsersConfig.load()
    UtilsConfig.load()
