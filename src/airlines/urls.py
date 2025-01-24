from django.urls import path
from airlines.views.airline_combinator import AirlineCombinatorView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()


urlpatterns = [
    ## localhost:8000/airlines/airline_combinator?from=PLU&to=MAO&departure_date=2022-06-12&return_date=2022-06-15
    path('airline-combinator', AirlineCombinatorView.as_view(), name='airline_combinator'),
]

urlpatterns += router.urls