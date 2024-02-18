import pandas

class BusStops:
    def __init__(self, filepath):
        self.stops = pandas.read_csv(filepath)