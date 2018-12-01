from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import TextField

from .models import *
from django import forms


class ContractForm(forms.ModelForm):

    class Meta:
        model = Contract

        fields = ['genre', 'date_from', 'date_to']

        labels = {
            'genre': 'Typ',
            'date_from': 'Data od',
            'date_to': 'Data do',
        }


class Point_of_care_Form(forms.ModelForm):

    class Meta:
        model = Point_of_care

        fields = ['city']

        labels = {
            'city': 'miasto',
        }


class UpdateManagerForm(forms.ModelForm):

    class Meta:
        model = Manager

        fields = ['point_of_care']

        labels = {
            'point_of_care': 'Odzial',
        }


class CaregiverForm(forms.ModelForm):

    class Meta:
        model = Caregiver

        fields = ['name', 'sname', 'point_of_care']

        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'point_of_care': 'Odzial',
        }


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = ['city', 'street', 'number', 'zip_code', 'ward']

        labels = {
            'city': 'Miasto',
            'street': 'Ulica',
            'number': 'Numer domu',
            'zip_code': 'Kod pocztowy',
            'ward': 'Podopieczny'
        }


class WardForm(forms.ModelForm):

    class Meta:
        model = Ward

        fields = ['name', 'sname', 'pesel']

        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'pesel': 'PESEL',
            'address': 'Adres',
        }


class DecisionForm(forms.ModelForm):

    class Meta:
        model = Decision

        fields = ['percent_payment', 'hours', 'charge', 'ward']

        labels = {
            'percent_payment': 'Doplata z MOPS w procentach',
            'hours': 'Przyslugujace godziny',
            'charge': 'Stawka godzinowa',
            'ward': 'Podopieczny',
        }


class IllnessForm(forms.ModelForm):

    class Meta:
        model = Illness

        fields = ['name', 'description']

        labels = {
            'name': 'Nazwa shorzenia',
            'description': 'Opis',
        }


class IllnessFormCheckboxes(forms.Form):

    illness = forms.ModelMultipleChoiceField(queryset=Illness.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Choroby')


class IllnessFormCheckboxesForUpdate(forms.Form):

    illness = forms.ModelMultipleChoiceField(queryset=Illness.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Choroby')


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity

        fields = ['name', 'description']

        labels = {
            'name': 'Nazwa shorzenia',
            'description': 'Opis',
        }


class ActivityFormCheckboxes(forms.Form):

    activity = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple())


class WorksheetForm(forms.ModelForm):

    class Meta:
        model = Worksheet

        fields = ['caregiver', 'ward', 'address', 'genre', 'decision', 'date', 'hour_from', 'hour_to',
                  'description']

        labels = {
            'caregiver': 'Opiekunka',
            'ward': 'Podopieczny',
            'address': 'Adres',
            'genre': 'typ zlecenia',
            'decision': 'Decyzji',
            'date': 'Data',
            'hour_from': 'Godzina od',
            'hour_to': 'Godzina do',
        }
