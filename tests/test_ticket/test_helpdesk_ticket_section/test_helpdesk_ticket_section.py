import pytest
from src.ticket.helpdesk_section.helpdesk_ticket_section import HelpDeskTicketSection
from src.ticket.helpdesk_section.config.helpdesk_ticket_config_loader import HelpdeskTicketConfig


@pytest.fixture(scope='class', autouse=True)
def helpdesk_ticket_section(class_mocker):
    mock_helpdesk = class_mocker.Mock()
    mock_helpdesk.e_id = '1'

    hts = HelpDeskTicketSection(mock_helpdesk)

    return hts


@pytest.fixture
def mock_db_conn(mocker):
    mock_db_conn = mocker.MagicMock()
    mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.DatabaseConnection', mock_db_conn)


@pytest.fixture
def mock_ticket_dao(mocker, mock_db_conn):
    mock_t_dao_cls = mocker.MagicMock()
    mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.TicketDAO', mock_t_dao_cls)
    return mock_t_dao_cls()


class TestHelpdeskTicketSection:

    @pytest.mark.parametrize('inps' , [('e', 'u', 'q')])
    def test_menu_with_unresolved_tickets(self, mocker, helpdesk_ticket_section, inps):
        iter_inps = iter(inps)
        mocker.patch('builtins.input', lambda _: next(iter_inps))

        mock_unresolved_tickets = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'unresolved_tickets', mock_unresolved_tickets)

        helpdesk_ticket_section.menu()
        mock_unresolved_tickets.assert_called_once()

    @pytest.mark.parametrize('inps' , [('e', 'r', 'q')])
    def test_menu_with_resolved_tickets(self, mocker, helpdesk_ticket_section, inps):
        iter_inps = iter(inps)
        mock_resolved_tickets = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'resolved_tickets', mock_resolved_tickets)
        mocker.patch('builtins.input', lambda _: next(iter_inps))
        helpdesk_ticket_section.menu()
        mock_resolved_tickets.assert_called_once()

    def test_menu_with_closed_tickets(self, mocker, helpdesk_ticket_section):
        inps = ('e', 'c', 'q')
        iter_inps = iter(inps)
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))

        mock_closed_tickets = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'closed_tickets', mock_closed_tickets)

        helpdesk_ticket_section.menu()

        mock_closed_tickets.assert_called_once()

    def test_unresolved_tickets_with_resolved_tickets_handler(self, mocker, helpdesk_ticket_section, mock_ticket_dao, sample_tickets):
        inps = iter(['r', 'q', 'n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao.get_all_raised_tickets.return_value = sample_tickets

        mock_resolved_tickets_handler = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'resolve_ticket_handler', mock_resolved_tickets_handler)

        helpdesk_ticket_section.unresolved_tickets()

        mock_resolved_tickets_handler.assert_called_once()

    def test_unresolved_tickets_with_empty_tickets(self, capsys, helpdesk_ticket_section, mock_ticket_dao, sample_tickets):
        mock_ticket_dao.get_all_raised_tickets.return_value = []

        helpdesk_ticket_section.unresolved_tickets()

        captured = capsys.readouterr()

        assert HelpdeskTicketConfig.EMPTY_UNRESOLVED_TICKETS in captured.out

    def test_resolved_tickets_with_close_tickets_handler(self, mocker, helpdesk_ticket_section, mock_ticket_dao, in_prog_tickets):
        inps = iter(('c', 'q', 'n'))
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao.get_all_in_progress_tickets.return_value = in_prog_tickets

        mock_close_tickets_handler = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'close_tickets_handler', mock_close_tickets_handler)

        helpdesk_ticket_section.resolved_tickets()

        mock_close_tickets_handler.assert_called_once()

    def test_resolved_tickets_with_empty_tickets(self, capsys, helpdesk_ticket_section, mock_ticket_dao):
        mock_ticket_dao.get_all_in_progress_tickets.return_value = []

        helpdesk_ticket_section.resolved_tickets()

        captured = capsys.readouterr()

        assert HelpdeskTicketConfig.EMPTY_RESOLVED_TICKETS in captured.out

    def test_closed_tickets_with_view_ticket_detail_handler(self, mocker, helpdesk_ticket_section, mock_ticket_dao, closed_tickets):
        inps = iter(('d', 'q', 'n'))
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao.get_all_closed_tickets.return_value = closed_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'view_ticket_detail_handler', mock_view_ticket_detail_handler)

        helpdesk_ticket_section.closed_tickets()

        mock_view_ticket_detail_handler.assert_called_once()

    def test_resolve_tickets_handler(self, mocker, helpdesk_ticket_section, sample_tickets):
        ticket_ids = iter(('6', '1'))
        mocker.patch('builtins.input', lambda _: next(ticket_ids))

        mock_resolve_tickets_by_id = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'resolve_ticket_by_id', mock_resolve_tickets_by_id)

        helpdesk_ticket_section.resolve_ticket_handler(sample_tickets)

        mock_resolve_tickets_by_id.assert_called_once_with('1')

    def test_close_tickets_handler(self, mocker, helpdesk_ticket_section, sample_tickets):
        ticket_ids = iter(('6', '1'))
        mocker.patch('builtins.input', lambda _: next(ticket_ids))

        mock_close_ticket_by_id = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'close_ticket_by_id', mock_close_ticket_by_id)

        helpdesk_ticket_section.close_tickets_handler(sample_tickets)

        mock_close_ticket_by_id.assert_called_once_with('1')

    def test_resolve_ticket_by_id(self, mocker, helpdesk_ticket_section, mock_ticket_dao):
        ticket_id = '1'
        sample_message = 'sample_message'
        mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.input_message_from_helpdesk', lambda: sample_message)

        mock_change_ticket_status = mocker.Mock()
        mock_assign_repr_id = mocker.Mock()
        mock_update_message_from_helpdesk = mocker.Mock()

        mock_ticket_dao.change_ticket_status = mock_change_ticket_status
        mock_ticket_dao.assign_repr_id = mock_assign_repr_id
        mock_ticket_dao.update_message_from_helpdesk = mock_update_message_from_helpdesk

        helpdesk_ticket_section.resolve_ticket_by_id(ticket_id)

        mock_change_ticket_status.assert_called_once_with('1', HelpdeskTicketConfig.IN_PROGRESS)
        mock_assign_repr_id.assert_called_once_with('1', '1')
        mock_update_message_from_helpdesk.assert_called_once_with(sample_message, '1')

    def test_close_ticket_by_id(self, mocker, helpdesk_ticket_section, mock_ticket_dao):
        ticket_id = '1'
        sample_message = 'sample_message'
        mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.input_message_from_helpdesk', lambda: sample_message)

        mock_change_ticket_status = mocker.Mock()
        mock_update_message_from_helpdesk = mocker.Mock()

        mock_ticket_dao.change_ticket_status = mock_change_ticket_status
        mock_ticket_dao.update_message_from_helpdesk = mock_update_message_from_helpdesk

        helpdesk_ticket_section.close_ticket_by_id(ticket_id)

        mock_change_ticket_status.assert_called_once_with('1', HelpdeskTicketConfig.CLOSED)
        mock_update_message_from_helpdesk.assert_called_once_with(sample_message, '1')
