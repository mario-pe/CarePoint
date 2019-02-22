from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import manager_required
from care_point.forms import IllnessForm
from care_point.models import Illness


@manager_required
def illness(request):
    illness = Illness.objects.all()
    return render(request, 'care_point/illness/illness.html', {'illness': illness})


@manager_required
def illness_add(request):
    if request.method == 'POST':
        form = IllnessForm(data=request.POST)
        if form.is_valid():
            illness = form.save(commit=False)
            illness.save()
        return redirect('care_point:illness')
    else:
        form = IllnessForm()
        return render(request, 'care_point/illness/illness_add.html', {'form': form})


@manager_required
def illness_details(request, illness_id):
    illness = get_object_or_404(Illness, pk=illness_id)
    return render(request, 'care_point/illness/illness_details.html', {'illness': illness})


@manager_required
def illness_update(request, illness_id):
    i = get_object_or_404(Illness, pk=illness_id)
    form = IllnessForm(data=request.POST or None, instance=i)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:illness')
    return render(request, 'care_point/illness/illness_update.html', {'form': form})


@manager_required
def illness_delete(request, illness_id):
    illness = get_object_or_404(Illness, pk=illness_id)
    illness.delete()
    return redirect('care_point:illness')