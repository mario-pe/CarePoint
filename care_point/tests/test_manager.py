from django.test import TestCase, Client

from account.models import User
from care_point.forms import ActivityForm, UpdateManagerForm
from care_point.models import Manager, Point_of_care, Activity


class ActivityTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.user_1 = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user_2 = User.objects.create(username='m2', first_name='name_m2', last_name='sure_name_m2', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user_3 = User.objects.create(username='m3', first_name='name_m3', last_name='sure_name_m3', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user_1.save()
        self.user_2.save()
        self.user_3.save()
        self.point_of_care = Point_of_care.objects.create(city='Bstok')
        self.point_of_care_2 = Point_of_care.objects.create(city='Suwalki')
        self.point_of_care.save()
        self.point_of_care_2.save()
        manager_1 = Manager.objects.create(user=self.user_1, point_of_care=self.point_of_care)
        manager_2 = Manager.objects.create(user=self.user_2, point_of_care=self.point_of_care)
        manager_3 = Manager.objects.create(user=self.user_3, point_of_care=self.point_of_care)
        manager_1.save()
        manager_2.save()
        manager_3.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/manager/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/manager/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/manager/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['managers']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/manager/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['manager'].user.first_name, 'name_m1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/manager/5/')
        managers = Manager.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(managers), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/manager/1/delete/')
        managers = Manager.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(managers), 2)

    def test_should_return_manager_update_form(self):
        self.client.force_login(user=self.user_1)
        response = self.client.get('/care_point/manager/2/update/')

        self.assertEqual(response.status_code, 200)

    def test_should_update_object(self):
        self.client.force_login(user=self.user_1)
        response = self.client.post('/care_point/manager/2/update/', {'user': self.user_2, 'first_name': 'adad', 'last_name': 'asd', 'point_of_care': 2})
        updated_manager = Manager.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/manager/")
        self.assertEqual(updated_manager.point_of_care, self.point_of_care_2)
