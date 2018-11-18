from django.shortcuts import render


def index(request):
    info = 'info'
    return render(request, 'care_point/index.html', {'info': info})
