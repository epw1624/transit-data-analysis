import pandas
import random
import datetime
import numpy

import bus_stops

NUM_TRIPS = 500
START_DATE = datetime.datetime(2023, 1, 31)
END_DATE = datetime.datetime(2024, 1, 31)
STD_DEV = 5

# https://paperbun.org/generate-a-random-date-between-two-dates-python/
def random_datetime(start_date, end_date):
    return start_date + datetime.timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

# only interested in generating bus trips, so all transactions have the form "Tap in at Bus Stop xxxxx"
def random_bus_transactions(bus_stop_codes, num_transactions):
    """
    returns a list of num_transactions bus transactions
    stop codes are selected using a normal distribution from bus_stop_codes
    """
    mean = len(bus_stop_codes) // 2
    probabilities = numpy.exp(-(numpy.arange(len(bus_stop_codes)) - mean)**2 / (2 * STD_DEV**2))
    probabilities /= probabilities.sum()
    stop_codes = random.choices(bus_stop_codes, weights=probabilities, k=num_transactions)
    return list(map(lambda code: f"Tap in at Bus Stop {code}", stop_codes))

all_stops = bus_stops.BusStops("datasets/translink_dataset/stops.csv").stops

# constrain the list of stops to zone 1, but the TransLink data doesn't include zones for bus stops, so use coordinates instead
# Eastern boundary: Boundary Road 123.02358 degrees W
# Northern boundary: Stanley Park totem pole: 49.29989 degrees N
# Southern boundary: Vancouver International Airport 49.19521 degrees N
z1_stops = all_stops[all_stops["stop_lon"] < -123.02358]
z1_stops = z1_stops[z1_stops["stop_lat"] < 49.29989 ]
z1_stops = z1_stops[z1_stops["stop_lat"] > 49.19521]

# generate data for each column

date_times = [random_datetime(START_DATE, END_DATE) for _ in range(NUM_TRIPS)]

z1_stop_codes = list(map(lambda code: int(code), list(z1_stops["stop_code"])))

# create reduced version of all_stop_codes list for more realistic transit habits
filtered_stop_codes = random.sample(z1_stop_codes, 30)
transactions = random_bus_transactions(filtered_stop_codes, NUM_TRIPS)

products = ["3 Zone UPass (N)" for _ in range(NUM_TRIPS)]

line_items = ["" for _ in range(NUM_TRIPS)]

amounts = ["$0.00" for _ in range(NUM_TRIPS)]

balances = ["$0.00" for _ in range(NUM_TRIPS)]

journey_ids = list(map(lambda dt: dt.astimezone(datetime.timezone.utc), date_times))

location_displays = [transaction + " " + product for transaction, product in zip(transactions, products)]

transaction_times = list(map(lambda datetime: datetime.time(), date_times))

order_dates = ["" for _ in range(NUM_TRIPS)]

payments = ["" for _ in range(NUM_TRIPS)]

order_numbers = ["" for _ in range(NUM_TRIPS)]

auth_codes = ["" for _ in range(NUM_TRIPS)]

totals = ["" for _ in range(NUM_TRIPS)]

# create a dataframe
df = pandas.DataFrame({
    "DateTime": date_times, 
    "Transaction": transactions, 
    "Product": products, 
    "LineItem": line_items, 
    "Amount": amounts,
    "BalanceDetails": balances,
    "JourneyId": journey_ids,
    "LocationDisplay": location_displays,
    "TransactionTime": transaction_times,
    "OrderDate": order_dates,
    "Payment": payments,
    "OrderNumber": order_numbers,
    "AuthCode": auth_codes,
    "Total": totals
    })

# write to csv
df.to_csv("datasets/sample_compass_card_data.csv")
