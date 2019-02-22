from django.test import TestCase, Client

from account.models import User
from care_point.forms import ActivityForm
from care_point.models import Manager, Point_of_care, Activity


class ActivityTest(TestCase):
    def setUp(self):
        self.client = Client()

        Activity.objects.create(name='activity_1', description='desc_1').save()
        Activity.objects.create(name='activity_2', description='desc_2').save()
        Activity.objects.create(name='activity_3', description='desc_3').save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()

    def test_index(self):
        response = self.client.get('/care_point/')
        self.assertEqual(response.status_code, 200)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/activity/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/activity/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['activity']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['activity'].name, 'activity_1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/5/')
        activites = Activity.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(activites), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/1/delete/')
        activites = Activity.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(activites), 2)

    def test_should_return_activity_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ActivityForm)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/activity/add/', {'name': 'activity_4', 'description': 'desc4'})
        activites = Activity.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(activites), 4)

    def test_should_return_activity_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/activity/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), ActivityForm)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/activity/2/update/', {'name': 'activity_update', 'description': 'desc_update'})
        updated_activity = Activity.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/activity/")
        self.assertEqual(updated_activity.name, 'activity_update')
        self.assertEqual(updated_activity.description, 'desc_update')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/activity/2/update/', {'call': 'activity_update', 'description': 'desc_update'})
        updated_activity = Activity.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(updated_activity.name, 'activity_2')
        self.assertEqual(updated_activity.description, 'desc_2')
