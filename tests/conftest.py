import pytest
from src.utils.load_configurations import load_configurations
from src.utils.data_containers.named_tuples import Ticket


@pytest.fixture(scope='session', autouse=True)
@load_configurations
def my_config_loader():
    pass


@pytest.fixture(scope='session')
def sample_tickets():
    return [
        Ticket(
            t_id='1',
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
            t_id='2',
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
            t_id='3',
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
            t_id='4',
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