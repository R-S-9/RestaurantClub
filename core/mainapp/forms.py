from django import forms

from .models import Reviews


class AddReviews(forms.ModelForm):
	class Meta:
		model = Reviews
		fields = [
			'user_name',
			'review',
			'stars'	
		]

		widgets = {
            'user_name': forms.TextInput(attrs={'placeholder':'Введите имя','class':'form-control'}),
            'review': forms.Textarea(attrs={'placeholder':'Отзыв','class':'form-control-review'}),
            'stars': forms.TextInput(attrs={'placeholder': 'Оценка',
                                           'class': 'form-control'}),
        }

	def clean(self):
		if (self.cleaned_data.get('stars') > 5) or (
				self.cleaned_data.get('stars') < 1):
			raise forms.ValidationError(
				'Звезды ставятся по 5 бальной шкале.'
			)
		if (len(str(self.cleaned_data.get('user_name'))) > 25) or (
				len(str(self.cleaned_data.get('user_name'))) < 1):
			raise forms.ValidationError(
				'Имя должно быть от 3 до 25 символов.'
			)
		if (len(str(self.cleaned_data.get('user_name'))) > 255) or (
				len(str(self.cleaned_data.get('user_name'))) < 1):
			raise forms.ValidationError(
				'Отзыв не должен превышать 255 символов.'
			)
		return self.cleaned_data
