import re
import csv
import dateparser

day_order = ['Mon', 'Tues', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


def find_open_restaurants(filename, timestamp):
    restaurant_hours = parse_csv(filename)
    return get_open_restaurants_at_timestamp(restaurant_hours, timestamp)

### Parse Dataset ###

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
    return format_timestamp(time)

def format_timestamp(timestamp):
    return int(timestamp.time().strftime('%H%M'))

### Evalutate Open Restaurants ###

def get_open_restaurants_at_timestamp(restaurant_hours, timestamp):
    time = format_timestamp(timestamp)
    weekday = day_order[timestamp.weekday()]

    open_restaurants = []

    for restaurant in restaurant_hours:
        if is_restaurant_open(restaurant['Hours'], weekday, time):
            open_restaurants.append(restaurant['Restaurant Name'])

    return open_restaurants

def is_restaurant_open(restaurant_hours, weekday, time):
    if weekday not in restaurant_hours:
        return False

    hours = restaurant_hours[weekday]

    open_time = hours['open']
    close_time = hours['close']

    if close_time > open_time:
        # Example: 11 am - 5 pm
        return (time >= open_time and time < close_time)

    if time >= open_time:
        # Example: 11 am - 1:30 am, current time = 5pm
        return True

    # Example: 11 am - 1:30 am, current time = 2am, look at previous days close hours
    return check_previous_days_hours(restaurant_hours, weekday, time)

def get_previous_days_hours(restaurant_hours, weekday):
    weekday_index = day_order.index(weekday)
    previous_weekday_index = weekday_index - 1 if weekday_index - 1 > 0 else 6
    return restaurant_hours[day_order[previous_weekday_index]]

def check_previous_days_hours(restaurant_hours, weekday, time):
    previous_days_hours = get_previous_days_hours(restaurant_hours, weekday)
    close_time = previous_days_hours['close']
    open_time = previous_days_hours['open']
    if close_time > open_time:
        # Edge case where previous days hours don't overlap midnight, Example: 11 am - 5 pm
        return False
    return time < close_time
