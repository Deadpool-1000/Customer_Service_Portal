import pytest
from src.ticket.manager_section.manager_ticket_section import ManagerTicketSection


@pytest.fixture(scope='class')
def manager_ticket_section(class_mocker):
    mock_manager = class_mocker.Mock()
    m = ManagerTicketSection(mock_manager)
    return m


@pytest.fixture
def mock_db_conn(mocker):
    mock_db_conn = mocker.MagicMock()
    mocker.patch('src.ticket.manager_section.manager_ticket_section.DatabaseConnection', mock_db_conn)


@pytest.fixture
def mock_ticket_dao(mocker, mock_db_conn):
    mock_t_dao_cls = mocker.MagicMock()
    mocker.patch('src.ticket.manager_section.manager_ticket_section.TicketDAO', mock_t_dao_cls)
    return mock_t_dao_cls()


class TestManagerTicketSection:
    def test_menu_with_view_all_tickets(self, mocker, manager_ticket_section):
        inps = iter(('a', 'q'))
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_view_all_tickets = mocker.Mock()
        mocker.patch.object(manager_ticket_section, 'view_all_tickets', mock_view_all_tickets)

        manager_ticket_section.menu()

        mock_view_all_tickets.assert_called_once()

    def test_view_all_tickets_with_detail_handler(self, mocker, manager_ticket_section, mock_ticket_dao, sample_tickets):
        inps = iter(('d', 'q', 'n'))
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao.get_all_tickets.return_value = sample_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(manager_ticket_section, 'view_ticket_detail_handler', mock_view_ticket_detail_handler)

        manager_ticket_section.view_all_tickets()

        mock_view_ticket_detail_handler.assert_called_once()
