import re
import csv
import dateparser

day_order = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def parse_hours(string):
    open_times = {}
    sections = string.split(' / ')
    for section in sections:
      affected_days = get_affected_days(section)
      time = parse_times(get_time_from_hours_string(section))

      for day in affected_days:
          open_times[day] = time

    return open_times

def get_affected_days(string):
    split_string = re.split(r'\W+', string)
    first_day = split_string[0]

    if split_string[1] in day_order:
        second_day = split_string[1]
        days = days_between(first_day, second_day)

        if split_string[2] in day_order:
            days.append(split_string[2])

        return days
    else:
        return [first_day]

def get_time_from_hours_string(string):
    match = re.search(r'([0-9]+).*$', string)
    return match.group()

def days_between(first_day, second_day):
    first_day_index = day_order.index(first_day)
    second_day_index = day_order.index(second_day)
    if first_day_index < second_day_index:
        return day_order[first_day_index:second_day_index + 1]
    else:
        return day_order[:second_day_index + 1] + day_order[first_day_index:]

def parse_times(hours):
    open_hour = get_time(hours.split('-')[0])
    close_hour = get_time(hours.split('-')[1])
    return {
        'open': open_hour,
        'close': close_hour,
    }

def get_time(string):
    time = dateparser.parse(string)
    return int(time.time().strftime('%H%M'))

def find_open_restuarants():
    parse_csv('examples/input1.csv')
    print('Hello World')

def parse_csv(filename):
    input_data = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_data.append(row)

    return input_data

find_open_restuarants()
