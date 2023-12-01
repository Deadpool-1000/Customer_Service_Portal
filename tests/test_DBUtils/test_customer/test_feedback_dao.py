import pytest
from src.DBUtils.customer.feedbackdao import FeedbackDAO
from src.utils.data_containers.named_tuples import Feedback


sample_feedback_data = [
    ('1', 4, 'test_desc1', '1t'),
    ('2', 4, 'test_desc2', '2t'),
    ('3', 4, 'test_desc3', '3t'),
    ('4', 4, 'test_desc4', '4t'),
    ('5', 4, 'test_desc5', '5t'),
    ('6', 4, 'test_desc6', '6t')
]

sample_feedback_data_formatted = [
    Feedback(f_id='1', stars=4, desc='test_desc1', t_id='1t'),
    Feedback(f_id='2', stars=4, desc='test_desc2', t_id='2t'),
    Feedback(f_id='3', stars=4, desc='test_desc3', t_id='3t'),
    Feedback(f_id='4', stars=4, desc='test_desc4', t_id='4t'),
    Feedback(f_id='5', stars=4, desc='test_desc5', t_id='5t'),
    Feedback(f_id='6', stars=4, desc='test_desc6', t_id='6t'),
]


@pytest.fixture
def feedback_dao(mock_sqlite3_conn):
    f = FeedbackDAO(mock_sqlite3_conn)
    return f


class TestFeedbackDAO:
    def test_get_feedback_with_sample_data(self, feedback_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchall.return_value = sample_feedback_data
        ret_feedback = feedback_dao.get_feedback()
        assert ret_feedback == sample_feedback_data_formatted

    def test_get_feedback_with_empty_data(self, feedback_dao, mock_sqlite3_cur):
        mock_sqlite3_cur.execute.return_value.fetchall.return_value = None
        ret_feedback = feedback_dao.get_feedback()
        assert ret_feedback == []
