from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import manager_required
from account.forms import User, UpdateUserForm
from care_point.forms import UpdateManagerForm
from care_point.models import Manager

@manager_required
def managers(request):
    managers = Manager.objects.all()
    return render(request, 'care_point/manager/manager.html', {'managers': managers})


@manager_required
def manager_details(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    return render(request, 'care_point/manager/manager_details.html', {'manager': manager})


@manager_required
def manager_update(request, manager_id):
    manager = get_object_or_404(Manager, pk=manager_id)
    user = get_object_or_404(User, pk=manager_id)
    manager_form = UpdateManagerForm(data=request.POST or None, instance=manager)
    user_form = UpdateUserForm(data=request.POST or None, instance=user)
    if request.method == 'POST':
        if manager_form.is_valid() and user_form.is_valid():
            manager = manager_form.save(commit=False)
            user = user_form.save(commit=False)
            manager.save()
            user.save()
        return redirect('care_point:managers')
    return render(request, 'care_point/manager/manager_update.html',
                  {'manager_form': manager_form, 'user_form': user_form})


@manager_required
def manager_delete(request, manager_id):
    Manager.objects.get(pk=manager_id).delete()
    User.objects.get(pk=manager_id).delete()
    return redirect('care_point:managers')
