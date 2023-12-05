import pytest
from src.main_menu.main_menu import MainMenu
from src.utils.data_containers.named_tuples import Employee


sample_employee = Employee(
    e_id=1,
    name='test_employee',
    email='test@gmail.com',
    address='test_address, test_city',
    phn_num='test_phn_num',
    dept_name='IT',
    dept_id='1',
    designation='helpdesk'
)


sample_manager = Employee(
    e_id=1,
    name='test_employee',
    email='test@gmail.com',
    address='test_address, test_city',
    phn_num='test_phn_num',
    dept_name='IT',
    dept_id='1',
    designation='manager'
)


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

    def test_employee_main_menu_with_helpdesk(self, mocker):
        inps = iter(['e', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mocker.patch('src.main_menu.main_menu.Login.employee_login', lambda : sample_employee)

        mock_helpdesk = mocker.Mock()
        mocker.patch('src.main_menu.main_menu.Helpdesk', mock_helpdesk)

        MainMenu.start_menu()

        mock_helpdesk.assert_called_once()

    def test_employee_main_menu_with_manager(self, mocker):
        inps = iter(['e', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mocker.patch('src.main_menu.main_menu.Login.employee_login', lambda: sample_manager)

        mock_manager = mocker.Mock()
        mocker.patch('src.main_menu.main_menu.Manager', mock_manager)

        MainMenu.start_menu()

        mock_manager.assert_called_once()

    def test_employee_main_menu_with_fatal_error(self, mocker):
        inps = iter(['e', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        mocker.patch('src.main_menu.main_menu.Login.employee_login', lambda: None)

        success = MainMenu.employee_main_menu()

        assert success is False

    def test_employee_main_menu_with_failed_to_login(self, mocker):
        inps = iter(['n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mocker.patch('src.main_menu.main_menu.Login.employee_login', lambda: False)

        success = MainMenu.employee_main_menu()

        assert success is False

    def test_employee_main_menu_with_retry_login(self, mocker):
        inps = iter(['y'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        emp_login = iter([False, sample_employee])
        mocker.patch('src.main_menu.main_menu.Login.employee_login', lambda: next(emp_login))

        mock_helpdesk = mocker.Mock()
        mocker.patch('src.main_menu.main_menu.Helpdesk', mock_helpdesk)
        success = MainMenu.employee_main_menu()

        assert success is True

