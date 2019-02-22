from unittest.mock import Mock

from django.test import TestCase, Client
from datetime import date as date
from datetime import time as time

from account.models import User
from care_point.forms import ActivityForm, WorksheetForm
from care_point.models import Manager, Point_of_care, Activity, Worksheet, Ward, Address, Caregiver, Illness, Decision


class WorksheetTest(TestCase):
    def setUp(self):
        self.client = Client()
        __date_1 = date(2016, 1, 1)
        __date_2 = date(2016, 2, 1)
        __date_3 = date(2016, 3, 1)
        __time1 = time(hour=11, minute=00)
        __time2 = time(hour=12, minute=00)
        self.illness = Illness.objects.create(name='illness_1', description='desc_1')
        self.illness.save()
        self.activity = Activity.objects.create(name='activity_1', description='desc_1')
        self.activity.save()
        self.point_of_care = Point_of_care.objects.create(city='Bstok')
        self.point_of_care.save()
        self.ward = Ward.objects.create(first_name='name_1', last_name='last_1', pesel='123456789')
        self.ward.save()
        self.ward_2 = Ward.objects.create(first_name='name_2', last_name='last_2', pesel='123466789')
        self.ward_2.save()
        self.user_1 = User.objects.create(username='c1', first_name='name_c1', last_name='sure_name_c1', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_1.save()

        self.decision = Decision.objects.create(percent_payment=20.0, hours=20.0, charge=20.0, ward=self.ward)
        self.decision.save()
        self.decision.illness = [self.illness]
        self.decision.activity = [self.activity]

        self.address = Address.objects.create(city='city_1', street='street_1', number='1', zip_code='11-111', ward=self.ward)
        self.address.save()
        self.caregiver_1 = Caregiver.objects.create(user=self.user_1, point_of_care=self.point_of_care)
        self.caregiver_1.save()

        Worksheet.objects.create(genre='umowa', date=__date_1, hour_from=__time1, hour_to=__time2, description='desc_1',
                                 ward=self.ward_2, address=self.address, caregiver=self.caregiver_1, decision=self.decision).save()
        Worksheet.objects.create(genre='umowa', date=__date_2, hour_from=__time1, hour_to=__time2, description='desc_2',
                                 ward=self.ward, address=self.address, caregiver=self.caregiver_1, decision=self.decision).save()
        Worksheet.objects.create(genre='umowa', date=__date_3, hour_from=__time1, hour_to=__time2, description='desc_3',
                                 ward=self.ward, address=self.address, caregiver=self.caregiver_1, decision=self.decision).save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/worksheet/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/worksheet/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['worksheet']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['worksheet'].genre, 'umowa')
        self.assertEqual(response.context['worksheet'].description, 'desc_1')


    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/5/')
        worksheet = Worksheet.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(worksheet), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/1/delete/')
        worksheet = Worksheet.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(worksheet), 2)

    def test_should_return_worksheet_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), WorksheetForm)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/add/',
                                    {'caregiver': 1, 'ward': 1, 'address': 1, 'genre': 'umowa',
                                     'decision': 1, 'date': date(2018, 11, 11), 'hour_from': time(hour=11, minute=00), 'hour_to': time(hour=12, minute=00), 'description': 'desc'})
        worksheet = Worksheet.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(worksheet), 4)

    def test_should_not_add_worksheet_when_caregiver_is_busy(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/add/',
                                    {'caregiver': 1, 'ward': 1, 'address': 1, 'genre': 'umowa',
                                     'decision': 1, 'date': date(2016, 1, 1), 'hour_from': time(hour=11, minute=00), 'hour_to': time(hour=12, minute=00), 'description': 'desc'})
        worksheet = Worksheet.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(worksheet), 3)
        self.assertEqual(response.context['info'], 'W godzinach 11:00:00 - 12:00:00 pracownik name_c1, sure_name_c1 wykonuje inne obowiazki')


    def test_should_not_add_object_when_houre_to_is_before_hour_from(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/add/',
                                    {'caregiver': 1, 'ward': 1, 'address': 1, 'genre': 'umowa',
                                     'decision': 1, 'date': date(2018, 11, 11), 'hour_from': time(hour=11, minute=00), 'hour_to': time(hour=10, minute=00), 'description': 'desc'})
        worksheet = Worksheet.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['info'], 'Nieprawidłowe godziny')

    def test_should_return_worksheet_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/worksheet/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), WorksheetForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/2/update/',
                                    {'caregiver': 1, 'ward': 1, 'address': 1, 'genre': 'zlecenie',
                                     'decision': 1, 'date': date(2018, 11, 11), 'hour_from': time(hour=11, minute=00),
                                     'hour_to': time(hour=12, minute=00), 'description': 'desc_update'})
        updated_worksheet = Worksheet.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/worksheet/")
        self.assertEqual(updated_worksheet.genre, 'zlecenie')
        self.assertEqual(updated_worksheet.description, 'desc_update')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/worksheet/2/update/',
                                    {'caregiver': 7, 'ward': 1, 'address': 1, 'genre': 'zlecenie',
                                     'decision': 1, 'date': date(2018, 11, 11), 'hour_from': time(hour=11, minute=00),
                                     'hour_to': time(hour=12, minute=00), 'description': 'desc_update'})
        updated_worksheet = Worksheet.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_worksheet.genre, 'umowa')
        self.assertEqual(updated_worksheet.description, 'desc_2')
