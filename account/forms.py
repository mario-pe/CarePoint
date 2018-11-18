from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserForm(UserCreationForm):
    # username = forms.CharField()
    # first_name = forms.CharField()
    # last_name = forms.CharField()
    # password = forms.CharField(widget=forms.PasswordInput)
    # email = forms.EmailField()
    #
    # class Meta:
    #     model = User
    #
    #     fields = ['username', 'first_name', 'last_name', 'email', 'password']
    #
    #     labels = {
    #         'username': 'Login',
    #         'first_name': 'Imie',
    #         'last_name': 'Nazwisko',
    #         'email': 'email',
    #         'password': 'haslo',
    #
    #     }

    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1')