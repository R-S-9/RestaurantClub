from django import forms

from .models import Review


class AddReviews(forms.ModelForm):
	class Meta:
		model = Review
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
				'maxlength': '1000',
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
	name = forms.CharField(required=True, max_length=30)
	description = forms.CharField(required=True, max_length=250)
	link = forms.CharField(label='Ваш сайт:', required=False, max_length=150)

	# TODO дописать фронт для такущей формы
	widgets = {
		'email': forms.EmailInput(attrs={
			'max': '50',
		}),
		'name': forms.TextInput(attrs={
			'min': '2',
			'max': '30',
		}),
		'description': forms.TextInput(attrs={
			'max': '1500',
		}),
		'link': forms.TextInput(attrs={
			'max': '255',
		}),
	}
