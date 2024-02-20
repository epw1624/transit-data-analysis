import pandas
import datetime
import matplotlib.pyplot as plt

import compass_card_data

ccd = compass_card_data.CompassCardData("datasets/compass_card_data.csv")
bus_trips = ccd.get_bus_trips()

# construct list of all times from the datetimes
trip_times = [pandas.to_datetime(row["TransactionTime"], format="%I:%M %p").time() for index, row in bus_trips.iterrows()]
trip_times_as_float = list(map(lambda x: x.hour * 60 + x.minute, trip_times))

graph = plt.hist(trip_times_as_float, bins=24)
plt.xticks([hour * 60 for hour in range(24)], [f"{hour:02d}:00" for hour in range(24)])
plt.show()