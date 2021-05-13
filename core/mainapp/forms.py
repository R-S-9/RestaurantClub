from django import forms

from .models import Reviews


class AddReviews(forms.ModelForm):
	class Meta:
		model = Reviews
		fields = [
			'user_name',
			'review',
			'stars',
		]

		widgets = {
			'user_name': forms.TextInput(attrs={
				'placeholder': 'Введите имя',
				'class': 'form-control',
				'minlength': '2',
				'maxlength': '25',
			}),
			'review': forms.Textarea(attrs={
				'placeholder': 'Отзыв',
				'class': 'form-control-review',
				'maxlength': '250',
				'width': '10',
			}),
			'stars': forms.TextInput(attrs={
				'placeholder': 'Оценка',
				'class': 'form-control',
				'type': 'number',
				'min': '1',
				'max': '5',
			}),
		}


class Feedback(forms.Form):
	class Meta:
		"""
		1. Емаил дирика
		2. Название ресторана
		3. Описание всего.
		4. Ссылки на инст, на сайты, и тд
		"""

	email = forms.EmailField(required=True, max_length=35)
	rest_name = forms.CharField(required=True, max_length=30)
	description = forms.CharField(required=True, max_length=250)
	link = forms.URLField(label='Ваш сайт:', required=False, max_length=150)

	# TODO дописать фронт для такущей формы
	widgets = {
		'email': forms.EmailInput(attrs={
			'placeholder': 'Email',
			'min': '9',
			'max': '35',
		}),
		'rest_name': forms.EmailInput(attrs={
			'placeholder': 'Название ресторана',
			'min': '1',
			'max': '30',
		}),
		'description': forms.EmailInput(attrs={
			'placeholder': 'О ресторане',
			'min': '1',
			'max': '250',
		}),
		'link': forms.EmailInput(attrs={
			'placeholder': 'Ваш сайт:',
			'max': '150',
		}),
	}
