from airports.models import Airport
from setup.viewsets.protect_model_viewset import ProtectModelViewset

class AirportViewSet(ProtectModelViewset):
    model = Airport
    