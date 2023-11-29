import pytest
from datetime import datetime
from src.utils.utils import view_list_generator, format_date


sample_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


class TestUtils:
    def test_view_list_generator(self, my_config_loader):
        g = view_list_generator(sample_list)
        assert next(g) == sample_list[:2]

    def test_view_list_generator_next_page(self, my_config_loader):
        g = view_list_generator(sample_list)
        first_two = next(g)
        next_two = next(g)
        assert next_two == sample_list[2:4]

    @pytest.mark.parametrize("bad_dates", ['abc', '2023-10-15', 'lo', '  ', '2023-10-87 22:15:33.77777'])
    def test_format_date_with_bad_date(self, bad_dates, my_config_loader):
        with pytest.raises(ValueError):
            format_date(bad_dates)

    @pytest.mark.parametrize('inp_date, expected', [('2023-10-25 11:37:54.637963', "25/10/2023 at 11:37")])
    def test_format_date_with_good_date(self, inp_date, expected, my_config_loader):
        date: datetime = format_date(inp_date)
        assert date == expected
