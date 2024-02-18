from enum import Enum
import pandas

class CardActions(Enum):
    TAP_IN = 1
    TAP_OUT = 2
    TRANSFER = 3
    LOADED = 4
    REFUND = 5

class CompassCardData:
    # dropping columns occurs after parsing the Transaction column, so it can also be dropped
    COLS_TO_DROP = ["Transaction", "LineItem", "LocationDisplay", "OrderDate", "Payment", "OrderNumber", "AuthCode", "Total"]

    def __init__(self, filepath):
        self.data = pandas.read_csv(filepath)
        self.extract_transaction()
        self.data.drop(columns=self.COLS_TO_DROP, inplace=True)

    def extract_transaction(self):
        transactions = list(self.data["Transaction"])

        # for reasons unknown, I couldn't get this to work with only one map
        actions = list(map(lambda t: t.split(" at ")[0], transactions))
        locations = list(map(lambda t: t.split(" at ")[1], transactions))

        self.data["Action"] = actions
        self.data["Location"] = locations

    def get_bus_trips(self):
        bus_trips = self.data[self.data["Location"].str.split(" ").str[0] == "Bus"]
        stops = list(map(lambda l: l.split(" ")[-1], list(bus_trips["Location"])))
        bus_trips["Stop"] = stops
        bus_trips["Stop"] = bus_trips["Stop"].astype(float)
        return bus_trips
    
    def get_bus_stops_with_frequencies(self):
        bus_trips = self.get_bus_trips()
        stops = {}
        for stop in list(bus_trips["Stop"]):
            if int(stop) not in stops:
                stops[int(stop)] = 1
            else:
                stops[int(stop)] += 1

        # convert to pandas dataframe
        stop_ids = []
        frequencies = []
        for key in stops:
            stop_ids.append(key)
            frequencies.append(stops[key])
        df = pandas.DataFrame({"stop_code": stop_ids, "frequency": frequencies})

        return df

    