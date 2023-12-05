import pytest
from src.users.manager.manager import Manager
from src.utils.data_containers.named_tuples import Feedback

sample_feedbacks = [
    Feedback(t_id=1, stars=2, desc='test_desc', f_id=2),
    Feedback(t_id=2, stars=3, desc='test_desc', f_id=3),
    Feedback(t_id=3, stars=4, desc='test_desc', f_id=4),
    Feedback(t_id=4, stars=2, desc='test_desc', f_id=5),
    Feedback(t_id=5, stars=1, desc='test_desc', f_id=6),
]


class TestManager:
    @pytest.fixture(autouse=True)
    def fake_manager(self):
        m = Manager(e_id=2, name='test_manager', phn_num='test_phn_number', address='test_address, test_city', email='test_manager@gmail.com')
        self.manager = m

    @pytest.fixture(autouse=True)
    def mock_db_conn(self, mocker):
        mock_db_conn_cls = mocker.MagicMock()
        mocker.patch('src.users.manager.manager.DatabaseConnection', mock_db_conn_cls)

    @pytest.fixture
    def mock_feedback_cls(self, mocker):
        mock_feedback_cls = mocker.Mock()
        mocker.patch('src.users.manager.manager.FeedbackDAO', mock_feedback_cls)
        return mock_feedback_cls

    @pytest.fixture
    def mock_ticket_section(self, mocker):
        mock_ts_menu = mocker.Mock()
        mocker.patch.object(self.manager.ticket_section, 'menu', mock_ts_menu)
        return mock_ts_menu

    def test_menu_with_ticket_section(self, mocker, mock_ticket_section):
        inps = iter([' ', 't', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        self.manager.menu()
        mock_ticket_section.assert_called_once()

    def test_feedback_handler_with_end_of_feedback(self, mocker, capsys, mock_feedback_cls):
        inps = iter(['f', 'n', 'n', 'n', 'n', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        mock_feedback_cls().get_feedback.return_value = sample_feedbacks
        self.manager.menu()
        captured = capsys.readouterr()
        assert "That's all the feedback we have" in captured.out

    def test_feedback_handler_with_quit(self, mocker, mock_feedback_cls):
        inps = iter(['f', 'n', 'q', 'y', 'q', 'n', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        mock_feedback_cls().get_feedback.return_value = sample_feedbacks
        ret_val = self.manager.menu()
        assert ret_val is None

    def test_feedback_handler_with_empty_feedbacks(self, mocker, capsys, mock_feedback_cls):
        inps = iter(['f', 'q'])
        mocker.patch('builtins.input', lambda prompt: next(inps))
        mock_feedback_cls().get_feedback.return_value = []
        self.manager.menu()
        captured = capsys.readouterr()
        assert "No Feedbacks to show." in captured.out
