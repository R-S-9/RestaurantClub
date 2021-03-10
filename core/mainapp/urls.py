from django.urls import path, include

from .views import index, search_results_view


urlpatterns = [
    path('', index),
    path('search/', search_results_view, name='search_results_view'),
]
