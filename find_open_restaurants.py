import re
import csv
import dateparser

day_order = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def find_open_restaurants(filename, datetime):
    restaurant_hours = parse_csv(filename)

def parse_csv(filename):
    input_data = []

    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_data.append({
              'Restaurant Name': row['Restaurant Name'],
              'Hours': parse_hours(row['Hours'])
            })

    return input_data

def parse_hours(string):
    open_times = {}
    sections = string.split(' / ')
    for section in sections:
        affected_days = get_affected_days(section)
        time = get_open_and_close_times(section)

        for day in affected_days:
            open_times[day] = time

    return open_times

def get_affected_days(string):
    match = re.search(r'^(\D)*', string)
    sections = match.group().split(',')

    days = []

    for section in sections:
        split_string = re.split(r'\W+', section.strip())
        first_day = split_string[0]

        if len(split_string) > 1:
            second_day = split_string[1]
            days += days_between(first_day, second_day)
        else:
            days.append(first_day)

    return days

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

def get_open_and_close_times(string):
    hours = get_time_from_hours_string(string)
    open_hour = get_time(hours.split('-')[0])
    close_hour = get_time(hours.split('-')[1])
    return {
        'open': open_hour,
        'close': close_hour,
    }

def get_time(string):
    time = dateparser.parse(string)
    return int(time.time().strftime('%H%M'))
