import pytest
from src.ticket.helpdesk_section.helpdesk_ticket_section import HelpDeskTicketSection


@pytest.fixture
def helpdesk_ticket_section(mocker):
    mock_db_conn = mocker.Mock()
    hts = HelpDeskTicketSection(mock_db_conn)
    return hts


class TestHelpdeskTicketSection:
    @pytest.mark.parametrize('inps' , [('e', 'u', 'q')])
    def test_menu_with_unresolved_tickets(self, mocker, helpdesk_ticket_section, inps):
        iter_inps = iter(inps)
        mock_unresolved_tickets = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'unresolved_tickets', mock_unresolved_tickets)
        mocker.patch('builtins.input', lambda _: next(iter_inps))
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

    @pytest.mark.parametrize('inps' , [('e', 'c', 'q')])
    def test_menu_with_closed_tickets(self, mocker, helpdesk_ticket_section, inps):
        iter_inps = iter(inps)
        mock_closed_tickets = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'closed_tickets', mock_closed_tickets)
        mocker.patch('builtins.input', lambda _: next(iter_inps))
        helpdesk_ticket_section.menu()
        mock_closed_tickets.assert_called_once()

    @pytest.mark.parametrize('t_id', [('6', '1')])
    def test_resolved_tickets_handler(self, mocker, helpdesk_ticket_section, sample_tickets, t_id):
        t_id = iter(t_id)

        mocker.patch('builtins.input', lambda _: next(t_id))
        mock_resolve_tickets_by_id = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'resolve_ticket_by_id', mock_resolve_tickets_by_id)

        helpdesk_ticket_section.resolved_tickets_handler(sample_tickets)

        mock_resolve_tickets_by_id.assert_called_once_with('1')

    @pytest.mark.parametrize('t_id', [('6', '1')])
    def test_closed_tickets_handler(self, mocker, helpdesk_ticket_section, sample_tickets, t_id):
        t_id = iter(t_id)

        mocker.patch('builtins.input', lambda _: next(t_id))
        mock_close_ticket_by_id = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'close_ticket_by_id', mock_close_ticket_by_id)

        helpdesk_ticket_section.close_tickets_handler(sample_tickets)

        mock_close_ticket_by_id.assert_called_once_with('1')

    def test_unresolved_tickets_with_resolved_tickets_handler(self, helpdesk_ticket_section, mocker, sample_tickets):
        mock_db_conn = mocker.MagicMock()
        mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.DatabaseConnection', mock_db_conn)
        mock_t_dao_cls = mocker.MagicMock()
        mocker.patch('src.ticket.helpdesk_section.helpdesk_ticket_section.TicketDAO', mock_t_dao_cls)
        mock_t_dao_cls().view_all_raised_tickets.return_value = sample_tickets

        mock_resolved_tickets_handler = mocker.Mock()
        mocker.patch.object(helpdesk_ticket_section, 'resolved_tickets_handler', mock_resolved_tickets_handler)

        inps = iter(['r', 'q', 'n'])
        mocker.patch('builtins.input', lambda _: next(inps))

        helpdesk_ticket_section.unresolved_tickets()

        mock_resolved_tickets_handler.assert_called_once()

    def test_unresolved_tickets_with_view_ticket_detail_handler(self, helpdesk_ticket_section, mocker, sample_tickets):
        pass
