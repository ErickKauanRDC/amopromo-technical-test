from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

class ProtectedApiView(APIView):
    """A protected API view that requires authentication."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return JsonResponse({'message': 'This is a protected view!'}, status=200)
    
   