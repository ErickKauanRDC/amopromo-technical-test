from airports.models.airport import Airport
from common.api_client import ApiClient
from logs.models.data_load_log import DataLoadLog
from setup import settings
from django.http import JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from setup.views.protect_api_view import ProtectedApiView


class AirportETL:
    """Extract, transform, and load data from an external API to a database."""
    def __init__(self, api_client):
        """Initialize the ETL process with an API client."""
        self.api_client = api_client
        self.log = self.create_initial_log()

    def create_initial_log(self):
        """Create an initial log for the ETL process."""
        return DataLoadLog.objects.create(
            model='Airport',
            success=False,
            message='The ETL process has started'
        )

    def update_log(self, success, message, n_records):
        """Update the log with the current status of the ETL process."""
        self.log.success = success
        self.log.message = message
        self.log.n_records = n_records
        self.log.save()

    def extract(self):
        """Extract data from the external API."""
        try:
            return self.api_client.get('air/airports')
        except Exception as e:
            self.update_log(False, f"Error during extraction: {e}", 0)
            return None

    def transform(self, airports):
        """Transform the extracted data into a list of Airport objects."""
        if not airports:
            self.update_log(False, "No airports data to transform.", 0)
            return None
        
        try:
            to_create = [
                Airport(
                    iata=iata,
                    city=data['city'],
                    latitude=data['lat'],
                    longitude=data['lon'],
                    state=data['state']
                )
                for iata, data in airports.items()
            ]
            return to_create
        except Exception as e:
            self.update_log(False, f"Error during transformation: {e}", 0)
            return None

    def load(self, airports):
        """Load the transformed data to database."""
        if not airports:
            self.update_log(False, "No airports data to load.", 0)
            return

        try:
            Airport.objects.all().delete()
            Airport.objects.bulk_create(airports)
            self.update_log(True, "The ETL process finished successfully.", len(airports))
        except Exception as e:
            self.update_log(False, f"Error during loading: {e}", 0)

    def run(self):
        """Run the ETL process."""
        airports = self.extract()
        if not airports:
            return self.log
        
        transformed_data = self.transform(airports)
        if not transformed_data:
            return self.log
        
        self.load(transformed_data)
        return self.log
    


class AiportETLView(ProtectedApiView):
    """API view to trigger the Airport ETL process."""
    def post(self, request):
        """Handle POST requests to trigger the ETL process."""
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

        etl = AirportETL(api_client)
        log = etl.run()

        return JsonResponse({
            "message": log.message,
            "success": log.success,
            "n_records": log.n_records,
        }, status=200)

