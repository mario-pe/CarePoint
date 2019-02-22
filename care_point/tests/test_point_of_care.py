from django.test import TestCase, Client

from account.models import User
from care_point.forms import Point_of_care_Form
from care_point.models import Manager, Point_of_care, Activity


class PointOfCareTest(TestCase):
    def setUp(self):
        self.client = Client()

        Point_of_care.objects.create(city='city_1').save()
        Point_of_care.objects.create(city='city_2').save()

        self.user = User.objects.create(username='m1', first_name='name_m1', last_name='sure_name_m1', is_manager=True,
                                        is_caregiver=False, password='123456Mp')
        self.user.save()
        point_of_care = Point_of_care.objects.create(city='Bstok')
        point_of_care.save()
        manager = Manager.objects.create(user=self.user, point_of_care=point_of_care)
        manager.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/care_point/points/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/points/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/points/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['points']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/point/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['point'].city, 'city_1')

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/point/5/')
        points = Point_of_care.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(points), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/point/1/delete/')
        points = Point_of_care.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(points), 2)

    def test_should_return_Point_of_care_Form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/point/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), Point_of_care_Form)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/point/add/', {'city': 'city_4'})
        points = Point_of_care.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(points), 4)

    def test_should_return_Point_of_care_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/point/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), Point_of_care_Form)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/point/2/update/', {'city': 'city_up'})
        point = Point_of_care.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/points/")
        self.assertEqual(point.city, 'city_up')

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/point/2/update/', {'citya': 'city_up'})
        point = Point_of_care.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(point.city, 'city_2')
