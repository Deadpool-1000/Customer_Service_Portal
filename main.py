import logging
from main_menu import MainMenu
from os import system

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s",
                    datefmt="%d-%M-%Y %H:%M:%S", level=logging.DEBUG, filename='utils/logs.log')
logger = logging.getLogger("main")

if __name__ == "__main__":
    system('cls')
    MainMenu.start_menu()

