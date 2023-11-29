import pytest
from src.utils.load_configurations import load_configurations


@pytest.fixture(scope='session')
@load_configurations
def my_config_loader():
    pass
