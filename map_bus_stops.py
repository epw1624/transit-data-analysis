import pandas
import folium

import compass_card_data
import bus_stops

class MapPin:
    def __init__(self, name, lat, long, freq):
        self.name = name
        self.lat = lat
        self.long = long
        self.freq = freq

    def construct_folium_marker(self):
        return folium.Marker(
            location=[self.lat, self.long],
            popup = f"{self.name}\n{self.freq} visits",
            icon = self.construct_folium_icon()
        )

    def construct_folium_icon(self):
        match self.freq:
            case 1:
                color = "red"
            case f if f < 5:
                color = "orange"
            case f if f < 20:
                color = "beige"
            case _:
                color = "green"
            
        return folium.Icon(color=color)


all_stops = bus_stops.BusStops("datasets/translink_dataset/stops.csv").stops

ccd = compass_card_data.CompassCardData("datasets/compass_card_dataset.csv")

my_stops = ccd.get_bus_stops_with_frequencies()

# construct a list of MapPin objects by joining the 2 datasets
joined_dataframe = pandas.merge(my_stops, all_stops, on="stop_code", how="left")

# remove any entries with missing location values
joined_dataframe = joined_dataframe.dropna(subset=["stop_lat", "stop_lon"])

map_pins = []
for index, row in joined_dataframe.iterrows():
    new_map_pin = MapPin(row["stop_name"], row["stop_lat"], row["stop_lon"], row["frequency"])
    map_pins.append(new_map_pin)

# construct Folium map
m = folium.Map(location=[49.2827, -123.1207])

for pin in map_pins:
    marker = pin.construct_folium_marker()
    marker.add_to(m)

m.save("map.html")



