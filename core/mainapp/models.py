from django.db import models
from django.db.models import Q

from django.utils import timezone


class Restaurant(models.Model):
	"""Ресторан."""
	restaurant_name = models.CharField(
		max_length=30,
		verbose_name='Название',
		blank=False,
		help_text='Название ресторана'
	)

	restaurant_id = models.AutoField(primary_key=True)

	location = models.CharField(
		max_length=150,
		verbose_name='Адрес',
		blank=False,
		help_text='Адрес ресторана'
	)

	def __str__(self):
		return self.restaurant_name

	class Meta:
		verbose_name = 'Ресторан'
		verbose_name_plural = 'Рестораны'


class Menu(models.Model):
	"""Меню."""
	menu = models.TextField(
		blank=False,
		verbose_name='Меню ресторана',
		help_text='Опишите каждое блюдо, с игридиентами, ценой и граммовкой',

	)

	id_menu = models.ForeignKey(
		Restaurant,
		verbose_name='Меню ресторана',
		on_delete=models.CASCADE,
		blank=False,
		help_text='Выберите ресторан'
	)

	@classmethod
	def get_data(cls, search_word):
		menu = cls.objects.filter(
			Q(menu__icontains=search_word) | Q(menu__iexact=search_word)
		)

		if menu.exists():
			return menu, cls._receiving_and_processing_data(menu, search_word)

		return None

	@staticmethod
	def _receiving_and_processing_data(data, search_word):
		"""Функция для обработки данных по введеным критериям."""

		first = []
		# Запись всех слов в список.
		for content in data:
			if not first:
				first.append(content.menu)

		helper = None
		for content in first:
			helper = content
		first = helper.split('\n')

		main_data = None
		for content in first:
			if search_word in content:
				main_data = content

		return main_data

	def __str__(self):
		return f'Меню {self.id_menu}'

	class Meta:
		verbose_name = 'Меню'
		verbose_name_plural = 'Меню'


class Reviews(models.Model):
	"""Отзывы."""
	reviews = models.CharField(
		max_length=255,
		verbose_name='Отзыв',
		blank=False,
		help_text='Оставьте отзыв о ресторане'
	)

	id_restaurant = models.ForeignKey(
		Restaurant,
		verbose_name='Для какого ресторана',
		on_delete=models.CASCADE,
		blank=False,
		help_text='Выберите ресторан'
	)

	stars = models.IntegerField(
		verbose_name='Оценка',
		default=5,
		help_text='Оценка ресторана по 5 бальной шкале'
	)

	date = models.DateTimeField(
		verbose_name='Дата',
		default=timezone.now,
		help_text='Дата создается автоматически'
	)

	order = models.IntegerField(
		verbose_name='Порядковый номер',
		default=9999,
		help_text='Порядковый номер создается автоматически'
	)

	def _set_order(self):
		last_order = self.__class__.objects.filter(
			id_restaurant=self.id_restaurant
		).order_by('order').values_list(
			'order', flat=True
		).last()

		if last_order:
			self.order = last_order + 1
		else:
			self.order = 1

	def save(self, *args, **kwargs):
		self._set_order()
		super(Reviews, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.id_restaurant} - id {self.order} - {self.date}'

	class Meta:
		verbose_name = 'ID отзыв'
		verbose_name_plural = 'ID отзывы'
		unique_together = ('id_restaurant', 'order')
		ordering = ('order',)


class Image(models.Model):
	"""Изображения к ресторану."""
	image = models.ImageField(
		verbose_name='Изображения',
		help_text='Выберите изображение'
	)

	menu = models.ForeignKey(
		Restaurant,
		verbose_name='Отзыв о ресторане',
		on_delete=models.CASCADE,
		blank=False,
		default='Ресторан',
		help_text='Выберите ресторан'
	)

	order = models.IntegerField(
		verbose_name='Порядковый номер',
		default=9999,
		help_text='Порядковый номер создается автоматически'
	)

	def _set_order(self):
		last_order = self.__class__.objects.filter(
			menu=self.menu
		).order_by('order').values_list(
			'order', flat=True
		).last()

		if last_order:
			self.order = last_order + 1
		else:
			self.order = 1

	def save(self, *args, **kwargs):
		self._set_order()
		super(Image, self).save(*args, **kwargs)

	def __str__(self):
		return f'{self.menu}: рис. {self.order}'

	class Meta:
		verbose_name = 'Картинка'
		verbose_name_plural = 'Картинки'
		unique_together = ('menu', 'order')
		ordering = ('order',)
