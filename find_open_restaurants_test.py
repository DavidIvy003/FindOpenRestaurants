import pytest

from find_open_restaurants import parse_csv, parse_hours, parse_times, days_between
from test_support.output_parse_hours_days import output_parse_hours_days

def test_parse_csv():
    output = parse_csv('examples/input1.csv')
    assert output[0]['Restaurant Name'] == 'The Cowfish Sushi Burger Bar'
    assert output[0]['Hours'] == 'Mon-Sun 11:00 am - 10 pm'

def test_parse_hours_days():
    output = parse_hours('Mon-Sun 11:00 am - 10 pm')
    assert output == output_parse_hours_days

class TestDaysBetween:
  def test_days_between_mon_and_fri(self):
      output = days_between('Mon', 'Fri')
      assert output == ['Mon', 'Tue', 'Wed', 'Thu', 'Fri']

  def test_days_between_fri_and_mon(self):
      output = days_between('Fri', 'Mon')
      assert output == ['Mon', 'Fri', 'Sat', 'Sun']

class TestParseTimes:
  def test_parse_times(self):
      output = parse_times('11:00 am - 10 pm')
      assert output == {
          'open': 1100,
          'close': 2200,
      }