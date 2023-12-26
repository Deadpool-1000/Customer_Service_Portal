import logging
from os import system, path
from src.main_menu.main_menu import MainMenu
from src.utils.load_configurations import load_configurations

path_current_directory = path.dirname(__file__)
LOG_FILE_PATH = path.join(path_current_directory, 'utils/logs/logs.log')


logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename=LOG_FILE_PATH)
logger = logging.getLogger("main")


def entry_point(f):
    if f.__module__ == '__main__':
        f()

    return f


@entry_point
@load_configurations
def main():
    logger.info('App started')
    system('cls')
    MainMenu.start_menu()
    logger.info('App ended')
