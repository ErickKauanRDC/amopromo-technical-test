from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets

class ProtectModelViewset(viewsets.ModelViewSet):
    """A protected API viewset that requires authentication."""
    permission_classes = [IsAuthenticated]

    
   