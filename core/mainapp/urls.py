from django.urls import path

from .views import main_map_restaurants, create_review, restaurants_map, \
    accepted_review, search_results_view_api, restaurants_card_api, \
    search_results_view, main_map_restaurants_api, accepted_coop


urlpatterns = [
    path('', main_map_restaurants, name='main_map_restaurants'),
    path('search/', search_results_view, name='search_results_view'),
    path('restaurant-<str:rest_name>-/', restaurants_map, name='restaurant'),
    path('accepted_coop', accepted_coop, name='accepted_coop'),
    path('restaurant-<str:rest_name>-/accepted_review/',
         accepted_review,
         name='accepted_review'
         ),
    path('main_map_restaurants_api',
         main_map_restaurants_api,
         name='main_map_restaurants_api'
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
         )
]
