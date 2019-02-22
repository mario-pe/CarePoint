from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import manager_required
from care_point.forms import ActivityForm
from care_point.models import Activity


@manager_required
def activity(request):
    activity = Activity.objects.all()
    return render(request, 'care_point/activity/activity.html', {'activity': activity})


@manager_required
def activity_add(request):
    if request.method == 'POST':
        form = ActivityForm(data=request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.save()
        return redirect('care_point:activity')
    else:
        form = ActivityForm()
        return render(request, 'care_point/activity/activity_add.html', {'form': form})


@manager_required
def activity_details(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    return render(request, 'care_point/activity/activity_details.html', {'activity': activity})


@manager_required
def activity_update(request, activity_id):

    a = get_object_or_404(Activity, pk=activity_id)
    form = ActivityForm(data=request.POST or None, instance=a)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:activity')
    return render(request, 'care_point/activity/activity_update.html', {'form': form})



@manager_required
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id)
    activity.delete()
    return redirect('care_point:activity')