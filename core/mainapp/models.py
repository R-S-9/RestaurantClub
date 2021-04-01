from django.db import models

from django.utils import timezone


class Restaurant(models.Model):
    """Ресторан."""
    restaurant_name = models.CharField(
        max_length=30,
        verbose_name='Название.',
        blank=False,
        help_text='Название ресторана.'
    )

    restaurant_id = models.AutoField(primary_key=True)

    location = models.CharField(
        max_length=150,
        verbose_name='Адрес.',
        blank=False,
        help_text='Адрес ресторана.'
    )

    description_restaurant = models.CharField(
        max_length=150,
        verbose_name='Описание.',
        help_text='Описание ресторана.'
    )

    average_check_restaurant = models.IntegerField(
        verbose_name='Средний чек.',
        help_text='Средний чек.'
    )

    # @staticmethod
    # def search_restaurant_name(ids):
    #     search = []
    #     for idd in ids:
    #         search.append(Restaurant.objects.filter(
    #             restaurant_id=idd
    #         ))
    #
    #     restaurant_name = []
    #     for name in search:
    #         restaurant_name.append(name[0])
    #
    #     return restaurant_name

    def __str__(self):
        return self.restaurant_name

    class Meta:
        verbose_name = 'Ресторан.'
        verbose_name_plural = 'Рестораны.'


# class Menu(models.Model):
#     """Меню."""
#
#     id_menu = models.ForeignKey(
#         Restaurant,
#         verbose_name='Меню ресторана',
#         on_delete=models.CASCADE,
#         blank=False,
#         help_text='Выберите ресторан',
#         related_name='menus'
#     )
#
#     @staticmethod
#     def restaurant_search(menu):
#         """Функция поиска отзывов о ресторанах, выводимыми пользователям."""
#         found = []
#         ids = []
#         review_found = []
#
#         for user in Menu.objects.select_related().all().iterator():
#             if user in menu:
#                 Restaurant.objects.filter(
#                     restaurant_id=user.id
#                 ).order_by('restaurant_id')
#
#                 ids.append(user.id)
#
#         for i in ids:
#             if i:
#                 found.append(Reviews.objects.filter(
#                     id_restaurant=ids[0]
#                 ))
#
#         for i in found[0]:
#             review_found.append([i.review])
#
#         # for i in review:
#         # 	# print(i.id)
#         # 	# print('\n')
#         # 	for j in ids:
#         # 		# print(j)
#         #
#         # 		if i.id == j:
#         # 			print(str(i.id) + ' ' + str(j))
#         # 			print('yes')
#         #
#         # # print(review)
#         # # print(ids)
#         # for i in review:
#         # 	# print(i)
#         # 	# print(ids)
#         # 	for j in ids:
#         # 		# print(j)
#         # 		if i.id == j:
#         # 			# print(j)
#         # 			# print(i.review)
#         # 			review_found.append([i.review])
#         #
#         # # print(Restaurant[ids])
#         # print(ids)
#
#         res_name = Restaurant.search_restaurant_name(ids)
#
#         return review_found, Reviews.star(ids), res_name
#
#     @classmethod
#     def get_data(cls, search_word):
#         """Функция для поиска блюда, введенного пользователем."""
#         menu = cls.objects.filter(
#             Q(menu__icontains=search_word) | Q(menu__iexact=search_word)
#         )
#
#         if menu.exists():
#             return menu, cls._receiving_and_processing_data(menu, search_word)
#
#         return None
#
#     @staticmethod
#     def _receiving_and_processing_data(data, search_word):
#         """Функция для обработки данных по введеным критериям."""
#         print(data)
#         print(search_word)
#         def processing_keyword(information, words):
#             search_all_word = []
#             output = []
#
#             # Writing all words to the list.
#             for content in information:
#                 search_all_word.append(content.menu)
#
#             for content in search_all_word:
#                 output.append(content)
#
#             information = look(output, words)
#
#             return information
#
#         def look(search, words):
#             lol = []
#
#             for i in search:
#                 if (re.findall(words.lower(), str(i))) \
#                         or (re.findall(words.capitalize(), str(i))) \
#                         or (re.findall(words, str(i))):
#                     lol.append(re.split(r'\r\n', i))
#
#             search = []
#             for i in lol:
#                 for j in i:
#                     if re.findall(words, j):
#                         search.append(j)
#
#             return search
#
#         return processing_keyword(data, search_word)
#
#     def __str__(self):
#         return f'Меню {self.id_menu}'
#
#     class Meta:
#         verbose_name = 'Меню'
#         verbose_name_plural = 'Меню'


class Dish(models.Model):
    name = models.CharField(verbose_name='Название.', max_length=50, )

    menu = models.ForeignKey(
        Restaurant,
        verbose_name='Меню.',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо.'
        verbose_name_plural = 'Блюда.'


class Reviews(models.Model):  # Review
    """Отзывы."""
    review = models.CharField(
        max_length=255,
        verbose_name='Отзыв.',
        blank=False,
        help_text='Оставьте отзыв о ресторане.'
    )

    id_restaurant = models.ForeignKey(
        Restaurant,
        verbose_name='Для какого ресторана.',
        on_delete=models.CASCADE,
        blank=False,
        help_text='Выберите ресторан.',
        related_name='reviews'
    )

    user_name = models.CharField(
        max_length=25,
        verbose_name='Имя пользователя.',
        help_text='Напишите выдуманное имя для отзыва.',
        blank=False,
    )

    stars = models.IntegerField(
        verbose_name='Оценка.',
        help_text='Оценка ресторана по 5 бальной шкале.'
    )

    date = models.DateTimeField(
        verbose_name='Дата.',
        default=timezone.now,
        help_text='Дата создается автоматически.'
    )

    order = models.IntegerField(
        verbose_name='Порядковый номер.',
        default=9999,
        help_text='Порядковый номер создается автоматически.'
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
        return f'{self.id_restaurant}'

    class Meta:
        verbose_name = ' отзыв.'
        verbose_name_plural = 'Отзывы.'
        unique_together = ('id_restaurant', 'order')
        ordering = ('order',)


class Image(models.Model):
    """Изображения к ресторану."""
    image_restaurant = models.ImageField(
        verbose_name='Изображения.',
        help_text='Выберите изображение.',
    )

    restaurant_id_image = models.ForeignKey(
        Restaurant,
        verbose_name='Изображение ресторана.',
        on_delete=models.CASCADE,
        blank=False,
        default='Ресторан.',
        help_text='Выберите ресторан.',
        related_name='images'
    )

    order = models.IntegerField(
        verbose_name='Порядковый номер.',
        default=1,
        help_text='Порядковый номер создается автоматически.'
    )

    def __str__(self):
        return str(self.image_restaurant)

    class Meta:
        verbose_name = 'Картинка.'
        verbose_name_plural = 'Картинки.'

