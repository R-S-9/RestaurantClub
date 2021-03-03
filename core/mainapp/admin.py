from django.contrib import admin

"""
	1. Добавление администратором ресторанов и его меню.
	2. Удаление отзывов.
	
"""

from .models import *

admin.site.register(Restaurant)
admin.site.register(Reviews)
