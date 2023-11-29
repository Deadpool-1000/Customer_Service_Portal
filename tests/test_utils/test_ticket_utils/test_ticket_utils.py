import pytest
from src.utils.tickets.ticket_utils import tid_is_valid, input_ticket, tickets_menu
from src.utils.data_containers.named_tuples import Ticket


sample_tickets = [
    Ticket(
        t_id=1,
        d_id=2,
        c_id=3,
        repr_id=2,
        title='test string',
        description='test string',
        status='test string',
        cust_feedback='test string',
        created_on='test_date',
        message='test string'
    ),
    Ticket(
        t_id=2,
        d_id=2,
        c_id=3,
        repr_id=2,
        title='test string',
        description='test string',
        status='test string',
        cust_feedback='test string',
        created_on='test_date',
        message='test string'
    ),
    Ticket(
        t_id=3,
        d_id=2,
        c_id=3,
        repr_id=2,
        title='test string',
        description='test string',
        status='test string',
        cust_feedback='test string',
        created_on='test_date',
        message='test string'
    ),
    Ticket(
        t_id=4,
        d_id=2,
        c_id=3,
        repr_id=2,
        title='test string',
        description='test string',
        status='test string',
        cust_feedback='test string',
        created_on='test_date',
        message='test string'
    )
]


@pytest.mark.usefixtures('my_config_loader')
class TestTicketUtils:
    def test_tid_is_valid_success(self):
        success = tid_is_valid(2, sample_tickets)
        assert success is True

    def test_input_ticket_with_valid_details(self, mocker):
        ticket_details = iter(('1', 'test_title', 'test_desc'))
        mocker.patch('builtins.input', lambda prompt: next(ticket_details))
        dept_id, title, desc = input_ticket()
        assert dept_id == '1' and title == 'test_title' and desc == 'test_desc'

    @pytest.mark.parametrize('details', [('', '1', 'test_title', 'test_desc'), ('1', '  ', 'test_title', 'test_desc'), ('1', 'test_title', '   ', 'test_desc')])
    def test_input_with_empty_details(self, details, mocker):
        ticket_details = iter(details)
        mocker.patch('builtins.input', lambda prompt: next(ticket_details))
        dept_id, title, desc = input_ticket()
        assert dept_id == '1' and title == 'test_title' and desc == 'test_desc'

    @pytest.mark.parametrize('user_choice', [('n', 'n', 'n', 'n')])
    def test_ticket_menu_with_next_page(self, mocker, capsys, user_choice):
        user_choice = iter(user_choice)
        end_of_tickets_message = "---------------------------That's all the tickets we have---------------------------"
        mocker.patch('src.utils.tickets.ticket_utils.simple_input', lambda prompt, allowed: next(user_choice))
        tickets_menu(
            tickets=sample_tickets,
            main_prompt='test_main_prompt',
            functionalities_prompt='test_functionalities_prompt',
            continue_prompt='test_continue_prompt',
        )
        captured = capsys.readouterr()
        assert end_of_tickets_message in captured.out

    @pytest.mark.parametrize('user_choice', [('n', 'q', 'n')])
    def test_ticket_menu_with_quit_options(self, mocker, capsys, user_choice):
        user_choice = iter(user_choice)
        end_of_tickets_message = "---------------------------That's all the tickets we have---------------------------"
        mocker.patch('src.utils.tickets.ticket_utils.simple_input', lambda prompt, allowed: next(user_choice))
        tickets_menu(
            tickets=sample_tickets,
            main_prompt='test_main_prompt',
            functionalities_prompt='test_functionalities_prompt',
            continue_prompt='test_continue_prompt',
        )
        captured = capsys.readouterr()
        assert end_of_tickets_message not in captured.out

    @pytest.mark.parametrize('user_choice', [('a', 'q', 'y', 'q', 'n')])
    def test_ticket_menu_with_functionalities(self, mocker, user_choice):
        user_choice = iter(user_choice)
        mocker.patch('src.utils.tickets.ticket_utils.simple_input', lambda prompt, allowed: next(user_choice))
        mock_func_a = mocker.Mock()
        test_functionalities = {
            'a': mock_func_a
        }
        tickets_menu(
            tickets=sample_tickets,
            main_prompt='test_main_prompt',
            functionalities_prompt='test_functionalities_prompt',
            continue_prompt='test_continue_prompt',
            functionalities= test_functionalities
        )
        mock_func_a.assert_called_once()
