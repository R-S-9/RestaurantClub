from django.shortcuts import render, get_object_or_404, HttpResponseRedirect,\
    HttpResponse
from django.db.models import Avg, Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from .models import Reviews, Restaurant
from .forms import AddReviews


def index(request):

    restaurants = Restaurant.objects.annotate(
        avg_stars=Avg('reviews__stars')
    ).order_by('-avg_stars').distinct()[:5]
    data = []

    for r in restaurants:
        rate = r.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate is None:
            rating = 'Нету'
        else:
            rating = float('{:.1f}'.format(rate))

        data.append({
            'restaurant_name': r.restaurant_name,
            'reviews': r.reviews.values('review', 'stars'),
            'description_restaurant': r.description_restaurant,
            'about_restaurant': r.about_restaurant,
            'average_check_restaurant': r.average_check_restaurant,
            'location': r.location,
            'rating': rating,
            'image': r.images.values('image_restaurant'),
        })

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


@csrf_exempt
def restaurants_map(request, rest_name):
    def _data_for_rest(rest):
        restaurants = Restaurant.objects.filter(
            restaurant_name__icontains=rest
        )

        information = []

        for r in restaurants:
            rate = r.reviews.aggregate(Avg('stars'))['stars__avg']
            if rate is None:
                rating = 'Нету'
            else:
                rating = float('{:.1f}'.format(rate))

            information.append({
                'restaurant_name': r.restaurant_name,
                'description_restaurant': r.description_restaurant,
                'about_restaurant': r.about_restaurant,
                'average_check_restaurant': r.average_check_restaurant,
                'location': r.location,
                'menu': r.dish_set.order_by('name').values(
                    'name', 'check'),
                'reviews': r.reviews.order_by('-date').values(
                    'review', 'stars', 'user_name', 'date',
                ),
                'rating': rating,
                'image': r.images.values('image_restaurant'),
            })

        # information = [
        #     {
        #         'restaurant_name': r.restaurant_name,
        #         'description_restaurant': r.description_restaurant,
        #         'average_check_restaurant': r.average_check_restaurant,
        #         'location': r.location,
        #         # 'menu': {'menus': '\n'.join(r.dish_set.values_list(
        #         #     'name', flat=True
        #         # )), 'checks': r.dish_set.values_list('check', flat=True)},
        #         'menu': r.dish_set.order_by('name').values(
        #             'name', 'check'),
        #         'reviews': r.reviews.order_by('-date').values(
        #             'review', 'stars', 'user_name', 'date',
        #         ),
        #         'rating': rating,
        #         'image': r.images.values('image_restaurant'),
        #     } for r in restaurant
        # ]

        return information

    data = _data_for_rest(rest_name)

    if request.method == 'GET':

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


def search_results_view_api(request):
    search_word = request.POST.get('search')

    if search_word:
        search_word = search_word.strip()

    filter_ = Q(dish__name__icontains=search_word) if search_word else Q()
    filter_dish = Q(name__icontains=search_word) if search_word else Q()

    restaurants = Restaurant.objects.filter(
        filter_
    ).distinct()

    if not restaurants.exists():
        return HttpResponse(status=404)

    data = [
        {
            'restaurant_name': r.restaurant_name,
            'description_restaurant': r.description_restaurant,
            'average_check_restaurant': r.average_check_restaurant,
            'location': r.location,
            'dish': ', '.join(r.dish_set.filter(
                filter_dish
            ).values_list('name', flat=True)),
            'menu': ', '.join(r.dish_set.values_list('name', flat=True)),
            'reviews': [{
                'review': rs.review, 'stars': rs.stars,
            } for rs in r.reviews.order_by('-date')],
            'rating': float('{:.1f}'.format(
                r.reviews.aggregate(Avg('stars'))['stars__avg']
            )),
            'image': tuple(r.images.values_list('image_restaurant', flat=True))
        } for r in restaurants
    ]

    return JsonResponse(dict(data=data))


def restaurants_card_api(request):

    rest_id = request.POST.get('rest_id')

    r = Restaurant.objects.filter(
        restaurant_id=rest_id
    ).first()

    if not r:
        return HttpResponse(status=404)

    information = {
            'restaurant_name': r.restaurant_name,
            'description_restaurant': r.description_restaurant,
            'average_check_restaurant': r.average_check_restaurant,
            'location': r.location,
            'menu': '\n'.join(r.dish_set.values_list('name', flat=True)),
            'reviews': [{
                'review': rs.review, 'stars': rs.stars,
                'user_name': rs.user_name, 'date': rs.date
            } for rs in r.reviews.order_by('-date')],
            'rating': float('{:.1f}'.format(
                r.reviews.aggregate(Avg('stars'))['stars__avg']
            )),
            'image': tuple(r.images.values_list(
                'image_restaurant',
                flat=True)),
        }

    return JsonResponse(information)


def create_review(request):
    """Принимает отзыв через api."""
    try:
        rest_id = request.POST.get('rest_id')
        if not rest_id:
            return HttpResponse(status=400)
        rest_id = int(rest_id)
    except ValueError:
        return HttpResponse(status=400)

    review = request.POST.get('review')
    if not review:
        return HttpResponse(status=400)

    user_name = request.POST.get('user_name')
    if not user_name:
        return HttpResponse(status=400)

    try:
        stars = request.POST.get('stars')
        if not stars:
            return HttpResponse(status=400)
        stars = int(stars)
    except ValueError:
        return HttpResponse(status=400)

    try:
        Reviews.objects.create(
            review=review,
            id_restaurant_id=rest_id,
            user_name=user_name,
            stars=stars,
        )
    except Restaurant.DoesNotExist:
        return HttpResponse(status=400)

    return HttpResponse(status=200)
