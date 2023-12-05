import pytest
from src.ticket.customer_section.customer_ticket_section import CustomerTicketSection
from src.utils.data_containers.named_tuples import Ticket


@pytest.fixture(autouse=True)
def mock_db_connection(mocker):
    db_conn = mocker.MagicMock()
    mock_conn = mocker.MagicMock()
    mocker.patch('src.ticket.customer_section.customer_ticket_section.DatabaseConnection', db_conn)
    db_conn().__enter__.return_value = mock_conn


@pytest.fixture
def mock_ticket_dao(mocker):
    t_dao = mocker.Mock()
    mocker.patch('src.ticket.customer_section.customer_ticket_section.TicketDAO', t_dao)
    return t_dao


@pytest.fixture
def mock_feedback_dao(mocker):
    f_dao = mocker.Mock()
    mocker.patch('src.ticket.customer_section.customer_ticket_section.FeedbackDAO', f_dao)
    return f_dao


@pytest.fixture(scope='class', autouse=True)
def cts(class_mocker):
    dummy_customer = class_mocker.Mock()
    dummy_customer.c_id = 1
    cts = CustomerTicketSection(dummy_customer)
    print("*********************************fake customer created*****************************************")
    return cts


class TestCustomerTicketSection:
    def test_raise_ticket(self, mocker, mock_ticket_dao, cts):
        mocker.patch('src.ticket.customer_section.customer_ticket_section.input_ticket', lambda: ('1', 'test_title', 'test_description'))
        mock_create_new_ticket = mocker.Mock()
        mock_ticket_dao().create_new_ticket = mock_create_new_ticket
        cts.raise_ticket()
        mock_create_new_ticket.assert_called_once_with(d_id='1', c_id=1, desc='test_description', title='test_title')

    def test_register_feedback(self, mock_feedback_dao, mocker, cts):
        mocker.patch('src.ticket.customer_section.customer_ticket_section.input_feedback_body', lambda: (5, 'sample_desc'))
        mock_add_feedback = mocker.Mock()
        mock_feedback_dao().add_feedback = mock_add_feedback
        cts.register_feedback(111)
        mock_add_feedback.assert_called_once_with(5, 'sample_desc', 111)

    def test_view_ticket_detail_handler_with_open_tickets(self, mocker, sample_tickets, cts):
        inps = iter(['2', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        ret_val = cts.view_ticket_detail_handler(sample_tickets)
        assert ret_val is None

    def test_view_ticket_detail_handler_with_closed_tickets(self, mocker, closed_tickets, cts):
        inps = iter(['2', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        ret_val = cts.view_ticket_detail_handler(closed_tickets)
        assert ret_val is None

    def test_view_ticket_detail_handler_with_feedback_option(self, mocker, closed_tickets, cts):
        inps = iter(['2', 'f'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_register_feedback = mocker.Mock()
        mocker.patch.object(cts, 'register_feedback', mock_register_feedback)

        cts.view_ticket_detail_handler(closed_tickets)
        mock_register_feedback.assert_called_once()

    def test_view_ticket_detail_handler_with_quit(self, mocker, sample_tickets, cts):
        inps = iter(['p', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        ret_val = cts.view_ticket_detail_handler(sample_tickets)
        assert ret_val is None

    def test_give_feedback_handler(self, mocker, closed_tickets, cts):
        inps = iter(['p', '2', 'f'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_register_feedback = mocker.Mock()
        mocker.patch.object(cts, 'register_feedback', mock_register_feedback)

        cts.give_feedback_handler(closed_tickets)
        mock_register_feedback.assert_called_once()

    def test_view_unresolved_tickets_with_detail_handler(self, mocker, raised_tickets, mock_ticket_dao, cts):
        inps = iter(['d', 'q', 'n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao().view_raised_tickets.return_value = raised_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(cts, 'view_ticket_detail_handler', mock_view_ticket_detail_handler)

        cts.view_unresolved_tickets()

        mock_view_ticket_detail_handler.assert_called_once()

    def test_view_unresolved_tickets_with_empty_tickets(self, capsys, raised_tickets, mock_ticket_dao, cts):
        mock_ticket_dao().view_raised_tickets.return_value = []
        expected_message = "There are no unresolved tickets yet"

        cts.view_unresolved_tickets()

        captured = capsys.readouterr()

        assert expected_message in captured.out

    def test_view_closed_tickets_with_detail_handler(self, mocker, closed_tickets, mock_ticket_dao, cts):
        inps = iter(['d', 'q', 'n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao().view_closed_tickets.return_value = closed_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(cts, 'view_ticket_detail_handler', mock_view_ticket_detail_handler)

        cts.view_closed_tickets()

        mock_view_ticket_detail_handler.assert_called_once()

    def test_view_closed_tickets_with_empty_tickets(self, capsys, closed_tickets, mock_ticket_dao, cts):
        mock_ticket_dao().view_closed_tickets.return_value = []
        expected_message = "There are no closed tickets yet"

        cts.view_closed_tickets()

        captured = capsys.readouterr()

        assert expected_message in captured.out

    def test_view_closed_tickets_with_feedback_handler(self, mocker, closed_tickets, mock_ticket_dao, cts):
        inps = iter(['f', 'q', 'n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao().view_closed_tickets.return_value = closed_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(cts, 'give_feedback_handler', mock_view_ticket_detail_handler)

        cts.view_closed_tickets()

        mock_view_ticket_detail_handler.assert_called_once()

    def test_view_in_progress_tickets_with_detail_handler(self, mocker, in_prog_tickets, mock_ticket_dao, cts):
        inps = iter(['d', 'q', 'n'])
        mocker.patch('builtins.input', lambda prompt: next(inps))

        mock_ticket_dao().view_in_progress_ticket.return_value = in_prog_tickets

        mock_view_ticket_detail_handler = mocker.Mock()
        mocker.patch.object(cts, 'view_ticket_detail_handler', mock_view_ticket_detail_handler)

        cts.view_in_progress_tickets()

        mock_view_ticket_detail_handler.assert_called_once()

    def test_view_in_progress_tickets_with_empty_tickets(self, capsys, in_prog_tickets, mock_ticket_dao, cts):
        mock_ticket_dao().view_in_progress_ticket.return_value = []
        expected_message = "There are no in-progress tickets yet"

        cts.view_in_progress_tickets()

        captured = capsys.readouterr()

        assert expected_message in captured.out
