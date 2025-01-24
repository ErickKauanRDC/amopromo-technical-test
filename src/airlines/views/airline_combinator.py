
from datetime import datetime

from django.http import JsonResponse
from requests import Response
from airports.models.airport import Airport
from common.api_client import ApiClient
from common.haversine_calculator import HaversineCalculator
from rest_framework.views import APIView
from setup import settings

class Flight:
    """This class represents a flight object. It contains the following attributes:
    {
			"departure_time": "2022-06-12T12:35:00",
			"arrival_time": "2022-06-12T15:40:00",
			"price": {
				"fare": 1738.55,
				"fees": 0.0,
				"total": 0.0
			},
			"aircraft": {
				"model": "A 320",
				"manufacturer": "Airbus"
			},
			"meta": {
				"range": 0,
				"cruise_speed_kmh": 0,
				"cost_per_km": 0.0
			}
	},
    """
    def __init__(self, departure_time, arrival_time, price, aircraft, meta):
        """Initialize the flight object with the given attributes."""
        self.departure_time = datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S")
        self.arrival_time = datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S")
        self.price = price
        self.aircraft = aircraft
        self.meta = meta

    def __dict__(self):
        """Return a dictionary representation of the flight object."""
        return {
            "departure_time": self.departure_time,
            "arrival_time": self.arrival_time,
            "price": self.price,
            "aircraft": self.aircraft,
            "meta": self.meta
        }

    

class Airline:
    """This class represents an airline object. It contains the following attributes:
    summary": {
		"departure_date": "2022-06-12",
		"from": {
			"iata": "PLU",
			"city": "Belo Horizonte",
			"lat": -19.75,
			"lon": -43.75,
			"state": "MG"
		},
		"to": {
			"iata": "MAO",
			"city": "Manaus",
			"lat": -3.031327,
			"lon": -60.046093,
			"state": "AM"
		},
		"currency": "BRL",
        "options" = [Flight, Flight, Flight...] 
	},
    """

    def __init__(self, summary, options, minimal_fee_value = 40, fee_percent = 0.1):
        """Initialize the airline object with the given attributes."""
        self.fee_percent = fee_percent
        self.minimal_fee_value = minimal_fee_value
        self.summary = summary
        self.linear_distance = self._calculate_linear_distance()
        self.options = [Flight(**option) for option in options]
        self.update_options()

    def _calculate_linear_distance(self):
        """Calculate the linear distance between the departure and arrival airports."""
        from_lat = self.summary['from']['lat']
        from_lon = self.summary['from']['lon']
        to_lat = self.summary['to']['lat']
        to_lon = self.summary['to']['lon']
        return HaversineCalculator(from_lat, from_lon, to_lat, to_lon,2).calculate()

    def _calculate_flight_price(self, flight : Flight):
        """Calculate the total price of the flight."""
        fees = round(max((flight.price['fare'] * self.fee_percent), self.minimal_fee_value), 2)
        
        return {
            **flight.price,
            'fees' : fees,
            'total': round((flight.price['fare'] + fees), 2)
        }
    
    def _calculate_cruise_speed_kmh(self, flight : Flight):
        """Calculate the cruise speed in km/h."""
        travel_time = (flight.arrival_time - flight.departure_time).total_seconds() / 3600
        return round(self.linear_distance / travel_time,2)

    def _calculate_flight_cost_per_km(self, flight : Flight):
        """Calculate the cost per km of the flight."""
        return round(self._calculate_flight_price(flight)['total'] / self.linear_distance, 2)

    def _calculate_flight_meta(self, flight : Flight):
        return {
            'range': self.linear_distance,
            'cruise_speed_kmh': self._calculate_cruise_speed_kmh(flight),
            'cost_per_km': self._calculate_flight_cost_per_km(flight)
        }
    
    def _update_flight(self, flight : Flight):
        """Update the flight object with the calculated price and meta data."""
        flight.price = self._calculate_flight_price(flight)
        flight.meta = self._calculate_flight_meta(flight)
        return flight
    
    def update_options(self):
        """Update the options list with the calculated price and meta data."""
        self.options = [self._update_flight(flight) for flight in self.options]

    def __dict__(self):
        """Return a dictionary representation of the airline object."""
        return {
            "summary": self.summary,
            "options": [option.__dict__() for option in self.options]
        }

class RoundTrip:
    """This class represents a combination of two flights, a departure and a return flight."""
    def __init__(self, departure_flight, return_flight):
        """Initialize the round trip object with the given departure and return flights."""
        self.departure_flight = departure_flight
        self.return_flight = return_flight
        self.total_price = self._calculate_total_price()

    def _calculate_total_price(self):
        """Calculate the total price of the round trip."""
        total_fare = self.departure_flight.price['fare'] + self.return_flight.price['fare']
        total_fees = self.departure_flight.price['fees'] + self.return_flight.price['fees']
        total_price = total_fare + total_fees
        self.total_price = total_price
        return {
            "fare": total_fare,
            "fees": total_fees,
            "total": total_price
        }

    def __dict__(self):
        """Return a dictionary representation of the round trip object."""
        return {
            "departure_flight": self.departure_flight.__dict__(),
            "return_flight": self.return_flight.__dict__(),
            "total_price": self.total_price,
        }
  

class AirlineManager:
    """This class is responsible for managing airline data."""
    def __init__(self, api_client):
        self.api_client = api_client

    def _get_airline(self, from_iata, to_iata, date):
        """Get airline data for a given route and date."""
        try:
            airline_data = self.api_client.get(f'air/search', f'{from_iata}/{to_iata}/{date}')
            return Airline(airline_data['summary'], airline_data['options'])
        except Exception as e:
            raise ValueError(f"Error getting airline data: {e}")
        
    def get_airlines(self, from_iata, to_iata, departure_date, return_date):
        departure_airline = self._get_airline(from_iata, to_iata, departure_date)
        return_airline = self._get_airline(to_iata, from_iata, return_date)

        if departure_airline and return_airline:
            return [departure_airline, return_airline]
        
        return None
    
    def _sort_round_trips(self, round_trips):
        """Sort the round trips by total price."""
        return sorted(round_trips, key=lambda round_trip: round_trip.total_price['total'])

    def _get_round_trips(self, from_iata, to_iata, departure_date, return_date):
        """Get all possible round trips for a given route and dates."""
        airlines = self.get_airlines(from_iata, to_iata, departure_date, return_date)
        
        if not airlines:
            return None
        
        round_trips = []

        for departure_airline in airlines[0].options:
            for return_airline in airlines[1].options:
                round_trips.append(RoundTrip(departure_airline, return_airline))
        
        round_trips = self._sort_round_trips(round_trips)

        return round_trips
    
    def get_airlines_combinations(self, from_iata, to_iata, departure_date, return_date):
        """Get all possible round trips for a given route and dates."""
        if datetime.strptime(departure_date, "%Y-%m-%d") > datetime.strptime(return_date, "%Y-%m-%d"):
            raise ValueError("The departure date must be before the return date.")

        airports = Airport.objects.filter(iata__in=[from_iata, to_iata])
        
        if len(airports) != 2:
            raise ValueError("Invalid airport IATA codes.")

        round_trips = self._get_round_trips(from_iata, to_iata, departure_date, return_date)

        return {
            "summary": {
                "from": from_iata,
                "to": to_iata,
                "departure_date": departure_date,
                "return_date": return_date
            },
            "round_trips": [round_trip.__dict__() for round_trip in round_trips]
        }
    
class AirlineCombinatorView(APIView):
    """This class is responsible for handling the airline combinator API requests."""
    def get(self, request):
        try:
            from_iata = request.query_params.get('from')
            to_iata = request.query_params.get('to')
            departure_date = request.query_params.get('departure_date')
            return_date = request.query_params.get('return_date')
            
            api_client = ApiClient(
                base_url=settings.STUB_AMOPROMO_BASE_URL,
                username=settings.STUB_AMOPROMO_USERNAME,
                password=settings.STUB_AMOPROMO_PASSWORD,
                api_key=settings.STUP_AMOPROMO_API_KEY
            )

            if not api_client:
                return JsonResponse({
                    "message": "Error setting up the API client.",
                    "success": False,
                }, status=500)
            airline_manager = AirlineManager(api_client)
            airlines_combinations = airline_manager.get_airlines_combinations(from_iata, to_iata, departure_date, return_date)

            return JsonResponse(airlines_combinations)
        except Exception as e:
            return JsonResponse({
                "message": f"An error occurred: {e}",
                "success": False,
            }, status=500)
    


    


        
        
    
        
        
        
        
        
    
    
    
    
    




