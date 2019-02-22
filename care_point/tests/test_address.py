from django.test import TestCase, Client

from account.models import User
from care_point.forms import AddressForm, AddressFormWard
from care_point.models import Manager, Point_of_care, Address, Ward


class AddressTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.ward = Ward.objects.create(first_name='ward_name', last_name='ward_last_name', pesel='12346512123')
        self.ward.save()
        Address.objects.create(city='city_1', street='street_1', number='1', zip_code='11-111', ward=self.ward).save()
        Address.objects.create(city='city_2', street='street_2', number='2', zip_code='22-222', ward=self.ward).save()
        Address.objects.create(city='city_3', street='street_3', number='3', zip_code='22-222', ward=self.ward).save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/address/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/address/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['address']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['address'].city, 'city_1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/5/')
        activites = Address.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(activites), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/1/delete/')
        activites = Address.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(activites), 2)

    def test_should_return_address_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), AddressFormWard)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/address/add/', {'city': 'city_4', 'street': 'street_4', 'number': '44', 'zip_code': '44-111', 'ward': 1})
        adreses = Address.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(adreses), 4)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/address/add/', {'city': 'city_4', 'street': 'street_4', 'number': '44', 'zip_code': '44-111', 'ward': 1})
        adreses = Address.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(adreses), 4)

    def test_should_return_address_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/address/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), AddressFormWard)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/address/2/update/', {'city': 'city_up', 'street': 'street_up', 'number': '66', 'zip_code': '11-111', 'ward': 1})
        updated_address = Address.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/address/")
        self.assertEqual(updated_address.city, 'city_up')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/address/2/update/', {'city': 'city_up', 'street': 'street_up', 'number': '66', 'zip_code': '11-111'})
        updated_address = Address.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_address.city, 'city_2')
