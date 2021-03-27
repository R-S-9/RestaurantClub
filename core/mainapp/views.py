from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Avg

from .models import Reviews, Restaurant

from django.views.decorators.csrf import csrf_exempt


def index(request):
    menu = Restaurant.objects.all()
    reviews = Reviews.objects.all()
    return render(request, 'base.html', {'menu': menu, 'reviews': reviews})


@csrf_exempt
def search_results_view(request):
    if request.method == 'GET':
        menu = Restaurant.objects.all()
        reviews = Reviews.objects.all()

        return render(
            request,
            'base.html',
            {'menu': menu, 'reviews': reviews}
        )

    if request.method == 'POST':
        search_word = request.POST.get('search').strip()

        restaurants = Restaurant.objects.filter(
            dish__name__icontains=search_word
        )

        if not restaurants.exists():
            errors = 'Введенного вами блюда, не найдено.'
            return render(request, 'base.html', {'errors': errors})

        restaurants_data = [
            {
                'restaurant_name': r.restaurant_name,
                'dish': ', '.join(r.dish_set.filter(
                    name__icontains=search_word
                ).values_list('name', flat=True)),
                'menu': ', '.join(r.dish_set.values_list('name', flat=True)),
                'reviews': r.reviews.values('review', 'stars'),
                'rating': float('{:.2f}'.format(
                    r.reviews.aggregate(Avg('stars'))['stars__avg']
                    )
                )
            } for r in restaurants
        ]

        return render(
            request,
            'search_results.html',
            {
                'data': restaurants_data
            }
        )

        # return JsonResponse(
        #     {
        #         'search_word': search_word.capitalize()
        #     }
        # )
