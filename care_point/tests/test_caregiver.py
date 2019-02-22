from django.test import TestCase, Client

from account.models import User
from care_point.forms import Point_of_care_Form, CaregiverForm
from care_point.models import Manager, Point_of_care, Activity, Caregiver


class CaregiverTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.point_of_care = Point_of_care.objects.create(city='Bstok')
        self.point_of_care.save()
        self.point_of_care_2 = Point_of_care.objects.create(city='Suwalki')
        self.point_of_care_2.save()
        self.user_1 = User.objects.create(username='c1', first_name='name_c1', last_name='sure_name_c1', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_2 = User.objects.create(username='c2', first_name='name_c2', last_name='sure_name_c2', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_3 = User.objects.create(username='c3', first_name='name_c3', last_name='sure_name_c3', is_manager=False,
                                        is_caregiver=True, password='123456Mp')
        self.user_1.save()
        self.user_2.save()
        self.user_3.save()

        self.caregiver_1 = Caregiver.objects.create(user=self.user_1, point_of_care=self.point_of_care)
        caregiver_2 = Caregiver.objects.create(user=self.user_2, point_of_care=self.point_of_care)
        caregiver_3 = Caregiver.objects.create(user=self.user_3, point_of_care=self.point_of_care)
        self.caregiver_1.save()
        caregiver_2.save()
        caregiver_3.save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()

        manager = Manager.objects.create(user=self.user, point_of_care=self.point_of_care)
        manager.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/caregiver/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/caregiver/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['caregivers']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['caregiver'].user.first_name, 'name_c1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/5/')
        caregiver = Caregiver.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(caregiver), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/1/delete/')
        caregiver = Caregiver.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(caregiver), 2)

    def test_should_return_caregiver_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), CaregiverForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/caregiver/2/update/', {'user': self.user_2, 'first_name': 'adad', 'last_name': 'asd', 'point_of_care': 2})
        caregiver_up = Caregiver.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/caregiver/")
        self.assertEqual(caregiver_up.point_of_care, self.point_of_care_2)

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/caregiver/2/update/', {'user': self.user_2, 'first_name': 'adad', 'last_name': 'asd', 'point_of_care': 3})
        caregiver_up = Caregiver.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(caregiver_up.point_of_care, self.point_of_care)

    def test_should_return_caregiver_schedule_if_user_is_caregiver(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/caregiver/schedule/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['caregiver'], self.caregiver_1)

    def test_should_redirect_if_user_is_manager(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/caregiver/schedule/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/account/login/?next=/care_point/caregiver/schedule/")