from django.db import models

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

    description_restaurant = models.CharField(
        max_length=50,
        verbose_name='Описание кухни',
        help_text='Описание кухни ресторана'
    )

    about_restaurant = models.CharField(
        max_length=250,
        verbose_name='Описание ресторана',
        help_text='Полное описание ресторана',
        blank=False,
        default=''
    )

    average_check_restaurant = models.IntegerField(
        verbose_name='Средний чек',
        help_text='Средний чек'
    )

    def __str__(self):
        return self.restaurant_name

    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'


class Dish(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=50,
    )

    check = models.IntegerField(
        verbose_name='Цена',
        default=0,
        help_text='Цена блюда'
    )

    menu = models.ForeignKey(
        Restaurant,
        verbose_name='Меню',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class Reviews(models.Model):  # Review
    """Отзывы."""
    review = models.CharField(
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
        help_text='Выберите ресторан',
        related_name='reviews'
    )

    user_name = models.CharField(
        max_length=25,
        verbose_name='Имя пользователя',
        help_text='Напишите выдуманное имя для отзыва',
        blank=False,
    )

    stars = models.IntegerField(
        verbose_name='Оценка',
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
        return f'{self.id_restaurant} {self.review}'

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        unique_together = ('id_restaurant', 'order')
        ordering = ('-order',)


class Image(models.Model):
    """Изображения к ресторану."""
    image_restaurant = models.ImageField(
        verbose_name='Изображения',
        help_text='Выберите изображение',
    )

    restaurant_id_image = models.ForeignKey(
        Restaurant,
        verbose_name='Изображение ресторана',
        on_delete=models.CASCADE,
        blank=False,
        default='Ресторан',
        help_text='Выберите ресторан',
        related_name='images'
    )

    order = models.IntegerField(
        verbose_name='Порядковый номер',
        default=1,
        help_text='Порядковый номер создается автоматически'
    )

    def __str__(self):
        return str(self.image_restaurant)

    class Meta:
        verbose_name = 'Картинка'
        verbose_name_plural = 'Картинки'
