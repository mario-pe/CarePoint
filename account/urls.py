from django.conf.urls import url
from account.views.user import *
from account.views.caregiver import *
from django.contrib.auth.views import login, logout, logout_then_login


app_name = 'account'

# urlpatterns = [url(r'^$', views.user_login, name='login'),
urlpatterns = [
    # url(r'^login/$', login, name='login'),
    # url(r'^logout/$', logout, name='logout'),
    url(r'^logout/$', logout, {'template_name': 'logged_out.html'}, name='logout'),
    # url(r'^logout-then-login/$', logout_then_login, name='logout_then_login'),
    url(r'^manager_signup/$', ManagerSignUpView.as_view(), name='manager_signup'),
    url(r'^caregiver_signup/$', CargiverSignUpView.as_view(), name='caregiver_signup'),
]