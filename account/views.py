from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, UserForm
from django.contrib.auth import authenticate, login
from django.views.generic import View


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakoczylo sie sukcesem.')
                else:
                    return HttpResponse('Uzytkownik zablokowany')
            else:
                return HttpResponse('Uwierzytelnienie nie powiodlo sie.')
    else:
        form = LoginForm()
    # return render(request, 'care_point/index.html', {'form': form})
    return render(request, 'account/login.html', {'form': form})


def singup(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            # login(request, user)
            return redirect('care_point:index')
    else:
        form = UserForm()
    return render(request, 'account/singup.html', {'form': form})

# class UserFormView(View):
#
#     form_class = UserForm
#     template_name = 'account/login.html'
#
#     def get(self,request):
#         form = self.form_class(None)
#         return render(request, self.template_name, {'form': form})
#
#     def post(self,request):
#         form = self.form_class(request.POST)
#
#         if form.is_valid():
#             user = form.save(commit=False)
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user.set_password(password)
#             user.save()