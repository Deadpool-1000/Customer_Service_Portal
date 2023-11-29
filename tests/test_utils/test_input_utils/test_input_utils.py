import pytest
from src.utils.inputs.input_utils import input_email_password, menu, input_customer_details, simple_input, input_feedback_body, input_message_from_helpdesk


@pytest.mark.usefixtures('my_config_loader')
class TestInputUtils:
    def test_input_email_and_password_with_valid_input(self, mocker):
        email_and_password = ('abc@gmail.com', 'Abcdef@2 ')
        mocker.patch('builtins.input', lambda prompt: email_and_password[0])
        mocker.patch('src.utils.inputs.input_utils.advpass', lambda prompt: email_and_password[1])

        email, password = input_email_password()
        assert email == 'abc@gmail.com' and password == 'Abcdef@2'

    @pytest.mark.parametrize(('email', 'password'), [(('aa', ' ', 'abc@gmail.com'), ('Abcdef@2', )), (('abcd@gmail.com',), ('', 'Abcdef@2'))])
    def test_input_email_and_password_with_invalid_input(self, mocker, email, password):
        iter_email = iter(email)
        iter_password = iter(password)
        mocker.patch('builtins.input', lambda prompt: next(iter_email))
        mocker.patch('src.utils.inputs.input_utils.advpass', lambda prompt: next(iter_password))

        ret_email, ret_password = input_email_password()
        assert ret_email == email[-1] and ret_password == password[-1]

    @pytest.mark.parametrize('inp', [['a', 'b'], ['b', 'a']])
    def test_menu_with_valid_options(self, mocker, inp):
        my_inputs = iter(inp)
        expected_val = iter(inp)
        mocker.patch('builtins.input', lambda _: next(my_inputs))
        m = menu('', ['a', 'b'])
        ret_val1 = next(m)
        ret_val2 = next(m)
        assert ret_val1 == next(expected_val) and ret_val2 == next(expected_val)

    @pytest.mark.parametrize('inp', [['', 'p', 'q'], ['p', 'p', 'q']])
    def test_menu_with_quit_option(self, mocker, inp):
        my_inputs = iter(inp)
        mocker.patch('builtins.input', lambda _: next(my_inputs))
        with pytest.raises(StopIteration):
            m = menu('', ['q', 'a', 'b', 'c'])
            next(m)

    @pytest.mark.parametrize(('cust_details', 'password', 'expected'), [(('', 'a', 'test@gmail.com', '', 'test_fullname', '', 'test_phn_num', '9898989898', '', 'test_address, test_city'), ('', 'abc', 'Abcdef@2'), ('test@gmail.com', 'test_fullname', '9898989898', 'test_address, test_city', 'Abcdef@2'))])
    def test_input_customer_details(self, mocker, cust_details, password, expected):
        iter_password = iter(password)
        iter_inps = iter(cust_details)
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))
        mocker.patch('src.utils.inputs.input_utils.advpass', lambda prompt: next(iter_password))

        ret_details = input_customer_details()
        assert expected == ret_details

    @pytest.mark.parametrize('inps', [('', 'b'), ('c',)])
    def test_simple_input(self, mocker, inps):
        iter_inps = iter(inps)
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))
        user_choice = simple_input('test_prompt', allowed=['a', 'b', 'c'])

        assert user_choice == inps[-1]

    @pytest.mark.parametrize(('stars', 'feedback'), [(('', 'a', '5'), ('', 'test_feedback')), (('@', '6'),('', 'test_feedback'))])
    def test_input_feedback_body(self, mocker, stars, feedback):
        iter_inps = iter([*stars, *feedback])
        mocker.patch('builtins.input', lambda prompt: next(iter_inps))
        ret_stars, ret_feedback = input_feedback_body()

        assert ret_stars == int(stars[-1]) and ret_feedback == feedback[-1]

    @pytest.mark.parametrize(('message',), [(('', 'test_message'),)])
    def test_input_message_from_helpdesk(self, mocker, message):
        iter_message = iter(message)
        mocker.patch('builtins.input', lambda prompt: next(iter_message))

        ret_message = input_message_from_helpdesk()
        assert ret_message == message[-1]