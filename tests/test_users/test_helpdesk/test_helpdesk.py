import pytest
from src.users.helpdesk.helpdesk import Helpdesk


class TestHelpdesk:
    @pytest.fixture(autouse=True)
    def fake_helpdesk(self):
        h = Helpdesk(e_id=1, name='test_name', phn_num='test_phn_num', address='test_address', email='test_email@gmail.com', dept_id=2)
        self.helpdesk = h

    @pytest.fixture
    def mock_ticket_section(self, mocker):
        mock_ts = mocker.Mock()
        mocker.patch.object(self.helpdesk.ticket_section, 'menu', mock_ts)
        return mock_ts

    def test_menu_with_message_box(self, mocker):
        inps = iter([' ', 'm', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        with pytest.raises(NotImplementedError):
            self.helpdesk.menu()

    def test_menu_with_ticket_section(self, mocker, mock_ticket_section):
        inps = iter([' ', 't', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.helpdesk.menu()
        mock_ticket_section.assert_called_once()
