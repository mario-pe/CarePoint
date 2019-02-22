from django.test import TestCase, Client

from account.models import User
from care_point.forms import IllnessForm
from care_point.models import Illness, Manager, Point_of_care


class IllnessTest(TestCase):
    def setUp(self):
        self.client = Client()

        Illness.objects.create(name='illness_1', description='desc_1').save()
        Illness.objects.create(name='illness_2', description='desc_2').save()
        Illness.objects.create(name='illness_3', description='desc_3').save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/illness/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/illness/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['illness']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['illness'].name, 'illness_1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/5/')
        illnesses = Illness.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(illnesses), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/1/delete/')
        illnesses = Illness.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(illnesses), 2)

    def test_should_return_illness_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), IllnessForm)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/illness/add/', {'name': 'illness_4', 'description': 'desc4'})
        illnesses = Illness.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(illnesses), 4)

    def test_should_return_illness_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/illness/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), IllnessForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/illness/2/update/', {'name': 'illness_update', 'description': 'desc_update'})
        updated_illness = Illness.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/illness/")
        self.assertEqual(updated_illness.name, 'illness_update')
        self.assertEqual(updated_illness.description, 'desc_update')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/illness/2/update/', {'call': 'illness_update', 'description': 'desc_update'})
        updated_illness = Illness.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_illness.name, 'illness_2')
        self.assertEqual(updated_illness.description, 'desc_2')
