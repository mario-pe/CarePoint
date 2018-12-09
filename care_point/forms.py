from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.db.models import TextField

from care_point.utils import _update_or_create_duties
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

        fields = ['point_of_care']

        labels = {
            'point_of_care': 'Odzial',
        }


class AddressFormWard(forms.ModelForm):

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


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address

        fields = ['city', 'street', 'number', 'zip_code', 'ward']

        labels = {
            'city': 'Miasto',
            'street': 'Ulica',
            'number': 'Numer domu',
            'zip_code': 'Kod pocztowy',
        }


class WardForm(forms.ModelForm):

    city = forms.CharField(label='Miasto')
    street = forms.CharField(label='Ulica')
    home_number = forms.CharField(label='Numer domu')
    zip_code = forms.CharField(label='Miasto')

    percent_payment = forms.CharField(label='Doplata z MOPS w procentach')
    hours = forms.CharField(label='Przyslugujace godziny')
    charge = forms.CharField(label='Stawka godzinowa')

    illness = forms.ModelMultipleChoiceField(queryset=Illness.objects.all(), widget=forms.CheckboxSelectMultiple(),
                                             label='Choroby')
    activity = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Aktywności')

    class Meta:
        model = Ward

        fields = ['name', 'sname', 'pesel']

        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'pesel': 'PESEL',
            'address': 'Adres',
        }

    def save(self, commit=True):
        ward = super().save(commit=False)
        if commit:
            ward.save()
        city = self.cleaned_data.get('city')
        street = self.cleaned_data.get('street')
        home_number = self.cleaned_data.get('home_number')
        zip_code = self.cleaned_data.get('zip_code')

        percent_payment = self.cleaned_data.get('percent_payment')
        hours = self.cleaned_data.get('hours')
        charge = self.cleaned_data.get('charge')
        illnesses = self.cleaned_data['illness']
        activites = self.cleaned_data['activity']
        Address.objects.create(city=city, street=street, number=home_number, zip_code=zip_code, ward=ward)
        decision = Decision.objects.create(percent_payment=percent_payment, hours=hours, ward=ward, charge=charge)
        _update_or_create_duties(decision, illnesses, activites)


class WardUpdateForm(forms.ModelForm):

    class Meta:
        model = Ward

        fields = ['name', 'sname', 'pesel']

        labels = {
            'name': 'Imie',
            'sname': 'Nazwisko',
            'pesel': 'PESEL',
        }


class DecisionFormWard(forms.ModelForm):

    class Meta:
        model = Decision

        fields = ['percent_payment', 'hours', 'charge', 'ward']

        labels = {
            'percent_payment': 'Doplata z MOPS w procentach',
            'hours': 'Przyslugujace godziny',
            'charge': 'Stawka godzinowa',
            'ward': 'Podopieczny',
        }


class DecisionForm(forms.ModelForm):

    class Meta:
        model = Decision

        fields = ['percent_payment', 'hours', 'charge']

        labels = {
            'percent_payment': 'Doplata z MOPS w procentach',
            'hours': 'Przyslugujace godziny',
            'charge': 'Stawka godzinowa',
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


class ActivityForm(forms.ModelForm):

    class Meta:
        model = Activity

        fields = ['name', 'description']

        labels = {
            'name': 'Nazwa shorzenia',
            'description': 'Opis',
        }


class ActivityFormCheckboxes(forms.Form):

    activity = forms.ModelMultipleChoiceField(queryset=Activity.objects.all(), widget=forms.CheckboxSelectMultiple(), label='Aktywności')


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
