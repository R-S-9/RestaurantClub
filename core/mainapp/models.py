from django.db import models
from django.utils import timezone


class Restaurant(models.Model):
	"""Ресторан."""
	restaurant_name = models.CharField(
		max_length=30,
		verbose_name='Название',
		blank=False
	)

	restaurant_id = models.AutoField(primary_key=True)

	menu = models.CharField(
		max_length=255,
		verbose_name='Меню',
		blank=False,
		null=True
	)

	location = models.CharField(
		max_length=150,
		verbose_name='Адрес',
		blank=False
	)



	def __str__(self):
		return self.restaurant_name

	class Meta:
		verbose_name = 'Ресторан'
		verbose_name_plural = 'Рестораны'
		# ordering = ('-date',)


class Reviews(models.Model):
	"""Отзывы."""

	reviews = models.CharField(
		max_length=255,
		verbose_name='Отзыв',
		blank=False,
		primary_key=True  #####
	)

	id_restaurant = models.ForeignKey(
		Restaurant,
		verbose_name='Отзыв о ресторане',
		on_delete=models.CASCADE,
	)

	date = models.DateTimeField(verbose_name='Дата', default=timezone.now)
	# order = models.IntegerField(verbose_name='Порядковый номер',)


	# def _set_order(self):
	# 	last_order = self.__class__.objects.filter(
	# 		id_restaurant=self.id_restaurant
	# 	).order_by('order').values_list(
	# 		'order', flat=True
	# 	).last()
	#
	# 	if last_order:
	# 		self.order = last_order + 1
	# 	else:
	# 		self.order = 1
	#
	# def save(self, *args, **kwargs):
	# 	self._set_order()
	# 	super(Reviews, self).save(*args, **kwargs)
	#
	def __str__(self):
		return f'{self.id_restaurant} - {self.date}'

	class Meta:
		verbose_name = 'id отзыв'
		verbose_name_plural = 'id отзывы'
		# unique_together = ('id_restaurant', 'order')
		# ordering = ('order',)


class Image(models.Model):
	image = models.ImageField(verbose_name='Изображения')






