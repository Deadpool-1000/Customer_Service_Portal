import logging
from os import system
from authentication.config.auth_config_loader import AuthConfig
from DBUtils.config.db_config_loader import DBConfig
from DBUtils.config.queries_config_loader import QueriesConfig
from main_menu.config.main_menu_config_loader import MainMenuConfig
from ticket.customer_section.config.customer_ticket_config_loader import CustomerTicketConfig
from ticket.helpdesk_section.config.helpdesk_ticket_config_loader import HelpdeskTicketConfig
from ticket.manager_section.config.manager_ticket_config_loader import ManagerTicketConfig
from users.config.users_config_loader import UsersConfig
from utils.config.utils_config_loader import UtilsConfig
from main_menu.main_menu import MainMenu

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename='utils/logs.log')
logger = logging.getLogger("main")

if __name__ == "__main__":
    logger.info('App started')
    system('cls')
    # Loading the configuration
    AuthConfig.load()
    DBConfig.load()
    QueriesConfig.load()
    MainMenuConfig.load()
    CustomerTicketConfig.load()
    HelpdeskTicketConfig.load()
    ManagerTicketConfig.load()
    UsersConfig.load()
    UtilsConfig.load()
    # Starting the main menu
    MainMenu.start_menu()
    logger.info('App ended')
