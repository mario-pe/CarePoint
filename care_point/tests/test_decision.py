from django.test import TestCase, Client

from account.models import User
from care_point.forms import Point_of_care_Form, DecisionFormWard
from care_point.models import Manager, Point_of_care, Activity, Illness, Decision, Ward


class DecisionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.illness = Illness.objects.create(name='illness_1', description='desc_1')
        self.illness.save()
        self.activity = Activity.objects.create(name='activity_1', description='desc_1')
        self.activity.save()
        self.ward = Ward.objects.create(first_name='name_1', last_name='last_1', pesel='123456789')
        self.ward.save()
        self.ward_2 = Ward.objects.create(first_name='name_2', last_name='last_2', pesel='123456734')
        self.ward_2.save()
        self.ward_3 = Ward.objects.create(first_name='name_3', last_name='last_3', pesel='123456785')
        self.ward_3.save()
        self.decision_1 = Decision.objects.create(percent_payment=10.0, hours=10.0, charge=10.0, ward=self.ward)
        self.decision_2 = Decision.objects.create(percent_payment=20.0, hours=20.0, charge=20.0, ward=self.ward_2)
        self.decision_3 = Decision.objects.create(percent_payment=30.0, hours=30.0, charge=20.0, ward=self.ward_3)
        self.decision_1.save()
        self.decision_1.illness = [self.illness]
        self.decision_1.activity = [self.activity]
        self.decision_2.save()
        self.decision_2.illness = [self.illness]
        self.decision_2.activity = [self.activity]
        self.decision_3.save()
        self.decision_3.illness = [self.illness]
        self.decision_3.activity = [self.activity]

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
        response = self.client.get('/care_point/decision/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/account/login/?next=/care_point/decision/')

    def test_should_return_all_objects_from_DB(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['decision']), 3)

    def test_should_return_details_of_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/1/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['decision'].percent_payment, 10.0)

    def test_should_return_status_code_404_if_object_not_exist(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/5/')
        decision = Decision.objects.all()

        self.assertEqual(response.status_code, 404)
        self.assertEqual(len(decision), 3)

    def test_should_delete_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/1/delete/')
        decision = Decision.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(decision), 2)

    def test_should_return_Decision_Form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/add/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), DecisionFormWard)

    def test_should_add_one_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/decision/add/', {'activity': 1, 'illness': 1, 'percent_payment': 20.0, 'hours': 20.0, 'charge': 20.0, 'ward': 1})
        decision = Decision.objects.all()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(decision), 4)

    def test_should_return_decision_update_form(self):
        self.client.force_login(user=self.user)
        response = self.client.get('/care_point/decision/2/update/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response.context['form']), DecisionFormWard)

    def test_should_update_object(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/decision/2/update/', {'activity': 1, 'illness': 1, 'percent_payment': 50.0, 'hours': 20.0, 'charge': 20.0, 'ward': 1})
        decision = Decision.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/care_point/decision/")
        self.assertEqual(decision.percent_payment, 50.0)

    def test_should_not_update_object_when_parameter_is_wrong(self):
        self.client.force_login(user=self.user)
        response = self.client.post('/care_point/decision/2/update/', {'activity': 100, 'illness': 1, 'percent_payment': 50.0, 'hours': 20.0, 'charge': 20.0, 'ward': 1})
        decision = Decision.objects.filter(pk=2).first()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(decision.percent_payment, 20.0)
