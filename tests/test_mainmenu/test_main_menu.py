import pytest
from src.main_menu.main_menu import MainMenu


@pytest.fixture
def mock_emp_main_menu(mocker):
    mock_emp_mm = mocker.Mock()
    mocker.patch.object(MainMenu, 'employee_main_menu', mock_emp_mm)
    return mock_emp_mm


@pytest.fixture
def mock_cust_main_menu(mocker):
    mock_cust_mm = mocker.Mock()
    mocker.patch.object(MainMenu, 'customer_main_menu', mock_cust_mm)
    return mock_cust_mm


class TestMainMenu:
    @pytest.mark.parametrize('inps', [('p', 'd', 'e'), ('', '  ', 'e')])
    def test_start_menu_with_employee_main_menu(self, mocker, mock_emp_main_menu, inps):
        iter_inps = iter(inps)
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))

        # So the main menu is exited
        mock_emp_main_menu.return_value = False

        MainMenu.start_menu()
        mock_emp_main_menu.assert_called_once()

    @pytest.mark.parametrize('inps', [('p', 'd', 'c'), ('', '  ', 'c')])
    def test_start_menu_with_customer_main_menu(self, mocker, mock_cust_main_menu, inps):
        iter_inps = iter(inps)
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))

        # So the main menu is exited
        mock_cust_main_menu.return_value = False

        MainMenu.start_menu()
        mock_cust_main_menu.assert_called_once()

    def test_employee_main_menu_with_helpdesk(self):
        pass

    def test_employee_main_menu_with_manager(self):
        pass

    def test_employee_main_menu_with_failed_to_login(self):
        pass
