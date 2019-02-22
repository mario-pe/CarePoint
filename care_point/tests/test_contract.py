from django.test import TestCase, Client
from datetime import date as date

from account.models import User
from care_point.forms import ActivityForm, ContractForm
from care_point.models import Manager, Point_of_care, Contract, Caregiver


class ActivityTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_caregiver = User.objects.create(username='c1', first_name='name_c1', last_name='sure_name_c1', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_caregiver.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        self.caregiver = Caregiver.objects.create(user=self.user_caregiver, point_of_care=point_of_care)

        Contract.objects.create(genre='umowa', date_from=date(2016, 1, 1), date_to=date(2016, 2, 1), caregiver=self.caregiver).save()
        Contract.objects.create(genre='zlecenie', date_from=date(2017, 1, 1), date_to=date(2017, 2, 1), caregiver=self.caregiver).save()
        Contract.objects.create(genre='zlecenie', date_from=date(2018, 1, 1), date_to=date(2018, 2, 1), caregiver=self.caregiver).save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()


    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/contract/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/contract/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['contracts']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['contract'].genre, 'umowa')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/5/')
        activites = Contract.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(activites), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/1/delete/')
        activites = Contract.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(activites), 2)

    def test_should_return_contract_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ContractForm)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/add/', {'genre': 'zlecenie', 'date_from': date(2017, 1, 1), 'date_to': date(2017, 2, 1), 'caregiver': 1})
        contracts = Contract.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(contracts), 4)

    def test_should_return_contract_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ContractForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/2/update/',
                                    {'genre': 'umowa', 'date_from': date(2017, 1, 1), 'date_to': date(2017, 2, 1),
                                     'caregiver': 1})
        updated_contract = Contract.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/contract/")
        self.assertEqual(updated_contract.genre, 'umowa')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/add/',
                                   {'genre': 'umowa', 'date_from': date(2017, 1, 1), 'date_to': date(2017, 2, 1),
                                    'caregiver': 2})
        updated_contract = Contract.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_contract.genre, 'zlecenie')

    def test_should_return_contract_form_for_caregiver(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/caregiver/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ContractForm)

    def test_should_add_one_contract_for_caregiver(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/caregiver/', {'genre': 'zlecenie', 'date_from': date(2017, 1, 1), 'date_to': date(2017, 2, 1), 'caregiver': 1})
        contracts = Contract.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(contracts), 4)

    def test_should_return_contract_form_for_next_caregiver_contract(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/contract/caregiver/1/next')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ContractForm)

    def test_should_add_one_contract_for_next_caregiver_contract(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/caregiver/1/next', {'genre': 'zlecenie', 'date_from': date(2017, 1, 1), 'date_to': date(2017, 2, 1), 'caregiver': 1})
        contracts = Contract.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(contracts), 4)

    def test_should_add_one_contract_for_next_caregiver_contract_if_not_valid(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/contract/caregiver/1/next', {'genre': 'zlecenie', 'date_from': date(2017, 1, 1), 'date_to': date(2016, 1, 1), 'caregiver': 1})
        contracts = Contract.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(contracts), 3)