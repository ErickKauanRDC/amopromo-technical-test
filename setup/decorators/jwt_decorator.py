from django.http import JsonResponse
from functools import wraps
from setup.utils.jwt_utils import JWTUtils  

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')
        
        if not token:
            return JsonResponse({"error": "Authorization token is required"}, status=401)
        
        try:
            token = token.split(' ')[1] if token.startswith('Bearer ') else token
            
            decoded_data = JWTUtils.decode(token)
            
            request.user_data = decoded_data
            return view_func(self,request, *args, **kwargs)
        
        except ValueError as e:
            return JsonResponse({"error": str(e)}, status=401)
    
    return _wrapped_view
