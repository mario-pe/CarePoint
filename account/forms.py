import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms import DateField

from care_point.models import Manager, Point_of_care, Caregiver, Contract

User = get_user_model()


class LoginForm(forms.Form):

    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class ManagerSignUpForm(UserCreationForm):
    point_of_care = forms.ModelChoiceField(
        queryset=Point_of_care.objects.all(),
        required=True,
        label='Odział'
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
        point_of_care = self.cleaned_data.get('point_of_care')
        Manager.objects.create(user=user, point_of_care=point_of_care)
        return user


class CaregiverSignUpForm(UserCreationForm): # poszerzyc formularz o pola potrzebne do utworzenia obiektów powiazanych z caregiver

    CONTRACT_TYPE = (
        ('umowa', 'umowa'),
        ('zlecenie', 'zlecenie')
    )

    point_of_care = forms.ModelChoiceField(
        queryset=Point_of_care.objects.all(),
        required=True,
        label='Odział',
    )
    contract_type = forms.ChoiceField(
        choices=CONTRACT_TYPE,
        required=True,
        label='Umowa',
    )
    contract_start_date = DateField(initial=datetime.date.today, label='Poczatek umowy')
    contract_end_date = DateField(initial=datetime.date.today() + datetime.timedelta(days=1), label='Koniec umowy')

    class Meta:
        model = User

        fields = ['username', 'first_name', 'last_name',]

        labels = {
            'username': 'Login',
            'first_name': 'Imie',
            'last_name': 'Nazwisko',
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_caregiver = True
        if commit:
            user.save()
        point_of_care = self.cleaned_data.get('point_of_care')
        contract_type = self.cleaned_data.get('contract_type')
        contract_start_date = self.cleaned_data.get('contract_start_date')
        contract_end_date = self.cleaned_data.get('contract_end_date')
        caregiver = Caregiver.objects.create(user=user, point_of_care=point_of_care)
        Contract.objects.create(genre=contract_type, date_from=contract_start_date, date_to=contract_end_date, caregiver=caregiver)
        return user


class UpdateUserForm(forms.ModelForm):

    class Meta:
        model = User

        fields = ['first_name', 'last_name']

        labels = {
            'first_name': 'Imie',
            'last_name': 'Nazwisko',
        }