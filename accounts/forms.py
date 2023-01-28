from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
	name = forms.CharField(label='Nombre', max_length=100)
	email = forms.EmailField(label='Correo electronico')
	password = forms.CharField(label='Contrasenia', widget=forms.PasswordInput())
	password_confirmation = forms.CharField(widget=forms.PasswordInput())
	
	# class Meta:
	# 	model = User
	# 	fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(RegisterForm, self).save(commit=False)
		
		user.email = self.cleaned_data["email"]

		if commit:
			user.save()
		return user