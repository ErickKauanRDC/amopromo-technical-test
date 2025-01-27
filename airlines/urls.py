from django.urls import path
from airlines.views.airline_combinator_view import AirlineCombinatorView


urlpatterns = [
    ## localhost:8000/airlines/airline_combinator?from=PLU&to=MAO&departure_date=2022-06-12&return_date=2022-06-15
    path('airline-combinator/<str:from_iata>/<str:to_iata>/<str:departure_date>/<str:return_date>', AirlineCombinatorView.as_view(), name='airline_combinator'),
]
