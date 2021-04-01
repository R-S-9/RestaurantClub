from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
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
            'description_restaurant': r.description_restaurant,
            'average_check_restaurant': r.average_check_restaurant,
            'location': r.location,
            'rating': float('{:.1f}'.format(
                        r.reviews.aggregate(Avg('stars'))['stars__avg'])
                        ),
            'image': r.images.values('image_restaurant'),
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
        ).distinct()

        if not restaurants.exists() or search_word == '':
            errors = 'Введенного вами блюда, не найдено.'
            return render(request, 'base.html', {'errors': errors})

        restaurants_data = [
            {
                'restaurant_name': r.restaurant_name,
                'description_restaurant': r.description_restaurant,
                'average_check_restaurant': r.average_check_restaurant,
                'location': r.location,
                'dish': ', '.join(r.dish_set.filter(
                    name__icontains=search_word
                ).values_list('name', flat=True)),
                'menu': ', '.join(r.dish_set.values_list('name', flat=True)),
                'reviews': r.reviews.values('review', 'stars'),
                'rating': float('{:.1f}'.format(
                    r.reviews.aggregate(Avg('stars'))['stars__avg']
                    )
                ),
                'image': r.images.values('image_restaurant'),
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


@csrf_exempt
def restaurants_map(request, rest_name):
    def _data_for_rest(rest):
        restaurant = Restaurant.objects.filter(
            restaurant_name__icontains=rest
        )

        information = [
            {
                'restaurant_name': r.restaurant_name,
                'description_restaurant': r.description_restaurant,
                'average_check_restaurant': r.average_check_restaurant,
                'location': r.location,
                'menu': '\n'.join(r.dish_set.values_list('name', flat=True)),
                'reviews': r.reviews.values('review', 'stars', 'user_name'),
                'rating': float('{:.1f}'.format(
                    r.reviews.aggregate(Avg('stars'))['stars__avg']
                )
                ),
                'image': r.images.values('image_restaurant'),
            } for r in restaurant
        ]

        return information

    if request.method == 'GET':

        data = _data_for_rest(rest_name)

        form = AddReviews()

        return render(
            request,
            'restaurant.html',
            {
                'data': data,
                'form': form,
            }
        )

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
            return HttpResponseRedirect("accepted_review")
        else:

            data = _data_for_rest(rest_name)

            errors = 'Введенные вами данные не корректны:\n' \
                     'Имя должно состоять от 3 до 25 символов.\n' \
                     'Отзыв не должен превышать 255 символов.\n' \
                     'Ресторан оценивается по 5 бальной шкале.\n'

            form = AddReviews()

            return render(
                request, 'restaurant.html',
                {
                    'data': data,
                    'form': form,
                    'errors': errors,
                }
            )


def accepted_review(request, rest_name):
    return render(request, 'accepted_review.html', {'rest_name': rest_name})
