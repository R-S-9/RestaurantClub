from django.shortcuts import render
from django.db.models import Q

from .models import Menu, Reviews


def index(request):
    menu = Menu.objects.all()
    reviews = Reviews.objects.all()
    return render(request, 'base.html', {'menu': menu, 'reviews': reviews})


def SearchResultsView(request):
    # id_restaurant = Menu.objects.filter(id_menu__iexact=)

    word = 'вкусно'
    # menu = Menu.objects.filter(menu__iexact='')
    # menu = Menu.objects.filter(menu__contains='вкусно')
    menu = Menu.objects.filter(Q(menu__contains=word) | Q(menu__iexact=word) | Q(menu__contains=word))

    return render(request, 'search_results.html', {'menu': menu})




