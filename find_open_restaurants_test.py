import pytest
from datetime import datetime

from find_open_restaurants import find_open_restaurants, parse_csv, parse_hours, get_open_and_close_times, days_between, is_restaurant_open, get_open_restaurants_at_timestamp
from test_support.output_parse_hours_days import output_parse_hours_days
from test_support.output_parse_hours_two_hours_sections import output_parse_hours_two_hours_sections
from test_support.output_parse_hours_one_day_sections import output_parse_hours_one_day_sections
from test_support.output_parse_hours_extra_day import output_parse_hours_extra_day
from test_support.output_parse_hours_closed_days import output_parse_hours_closed_days
from test_support.output_parse_hours_extra_day_first import output_parse_hours_extra_day_first
from test_support.restaurants_open_close_hours import restaurants_open_close_hours

all_restaurants = list( restaurant['Restaurant Name'] for restaurant in restaurants_open_close_hours )


def test_find_open_restaurants():
    output = find_open_restaurants('examples/input1.csv', datetime(2019, 8, 27, 12, 30))
    assert len(output) == 36

def test_parse_csv():
    output = parse_csv('examples/input1.csv')
    assert output == restaurants_open_close_hours

class TestGetOpenRestaurantsAtTimestamp:
    def test_tuesday_afternoon(self):
        output = get_open_restaurants_at_timestamp(restaurants_open_close_hours, datetime(2019, 8, 27, 12, 30)) # Tuesday 12:30pm
        assert len(output) == 36

    def test_sunday_evening(self):
        output = get_open_restaurants_at_timestamp(restaurants_open_close_hours, datetime(2019, 9, 1, 17, 30)) # Sunday 5:30pm
        assert len(set(all_restaurants) - set(output) - set(['Char Grill', 'Top of the Hill', 'Jose and Sons'])) == 0

    def test_wednesday_early_am(self):
        output = get_open_restaurants_at_timestamp(restaurants_open_close_hours, datetime(2019, 8, 28, 3, 30)) # Wedneday 3:30am
        assert output == ['Seoul 116']

    def test_friday_early_am(self):
        output = get_open_restaurants_at_timestamp(restaurants_open_close_hours, datetime(2019, 8, 30, 1, 0)) # Friday 1:00am
        assert output == ['Bonchon', 'Seoul 116']

    def test_saturday_early_am(self):
        output = get_open_restaurants_at_timestamp(restaurants_open_close_hours, datetime(2019, 8, 31, 0, 0)) # Saturday 12:00am
        assert output == ['The Cheesecake Factory', 'Bonchon', 'Seoul 116']

class TestParseHours:
    def test_parse_hours_across_multiple_days(self):
        output = parse_hours('Mon-Sun 11:00 am - 10 pm')
        assert output == output_parse_hours_days

    def test_parse_hours_two_hours_sections(self):
        output = parse_hours('Mon-Thu 11:30 am - 10 pm  / Fri-Sun 11:30 am - 11 pm')
        assert output == output_parse_hours_two_hours_sections

    def test_parse_hours_one_day_sections(self):
        output = parse_hours('Mon-Wed 5 pm - 12:30 am  / Thu-Fri 5 pm - 1:30 am  / Sat 3 pm - 1:30 am  / Sun 3 pm - 11:30 pm')
        assert output == output_parse_hours_one_day_sections

    def test_parse_hours_extra_day(self):
        output = parse_hours('Tues-Fri, Sun 11:30 am - 10 pm  / Sat 5:30 pm - 11 pm / Mon 5:30 pm - 11 pm')
        assert output == output_parse_hours_extra_day

    def test_parse_hours_closed_days(self):
        output = parse_hours('Mon-Sat 11 am - 11 pm')
        assert output == output_parse_hours_closed_days

    def test_parse_hours_extra_day_first(self):
        output = parse_hours('Mon, Wed-Sun 11 am - 10 pm')
        assert output == output_parse_hours_extra_day_first

class TestDaysBetween:
    def test_days_between_mon_and_fri(self):
        output = days_between('Mon', 'Fri')
        assert output == ['Mon', 'Tues', 'Wed', 'Thu', 'Fri']

    def test_days_between_fri_and_mon(self):
        output = days_between('Fri', 'Mon')
        assert output == ['Mon', 'Fri', 'Sat', 'Sun']

class TestOpenAndCloseTimes:
    def test_parse_times(self):
        output = get_open_and_close_times('Tues-Fri 11:00 am - 10 pm')
        assert output == {
            'open': 1100,
            'close': 2200,
        }

class TestIsRestaurantOpen:
    def test_before_midnight(self):
        assert is_restaurant_open(output_parse_hours_days, 'Mon', 1100) == True
        assert is_restaurant_open(output_parse_hours_days, 'Mon', 1000) == False
        assert is_restaurant_open(output_parse_hours_days, 'Mon', 2100) == True
        assert is_restaurant_open(output_parse_hours_days, 'Mon', 2200) == False

    def test_after_midnight(self):
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 100) == True
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 200) == False
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 0) == True
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 1600) == False
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 1700) == True
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Fri', 2300) == True

        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Thu', 100) == False
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Thu', 0) == True
        assert is_restaurant_open(output_parse_hours_one_day_sections, 'Thu', 30) == False

    def test_close_days(self):
        assert is_restaurant_open(output_parse_hours_closed_days, 'Sun', 1200) == False
