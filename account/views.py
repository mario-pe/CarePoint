from django.http import HttpResponse
from django.shortcuts import render, redirect

from .forms import LoginForm
from django.contrib.auth import authenticate, login


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'],
#                                 password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Uwierzytelnienie zakoczylo sie sukcesem.')
#                 else:
#                     return HttpResponse('Uzytkownik zablokowany')
#             else:
#                 return HttpResponse('Uwierzytelnienie nie powiodlo sie.')
#     else:
#         form = LoginForm()
#     return render(request, 'account/login.html', {'form': form})
#
