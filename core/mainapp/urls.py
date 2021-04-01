from django.urls import path

from .views import index, search_results_view, restaurants_map, accepted_review


urlpatterns = [
    path('', index, name='index'),
    path('search/', search_results_view, name='search_results_view'),
    path('restaurant-<str:rest_name>-/', restaurants_map, name='restaurant'),
    path('restaurant-<str:rest_name>-/accepted_review/',
         accepted_review,
         name='accepted_review'
         )
]
