from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction

from care_point.models import Manager, Point_of_care

User = get_user_model()


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ManagerSignUpForm(UserCreationForm):
    point_of_care = forms.ModelChoiceField(
        queryset=Point_of_care.objects.all(),
        required=True,
        label='Odział',
    )

    class Meta(UserCreationForm.Meta):
        fields = ('first_name', 'last_name', 'username',)
        model = User
        labels = {
            'username': 'Login',
            'first_name': 'Imie',
            'last_name': 'Nazwisko',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_manager = True
        if commit:
            user.save()
        poc = self.cleaned_data.get('point_of_care')
        manager = Manager.objects.create(user=user, point_of_care=poc)
        return user


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = ['first_name', 'last_name']

        labels = {
            'first_name': 'Imie',
            'last_name': 'Nazwisko',
        }