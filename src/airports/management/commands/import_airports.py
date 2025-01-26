
from airports.views.aiport_etl_view import AirportETL
from django.core.management.base import BaseCommand

from common.api_client import ApiClient
from django.conf import settings

class Command(BaseCommand):
    """Command to Extract, Transform and Loads the airport data to airpot table"""
    help = "Extract, Transform and Loads the airport data to airpot table"

    def handle(self, *args, **kwargs):
        """Handle the command operation"""
        try:
            api_client = ApiClient(
                base_url=settings.STUB_AMOPROMO_BASE_URL,
                username=settings.STUB_AMOPROMO_USERNAME,
                password=settings.STUB_AMOPROMO_PASSWORD,
                api_key=settings.STUP_AMOPROMO_API_KEY
            )

       
            self.stdout.write('Starting the ETL process...')
            log = AirportETL(api_client).run() 
 
            self.stdout.write(f'The ETL has finished sucessful with and inserted into database {log.n_records} records')
        except Exception as e:
            self.stderr.write(f'Error during the ETL process: {e}')
            raise e