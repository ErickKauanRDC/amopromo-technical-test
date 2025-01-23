from django.urls import path
from airports.views import AiportETLView
from rest_framework.routers import DefaultRouter

from airports.views.aiport import AirportViewSet

router = DefaultRouter()
router.register('airports', AirportViewSet, basename='airport')

urlpatterns = [
    path('load-airports/', AiportETLView.as_view(), name='load-aiports'),  
]

urlpatterns += router.urls