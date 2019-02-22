from unittest.mock import Mock
from datetime import date as date
from datetime import time

from django.test import TestCase, Client

from account.models import User
from care_point.forms import ActivityForm, WardForm, WardUpdateForm, WorksheetForm, AddressFormWard, DecisionFormWard
from care_point.models import Manager, Point_of_care, Activity, Ward, Illness, Caregiver, Address, Decision, Worksheet


class WardTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_caregiver = User.objects.create(username='c1', first_name='name_c1', last_name='sure_name_c1', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_caregiver.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        self.caregiver = Caregiver.objects.create(user=self.user_caregiver, point_of_care=point_of_care)
        self.ward = Ward.objects.create(first_name='name_1', last_name='last_1', pesel='123456789')
        self.ward.save()
        Ward.objects.create(first_name='name_2', last_name='last_2', pesel='123456734').save()
        Ward.objects.create(first_name='name_3', last_name='last_3', pesel='123456785').save()

        self.address = Address.objects.create(city='city_1', street='street_1', number='1', zip_code='11-111', ward=self.ward)
        self.address.save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()

        self.decision = Mock()

        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()
        self.illness = Illness.objects.create(name='illness_1', description='desc_1')
        self.illness.save()
        self.activity = Activity.objects.create(name='activity_1', description='desc_1')
        self.activity.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/ward/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/ward/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['ward']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['ward'].first_name, 'name_1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/5/')
        wards = Ward.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(wards), 3)

    def test_should_delete_one_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/1/delete/')
        wards = Ward.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(wards), 2)

    def test_should_return_ward_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['ward_form']), WardForm)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/ward/add/',
                                    {'first_name': 'name_4', 'last_name': 'last_4', 'pesel': '12345432',
                                     'city': 'city_4', 'street': 'street_4', 'home_number': '5', 'zip_code': '12-120',
                                     'percent_payment': 20.0, 'hours': 20.0, 'charge': 20.0, 'illness': 1,
                                     'activity': 1})
        wards = Ward.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(wards), 4)

    def test_should_not_add_one_ward_whan_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/ward/add/',
                                    {'first_name': 'name_1', 'last_name': 'last_1', 'pesel': '123456789',
                                     'city': 'city_4', 'street': 'street_4', 'home_number': '5', 'zip_code': '12-120',
                                     'percent_payment': 20.0, 'hours': 20.0, 'charge': 20.0, 'illness': 1,
                                     'activity': 1})
        wards = Ward.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(wards), 3)

    def test_should_return_activity_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), WardUpdateForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/ward/2/update/',
                                    {'first_name': 'name_up', 'last_name': 'last_up', 'pesel': '123456734'})
        updated_ward = Ward.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/ward/")
        self.assertEqual(updated_ward.first_name, 'name_up')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/ward/2/update/',
                                    {'first_name': 'name_up', 'last_name': 'last_up', 'pesel': '1234567asdasda34'})
        updated_ward = Ward.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_ward.first_name, 'name_2')

    def test_should_return_worksheet_form_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/ward/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), WorksheetForm)

    def test_should_add_worksheet_for_ward(self):
        __date = date(2016, 1, 1)
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/ward/1/',
                                    {'caregiver': 1, 'ward': 1, 'address': 1, 'genre': 'umowa',
                                     'decision': self.decision, 'date': __date, 'hour_from': time(hour=11, minute=00), 'hour_to': time(hour=12, minute=00), 'description': 'desc'})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Worksheet.objects.all()), 1)

    def test_should_return_AddressFormWard_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/ward/1/add_address/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), AddressFormWard)

    def test_should_add_address_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/ward/1/add_address/', {'city': 'city_1', 'street': 'street_1', 'number': '1', 'zip_code': '11-111', 'ward': 1})

        self.assertEqual(response.status_code, 302)

    def test_should_return_DecisionFormWard_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/1/ward')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), DecisionFormWard)

    def test_should_add_decision_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/decision/1/ward', {'activity': 1, 'illness': 1, 'percent_payment': 20.0, 'hours': 20.0, 'charge': 20.0, 'ward': 1})

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(Decision.objects.all()), 1)

    def test_should_not_add_decision_for_ward(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/decision/1/ward', {'activity': 1, 'illness': 123, 'percent_payment': 20.0, 'hours': 20.0, 'charge': 20.0, 'ward': 1})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Decision.objects.all()), 0)

