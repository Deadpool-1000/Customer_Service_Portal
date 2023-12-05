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
            status='open',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='2',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='open',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='3',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='open',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='4',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='open',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        )
    ]


@pytest.fixture(scope='session')
def closed_tickets():
    return [
        Ticket(
            t_id='1',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='closed',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='2',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='closed',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='3',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='closed',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='4',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='closed',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        )
    ]


@pytest.fixture(scope='session')
def raised_tickets():
    return [
        Ticket(
            t_id='1',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='2',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='3',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='4',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        )
    ]


@pytest.fixture(scope='session')
def in_prog_tickets():
    return [
        Ticket(
            t_id='1',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='2',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='3',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        ),
        Ticket(
            t_id='4',
            d_id=2,
            c_id=3,
            repr_id=2,
            title='test string',
            description='test string',
            status='raised',
            cust_feedback='test string',
            created_on='2023-11-03 15:35:16.375121',
            message='test string'
        )
    ]
