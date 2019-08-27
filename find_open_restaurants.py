import csv

def find_open_restuarants():
    print('Hello World')

def parse_csv():
    input_data = []

    with open('examples/input1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            input_data.append(row)

    return input_data

find_open_restuarants()
