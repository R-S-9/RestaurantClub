import json
from operator import itemgetter

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect,\
    HttpResponse
from django.db.models import Avg, Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail

from .models import Review, Restaurant, adding_endings_for_improved_search
from .forms import AddReviews, Feedback
from django.conf import settings


def main_map_restaurants(request, errors=None, form=None):

    if not form and 'application_to_add' in request.POST:
        return restaurant_offer(request)

    return loading_data_for_main_site(request, errors)


def restaurant_offer(request):
    form = Feedback(request.POST)

    if form.is_valid():
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        description = form.cleaned_data['description']
        link = form.cleaned_data['link']

        message = f'Доброго времени суток RestaurantClub. Я {name}, хочу ' \
                  f'добавить свой ресторан в ваше приложение.\nМой e-mail ' \
                  f'для контакта - {email}.\nИнформация о моем ресторане:\n' \
                  f'{description}\nСсылки: {link}'

        send_mail(
            f'Сотрудничество с сайтом RestaurantClub от {name}',
            message,
            settings.EMAIL_HOST_USER,
            [
                'rafik.saakyan.1989@mail.ru'
            ]
        )

    return HttpResponseRedirect('accepted_coop')


def accepted_coop(request):
    return render(request, 'accepted_coop.html', {})


def loading_data_for_main_site(request, errors):
    if not errors:
        errors = False

    restaurants = Restaurant.objects.annotate(
        avg_stars=Avg('reviews__stars')
    ).order_by('-avg_stars').distinct()[:10]
    data = []

    for r in restaurants:
        rate = r.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate is None:
            rating = 0
        else:
            rating = float('{:.1f}'.format(rate))

        data.append({
            'restaurant_name': r.restaurant_name,
            'description_restaurant': r.description_restaurant,
            'rating': rating,
            'image': r.images.values('image_restaurant'),
            'reviews': r.reviews.values('review', 'stars'),
        })

    data.sort(key=itemgetter('rating'), reverse=True)

    return render(request, 'base.html', {'data': data, 'errors': errors})


@csrf_exempt
def search_results_view(request):
    if request.method == 'GET':
        menu = Restaurant.objects.all()
        reviews = Review.objects.all()

        return render(
            request,
            'base.html',
            {'menu': menu, 'reviews': reviews}
        )

    if request.method == 'POST':
        search_word = request.POST.get('search').strip()

        search_word = adding_endings_for_improved_search(search_word)

        restaurants = Restaurant.objects.filter(
            dish__name__icontains=search_word
        ).distinct()

        if not restaurants.exists() or search_word == '':
            errors = 'Введенного вами блюда, не найдено.'
            return main_map_restaurants(request, errors)

        data = []

        for r in restaurants:
            rate = r.reviews.aggregate(Avg('stars'))['stars__avg']

            if rate is None:
                rating = 0
            else:
                rating = float('{:.1f}'.format(rate))

            dish = r.dish_set.filter(
                name__icontains=search_word
            ).values('name', 'check')

            data.append({
                'restaurant_name': r.restaurant_name,
                'dish': [
                    {'name': i['name'], 'check': i['check']} for i in dish
                ],
                'description_restaurant': r.description_restaurant,
                'location': r.location,
                'rating': rating,
                'image': r.images.values('image_restaurant'),
                'reviews': r.reviews.values('review', 'stars'),
            })

        data.sort(key=itemgetter('rating'), reverse=True)

        return render(
            request,
            'search_results.html',
            {
                'data': data,
                'search_word': search_word.capitalize(),
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
                     'Имя должно состоять от 2 до 25 символов.\n' \
                     'Отзыв не должен превышать 250 символов.\n' \
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


def main_map_restaurants_api(request):
    restaurants = Restaurant.objects.annotate(
        avg_stars=Avg('reviews__stars')
    ).order_by('-avg_stars').distinct()[:12]

    if not restaurants:
        return HttpResponse(status=400)

    data = []

    for r in restaurants:
        rate = r.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate is None:
            rating = 0
        else:
            rating = float('{:.1f}'.format(rate))

        data.append({
            'restaurant_name': r.restaurant_name,
            'restaurant_id': r.restaurant_id,
            'description_restaurant': r.description_restaurant,
            'average_check_restaurant': r.average_check_restaurant,
            'location': r.location,
            'rating': rating,
            'image': tuple(r.images.values_list(
                'image_restaurant',
                flat=True
            ))
        })

    data.sort(key=itemgetter('rating'), reverse=True)

    return JsonResponse(dict(data=data))


def search_results_view_api(request):

    if request.method != 'GET':
        return HttpResponse(status=400)

    search_word = request.GET.get('search')

    if search_word:
        search_word = search_word.strip()

    filter_ = Q(dish__name__icontains=search_word) if search_word else Q()
    filter_dish = Q(name__icontains=search_word) if search_word else Q()

    restaurants = Restaurant.objects.filter(
        filter_,
    ).distinct()

    if not restaurants.exists():
        return HttpResponse(status=404)

    data = []

    for r in restaurants:
        rate = r.reviews.aggregate(Avg('stars'))['stars__avg']
        if rate is None:
            rating = 0
        else:
            rating = float('{:.1f}'.format(rate))

        data.append({
                'restaurant_name': r.restaurant_name,
                'restaurant_id': r.restaurant_id,
                'description_restaurant': r.description_restaurant,
                'average_check_restaurant': r.average_check_restaurant,
                'location': r.location,
                'dish': ', '.join(r.dish_set.filter(
                    filter_dish
                ).values_list('name', flat=True)),
                'rating': rating,
                'image': tuple(r.images.values_list(
                    'image_restaurant',
                    flat=True
                ))
            }
        )

    data.sort(key=itemgetter('rating'), reverse=True)

    return JsonResponse(dict(data=data))


def restaurants_card_api(request):
    if request.method != 'GET':
        return HttpResponse(status=400)

    try:
        rest_id = int(request.GET.get('rest_id'))
    except ValueError:
        return HttpResponse(status=400)

    r = Restaurant.objects.filter(
        restaurant_id=rest_id
    ).first()

    if not r:
        return HttpResponse(status=404)

    information = {
            'restaurant_name': r.restaurant_name,
            'restaurant_id': r.restaurant_id,
            'description_restaurant': r.description_restaurant,
            'about_restaurant': r.about_restaurant,
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

    data = json.loads(request.body)

    try:
        rest_id = data.get('rest_id', None)
        if not rest_id:
            return HttpResponse(status=400)
        rest_id = int(rest_id)

    except ValueError:
        return HttpResponse(status=400)

    review = data.get('review', None)
    if not review:
        return HttpResponse(status=400)

    user_name = data.get('user_name', None)
    if not user_name:
        return HttpResponse(status=400)

    try:
        stars = data.get('stars', None)
        if not stars:
            return HttpResponse(status=400)
        stars = int(stars)
        if stars > 5 or stars < 1:
            return HttpResponse(status=400)
    except ValueError:
        return HttpResponse(status=400)

    try:
        Review.objects.create(
            review=review,
            id_restaurant_id=rest_id,
            user_name=user_name,
            stars=stars,
        )
    except Restaurant.DoesNotExist:
        return HttpResponse(status=404)

    return HttpResponse(status=200)
