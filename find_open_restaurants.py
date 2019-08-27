import csv

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
