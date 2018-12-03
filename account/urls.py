from django.conf.urls import url
from account.views.user import ManagerSignUpView
from account.views.caregiver import CaregiverSignUpView
from django.contrib.auth.views import login, logout

app_name = 'account'

urlpatterns = [
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout, {'template_name': 'logged_out.html'}, name='logout'),
    url(r'^manager_signup/$', ManagerSignUpView.as_view(), name='manager_signup'),
    url(r'^caregiver_signup/$', CaregiverSignUpView.as_view(), name='caregiver_signup'),
]