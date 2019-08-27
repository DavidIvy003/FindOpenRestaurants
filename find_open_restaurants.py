import csv
import dateparser

day_order = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

def parse_hours(string):
    open_times = {}
    sections = string.split(' / ')
    for section in sections:
      affected_days = get_affected_days_and_open_times(section)
      for key, value in affected_days.items():
          open_times[key] = value
    return open_times

def get_affected_days_and_open_times(string):
    open_times = {}
    first_day = string[:3]
    if string[3:4] == '-':
        second_day = string[4:7]
        time = string[8:]
        days = days_between(first_day, second_day)
        open_and_close_times = parse_times(time)
        for day in days:
            open_times[day] = open_and_close_times
    else:
        time = string[4:]
    return open_times

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
