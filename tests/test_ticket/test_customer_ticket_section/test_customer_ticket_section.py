import pytest
from src.ticket.customer_section.customer_ticket_section import CustomerTicketSection
from src.utils.data_containers.named_tuples import Ticket


@pytest.fixture
def dummy_customer(mocker):
    cust = mocker.Mock()
    cust.c_id = 1
    return cust


@pytest.fixture
def ticket_section(dummy_customer):
    cts = CustomerTicketSection(dummy_customer)
    return cts


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


class TestCustomerTicketSection:
    def test_raise_ticket(self, mocker, ticket_section, mock_ticket_dao):
        mocker.patch('src.ticket.customer_section.customer_ticket_section.input_ticket', lambda: ('1', 'test_title', 'test_description'))
        mock_create_new_ticket = mocker.Mock()
        mock_ticket_dao().create_new_ticket = mock_create_new_ticket
        ticket_section.raise_ticket()
        mock_create_new_ticket.assert_called_once_with(d_id='1', c_id=1, desc='test_description', title='test_title')

    def test_register_feedback(self, ticket_section, mock_feedback_dao, mocker):
        mocker.patch('src.ticket.customer_section.customer_ticket_section.input_feedback_body', lambda: (5, 'sample_desc'))
        mock_add_feedback = mocker.Mock()
        mock_feedback_dao().add_feedback = mock_add_feedback
        ticket_section.register_feedback(111)
        mock_add_feedback.assert_called_once_with(5, 'sample_desc', 111)
