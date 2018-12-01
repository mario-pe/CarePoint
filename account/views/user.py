from django.shortcuts import redirect

from account.models import User
from account.forms import ManagerSignUpForm
from django.contrib.auth import login
from django.views.generic import CreateView


class ManagerSignUpView(CreateView):
    model = User
    form_class = ManagerSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'manager'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('care_point:managers')