import math


class HaversineCalculator:
    """This class represents a haversine calculator object."""
    def __init__(self, lat1, lon1, lat2, lon2, decimal_places=2):
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        self.decimal_places = decimal_places

    def calculate(self):
        """Calculate the distance between two points using the haversine formula."""
        dlat = math.radians(self.lat2 - self.lat1)
        dlon = math.radians(self.lon2 - self.lon1)
        a = math.sin(dlat / 2) * math.sin(dlat / 2) + math.cos(math.radians(self.lat1)) * math.cos(math.radians(self.lat2)) * math.sin(dlon / 2) * math.sin(dlon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c
        return round(distance, self.decimal_places)
    
