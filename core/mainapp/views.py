from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import Q

from .models import Menu, Reviews

from django.views.decorators.csrf import csrf_exempt


def index(request):
    menu = Menu.objects.all()
    reviews = Reviews.objects.all()
    return render(request, 'base.html', {'menu': menu, 'reviews': reviews})


@csrf_exempt
def search_results_view(request):
    if request.method == 'GET':
        menu = Menu.objects.all()
        reviews = Reviews.objects.all()
        return render(
            request,
            'search_results.html',
            {'menu': menu, 'reviews': reviews}
        )

    if request.method == 'POST':
        search_word = request.POST.get('search').strip()

        data = Menu.get_data(search_word)

        if data is None:
            errors = 'Введенного вами блюда, не найдено.'
            return render(request, 'base.html', {'errors': errors})

        menu, dish = data

        return render(
            request,
            'search_results.html',
            {
                'menu': menu,
                'search_word': search_word.capitalize(),
                'dish': dish
            }
        )

        # return JsonResponse(
        #     {
        #         'search_word': search_word.capitalize()
        #     }
        # )
