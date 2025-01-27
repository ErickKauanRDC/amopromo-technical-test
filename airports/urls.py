from django.urls import path
from airports.views import AiportETLView
from airports.views.aiport_view import AirportViewSet

urlpatterns = [
    path('load-airports/', AiportETLView.as_view(), name='load-aiports'),  
    path('airport/', AirportViewSet.as_view(), name='airport'),
    path('airport/<int:pk>/', AirportViewSet.as_view(), name='airport'),
]

