import pandas

class BusStops:
    COLS_TO_DROP = ["stop_url", "parent_station", "wheelchair_boarding", "stop_desc"]
    def __init__(self, filepath):
        self.stops = pandas.read_csv(filepath)
        self.stops["stop_id"] = self.stops["stop_id"].astype(int)
        self.stops["location_type"] = self.stops["location_type"].astype(int)
        self.stops.drop(columns=self.COLS_TO_DROP, inplace=True)