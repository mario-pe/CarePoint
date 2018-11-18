from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from care_point.forms import Point_of_care_Form
from care_point.models import Point_of_care


@login_required
def points(request):
    points = Point_of_care.objects.all()
    return render(request, 'care_point/point_of_care/point_of_care.html', {'points': points})


@login_required
def point_add(request):
    if request.method == 'POST':
        form = Point_of_care_Form(data=request.POST)
        if form.is_valid():
            point = form.save(commit=False)
            point.save()
        return redirect('care_point:points')
    else:
        form = Point_of_care_Form()
        return render(request, 'care_point/point_of_care/point_of_care_add.html', {'form': form})


@login_required
def point_details(request, point_id):
    point = get_object_or_404(Point_of_care, pk=point_id)
    return render(request, 'care_point/point_of_care/point_of_care_details.html', {'point': point})


@login_required
def point_update(request, point_id):
    i = get_object_or_404(Point_of_care, pk=point_id)
    form = Point_of_care_Form(data=request.POST or None, instance=i)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:points')
    return render(request, 'care_point/point_of_care/point_of_care_update.html', {'form': form})


@login_required
def point_delete(request, point_id):
    point = get_object_or_404(Point_of_care, pk=point_id)
    point.delete()
    return redirect('care_point:points')
