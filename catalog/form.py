from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUp(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', help_text='')
    password1 = forms.CharField(label='Пароль', help_text='', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    password2 = forms.CharField(label='Подтверждение пароля', help_text='', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    email = forms.EmailField(label='Почта', widget=forms.TextInput(attrs={'placeholder': 'name@mail.com'}))
    first_name = forms.CharField(label='Имя', max_length=20)
    last_name = forms.CharField(label='Фамилия', max_length=20, required=False)

    # class Meta:
    #     model = User
    #     fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')




