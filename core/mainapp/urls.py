from django.urls import path

from .views import index, search_results_view, restaurants_map, \
    feedback_restaurant


urlpatterns = [
    path('', index),
    path('search/', search_results_view, name='search_results_view'),
    path('restaurant-<str:rest_name>-/', restaurants_map, name='restaurant'),
    path('feedback-<str:rest_name>-/', feedback_restaurant, name='feedback')
]
