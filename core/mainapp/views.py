from django.shortcuts import render, get_object_or_404
from django.db.models import Avg
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from .models import Reviews, Restaurant
from .forms import AddReviews


def index(request):

    restaurants = Restaurant.objects.filter(
        Q(reviews__stars__icontains=5)
    ).distinct()[:5]

    data = [
        {
            'restaurant_name': r.restaurant_name,
            'reviews': r.reviews.values('review', 'stars'),
            'rating': float('{:.1f}'.format(
                        r.reviews.aggregate(Avg('stars'))['stars__avg'])
                        )
        } for r in restaurants
    ]

    return render(request, 'base.html', {'data': data})


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

        if not restaurants.exists() or search_word == '':
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
                'rating': float('{:.1f}'.format(
                    r.reviews.aggregate(Avg('stars'))['stars__avg']
                    )
                )
            } for r in restaurants
        ]

        return render(
            request,
            'search_results.html',
            {
                'data': restaurants_data,
                'search_word': search_word.capitalize()
            }
        )

        # return JsonResponse(
        #     {
        #         'search_word': search_word.capitalize()
        #     }
        # )


def restaurants_map(request, rest_name):
    if request.method == 'GET' or 'POST':

        restaurant = Restaurant.objects.filter(
            restaurant_name__icontains=rest_name
        )

        data = [
            {
                'restaurant_name': r.restaurant_name,
                'menu': '\n'.join(r.dish_set.values_list('name', flat=True)),
                'reviews': r.reviews.values('review', 'stars'),
                'rating': float('{:.1f}'.format(
                    r.reviews.aggregate(Avg('stars'))['stars__avg']
                    )
                )
            } for r in restaurant
        ]

        return render(
            request,
            'restaurant.html',
            {
                'data': data,
            }
        )


@csrf_exempt
def feedback_restaurant(request, rest_name):
    if request.method == "GET":

        form = AddReviews()
        return render(request, 'feedback.html', {
            'restaurant_name': rest_name,
            'form': form,
        })

    if request.method == "POST":
        postForm = AddReviews(request.POST)

        ids = Restaurant.objects.filter(
            restaurant_name=rest_name
        )

        for i in ids:
            ids = i.pk

        post = get_object_or_404(Restaurant.objects.filter(restaurant_id=ids))

        if postForm.is_valid():
            post_form = postForm.save(commit=False)
            post_form.post = post, request.POST
            post_form.id_restaurant = post
            post_form.save()
            return restaurants_map(request, rest_name)
        else:
            errors = 'Введенные вами данные не корректны.\n' \
                     'Имя должно состоять от 3 до 25 символов.\n' \
                     'Отзыв не должен превышать 255 символов.\n' \
                     'Ресторан оценивается по 5 бальной шкале.\n'

            form = AddReviews()

            return render(request, 'feedback.html', {
                'errors': errors,
                'restaurant_name': rest_name,
                'form': form,
            }
                          )
    else:
        form = AddReviews()

        return render(
            request, 'feedback.html',
            {
                'restaurant_name': rest_name,
                'form': form,
            }
                      )
