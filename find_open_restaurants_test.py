import pytest

from find_open_restaurants import parse_csv, parse_hours, get_open_and_close_times, days_between
from test_support.output_parse_hours_days import output_parse_hours_days
from test_support.output_parse_hours_two_hours_sections import output_parse_hours_two_hours_sections
from test_support.output_parse_hours_one_day_sections import output_parse_hours_one_day_sections
from test_support.output_parse_hours_extra_day import output_parse_hours_extra_day
from test_support.output_parse_hours_closed_days import output_parse_hours_closed_days

def test_parse_csv():
    output = parse_csv('examples/input1.csv')
    assert output[0]['Restaurant Name'] == 'The Cowfish Sushi Burger Bar'
    assert output[0]['Hours'] == 'Mon-Sun 11:00 am - 10 pm'

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