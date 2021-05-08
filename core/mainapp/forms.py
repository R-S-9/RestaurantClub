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
				'minlength': '3',
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
