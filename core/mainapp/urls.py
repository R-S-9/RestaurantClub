from django.urls import path, include

from .views import index, SearchResultsView


urlpatterns = [
    path('', index),
    path('serch', SearchResultsView),
]
