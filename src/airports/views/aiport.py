from rest_framework import viewsets
from airports.models import Airport
from airports.serializers import AirportSerializer
from setup.views.protect_model_viewset import ProtectModelViewset

class AirportViewSet(ProtectModelViewset):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer