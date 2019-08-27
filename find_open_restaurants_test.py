from find_open_restaurants import parse_csv

def test_parse_csv():
    output = parse_csv('examples/input1.csv')
    assert output[0]['Restaurant Name'] == 'The Cowfish Sushi Burger Bar'
    assert output[0]['Hours'] == 'Mon-Sun 11:00 am - 10 pm'