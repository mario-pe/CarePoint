from account.models import User
from account.forms import CaregiverSignUpForm
from django.contrib.auth import login
from django.views.generic import CreateView
from django.shortcuts import render, redirect


class CaregiverSignUpView(CreateView):
    model = User
    form_class = CaregiverSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'caregiver'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('care_point:caregiver')
