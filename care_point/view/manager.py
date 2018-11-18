from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from care_point.forms import ManagerForm
from care_point.models import Manager


@login_required
def managers(request):
    managers = Manager.objects.all()
    return render(request, 'care_point/manager/manager.html', {'managers': managers})


@login_required
def manager_add(request):
    if request.method == 'POST':
        form = ManagerForm(data=request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.save()
        return redirect('care_point:managers')
    else:
        form = ManagerForm()
        return render(request, 'care_point/manager/manager_add.html', {'form': form})


@login_required
def manager_details(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    return render(request, 'care_point/manager/manager_details.html', {'manager': manager})


@login_required
def manager_update(request, manager_id):
    i = get_object_or_404(Manager, pk=manager_id)
    form = ManagerForm(data=request.POST or None, instance=i)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:managers')
    return render(request, 'care_point/manager/manager_update.html', {'form': form})


@login_required
def manager_delete(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    manager.delete()
    return redirect('care_point:managers')
