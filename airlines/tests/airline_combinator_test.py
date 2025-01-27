from django.test import TestCase

from airlines.views.airline_combinator_view import Airline, AirlineManager, Flight, RoundTrip
from common.api_client import ApiClient
from setup import settings

MOCK_DATA = {
	"summary": {
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
		"currency": "BRL"
	},
	"options": [
		{
			"departure_time": "2022-06-12T20:40:00",
			"arrival_time": "2022-06-12T23:45:00",
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
		{
			"departure_time": "2022-06-12T00:05:00",
			"arrival_time": "2022-06-12T02:55:00",
			"price": {
				"fare": 2046.59,
                "fees": 0,
                "total": 0
			},
			"aircraft": {
				"model": "777-200",
				"manufacturer": "Boeing"
			},
			"meta": {
				"range": 0,
				"cruise_speed_kmh": 0,
				"cost_per_km": 0.0
			}
		},
    ]
}

class TestAirlineCalculation(TestCase):
    """This class test the Airline calculations"""

    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.airline : Airline = Airline(MOCK_DATA['summary'], MOCK_DATA['options']) 

    def test_airline_linear_distance_calculator(self):
        expected_value = 2566.2
        self.assertEqual(self.airline._calculate_linear_distance(), expected_value)
       
    def test_flight_price_and_meta_assertion(self):
        """Using the default values of 10% of fee and R$ 40,00 to minimal fee"""
        flight1_data = MOCK_DATA["options"][0]
        flight2_data = MOCK_DATA["options"][1]

        flight1 = Flight(
            departure_time=flight1_data["departure_time"],
            arrival_time=flight1_data["arrival_time"],
            aircraft = {
				"model": "A 320",
				"manufacturer": "Airbus"
			},
            price={
                "fare": 1738.55,
                "fees": 173.86,
                "total": 1912.41
            },
            meta = {
                "range": 2566.2,
                "cruise_speed_kmh": 832.28,
                "cost_per_km": 0.75
            }
        )

        flight2 = Flight(
            departure_time=flight2_data["departure_time"],
            arrival_time=flight2_data["arrival_time"],
            aircraft =  {
                "model": "777-200",
                "manufacturer": "Boeing"
            },
            price={
               "fare": 2046.59,
                "fees": 204.66,
                "total": 2251.25
            },
            meta = {
                "range": 2566.2,
                "cruise_speed_kmh": 905.72,
                "cost_per_km": 0.88
            }
        )
        
        self.assertDictEqual(flight1.__dict__(), self.airline.options[0].__dict__())
        self.assertDictEqual(flight2.__dict__(), self.airline.options[1].__dict__())

    

class TestRoundTripCalculation(TestCase):
    def test_round_trip_total_price(self):
        flight1_data = MOCK_DATA["options"][0]
        flight2_data = MOCK_DATA["options"][1]

        flight1 = Flight(
            departure_time=flight1_data["departure_time"],
            arrival_time=flight1_data["arrival_time"],
            aircraft = {
				"model": "A 320",
				"manufacturer": "Airbus"
			},
            price={
                "fare": 1738.55,
                "fees": 173.86,
                "total": 1912.41
            },
            meta = {
                "range": 2566.2,
                "cruise_speed_kmh": 832.28,
                "cost_per_km": 0.75
            }
        )

        flight2 = Flight(
            departure_time=flight2_data["departure_time"],
            arrival_time=flight2_data["arrival_time"],
            aircraft =  {
                "model": "777-200",
                "manufacturer": "Boeing"
            },
            price={
               "fare": 2046.59,
                "fees": 204.66,
                "total": 2251.25
            },
            meta = {
                "range": 2566.2,
                "cruise_speed_kmh": 905.72,
                "cost_per_km": 0.88
            }
        )

        round_trip = RoundTrip(flight1,flight2)

        expected_total_price = {
            "fare": 3785.14,
            "fees": 378.52,
            "total": 4163.66
        }

        total_price = round_trip._calculate_total_price()

        self.assertDictEqual(total_price, expected_total_price)


class TestAirlineManager(TestCase):
    def __init__(self, methodName = "runTest"):
        super().__init__(methodName)
        self.api_client = ApiClient(
                base_url=settings.STUB_AMOPROMO_BASE_URL,
                username=settings.STUB_AMOPROMO_USERNAME,
                password=settings.STUB_AMOPROMO_PASSWORD,
                api_key=settings.STUP_AMOPROMO_API_KEY
        )

    def test_get_airlines_with_invalid_dates(self):
    
        with self.assertRaises(ValueError) as context:
            
            iata_from = 'MAO'
            iata_to = 'PLU'
            departure_date = '2022-01-01'
            return_date = '2021-12-31'

            AirlineManager(self.api_client).get_airlines_combinations(
                iata_from, iata_to, departure_date, return_date
            )
        
        self.assertEqual(
            str(context.exception), 
            "The departure date must be before the return date."
        )
    
    def test_get_airlines_with_invalid_iatas(self):
    
        with self.assertRaises(ValueError) as context:
            
            iata_from = 'MSAO'
            iata_to = 'PLU'
            departure_date = '2022-01-01'
            return_date = '2022-01-05'

            AirlineManager(self.api_client).get_airlines_combinations(
                iata_from, iata_to, departure_date, return_date
            )
        
        self.assertEqual(
            str(context.exception), 
            "Invalid airport IATA codes."
        )

        

        
        