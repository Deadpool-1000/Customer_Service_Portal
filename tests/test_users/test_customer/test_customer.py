import pytest
from src.users.customer.customer import Customer


class TestCustomer:
    @pytest.fixture(autouse=True)
    def customer_fake(self):
        c = Customer(c_id=1, name='customer_fake', phn_num='test_num', address='test_address, test_city',
                     email='test@gmail.com')
        self.customer = c

    @pytest.fixture
    def mock_ticket_section_raise_ticket(self, mocker):
        mock_raise_ticket = mocker.Mock()
        mocker.patch.object(self.customer.ticket_section, 'raise_ticket', mock_raise_ticket)
        return mock_raise_ticket

    @pytest.fixture
    def mock_ticket_section_view_unresolved_tickets(self, mocker):
        mock_view_unresolved = mocker.Mock()
        mocker.patch.object(self.customer.ticket_section, 'view_unresolved_tickets', mock_view_unresolved)
        return mock_view_unresolved

    @pytest.fixture
    def mock_ticket_section_view_closed_tickets(self, mocker):
        mock_view_closed = mocker.Mock()
        mocker.patch.object(self.customer.ticket_section, 'get_closed_tickets_by_cid', mock_view_closed)
        return mock_view_closed

    @pytest.fixture
    def mock_ticket_section_view_in_progress_tickets(self, mocker):
        mock_view_in_prog = mocker.Mock()
        mocker.patch.object(self.customer.ticket_section, 'view_in_progress_tickets', mock_view_in_prog)
        return mock_view_in_prog

    def test_menu_with_trh(self, mocker, mock_ticket_section_raise_ticket):
        inps = iter([' ', 'r', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.customer.menu()
        mock_ticket_section_raise_ticket.assert_called_once()

    def test_menu_with_rth(self, mocker, mock_ticket_section_view_unresolved_tickets):
        inps = iter([' ', 'u', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.customer.menu()
        mock_ticket_section_view_unresolved_tickets.assert_called_once()

    def test_menu_with_in_prog_tickets(self, mocker, mock_ticket_section_view_in_progress_tickets):
        inps = iter([' ', 'p', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.customer.menu()
        mock_ticket_section_view_in_progress_tickets.assert_called_once()

    def test_menu_with_closed_tickets(self, mocker, mock_ticket_section_view_closed_tickets):
        inps = iter([' ', 'c', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.customer.menu()
        mock_ticket_section_view_closed_tickets.assert_called_once()
