# Find Open Restaurants

Find a list of open restaurants from a CSV of restaurant hours and a datetime. See full prompt [here](https://gist.github.com/sharpmoose/d25487b913a08f6a6e6059c07035a041).

## Getting Started

### Prerequisites

Python3

### Installing

```bash
pip install -r requirements.txt
```

## Running the tests

```bash
pytest
```

## Uses

```python
from find_open_restaurants import find_open_restaurants

find_open_restaurants(csv_filepath, datetime_object)
```

### Example

What's open now:

```python
from datetime import datetime
from find_open_restaurants import find_open_restaurants

find_open_restaurants('examples/input1.csv', datetime.now())
```

## Run Tests In Docker

```bash
docker-compose up --build
```