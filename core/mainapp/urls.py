from django.urls import path

from .views import index, search_results_view, restaurants_map, \
    accepted_review, search_results_view_api, restaurants_card_api, \
    create_review


urlpatterns = [
    path('', index, name='index'),
    path('search/', search_results_view, name='search_results_view'),
    path('restaurant-<str:rest_name>-/', restaurants_map, name='restaurant'),
    path('restaurant-<str:rest_name>-/accepted_review/',
         accepted_review,
         name='accepted_review'
         ),
    path('search_results_view_api/',
         search_results_view_api,
         name='search_results_view_api'
         ),
    path('restaurants_card_api/',
         restaurants_card_api,
         name='restaurants_card_api'
         ),
    path('create_review/',
         create_review,
         name='create_review'
         ),
]
