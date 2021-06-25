from django.contrib import admin

from .models import *


class DishInline(admin.TabularInline):
	model = Dish
	extra = 2


class ImageInline(admin.TabularInline):
	model = Image
	extra = 1


class ReviewInline(admin.TabularInline):
	model = Review
	extra = 1


class RestaurantAdmin(admin.ModelAdmin):
	field = '__all__'

	inlines = [DishInline, ReviewInline, ImageInline]
	list_display = (
		'restaurant_name',
		'average_check_restaurant',
		'description_restaurant',
		'location'
	)
	list_filter = ['average_check_restaurant']
	search_fields = ['restaurant_name']


admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Review)
admin.site.register(Image)
admin.site.register(Dish)
