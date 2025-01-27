from django.http import JsonResponse
from django.views import View
from django.db.models import Model

from setup.decorators.jwt_decorator import jwt_required

class ProtectModelViewset(View):
    """A protected API viewset that requires authentication."""
    model: Model = None
    fields = '__all__'

    def _get_queryset(self):
        """Return all objects from the model or specific fields if defined."""
        if self.fields == "__all__":
            return self.model.objects.all().values()
        return self.model.objects.all().values(self.fields)
    
    def _get_unique_obj(self, id):
        """Return a single object from the model or specific fields if defined."""
        if self.fields == "__all__":
            return self.model.objects.filter(id=id).values()
        return self.model.objects.all().filter(id=id).values(self.fields)

    @jwt_required
    def get(self, request, pk=None, *args, **kwargs):
        """Handle GET requests to return a queryset or a single object."""
        try:
            if pk:
                result = self._get_unique_obj(pk)
                if not result:
                    return JsonResponse({
                        'error': f'Object with id {pk} not found.'
                    }, status=404)
            else:
                result = self._get_queryset()
            
            return JsonResponse(list(result), safe=False, status=200)
        
        except Exception as e:
            return JsonResponse({
                'error': str(e)
            }, status=500)
