from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import manager_required
from care_point.forms import WorksheetForm
from care_point.models import Worksheet, Decision
from care_point.utils import check_available, _prepare_duties_for_decisoin


@manager_required
@login_required
def worksheet(request):
    worksheet = Worksheet.objects.all()
    return render(request, 'care_point/worksheet/worksheet.html', {'worksheet': worksheet})


@login_required
def worksheet_add(request):
    if request.method == 'POST':
        form = WorksheetForm(data=request.POST)
        if form.is_valid():
            new_worksheet = form.save(commit=False)
            caregiver_worksheet_at_date = Worksheet.objects.filter(caregiver=new_worksheet.caregiver).filter(date=new_worksheet.date)
            ward_worksheet_at_date = Worksheet.objects.filter(ward=new_worksheet.ward).filter(date=new_worksheet.date)
            is_caregiver_free = check_available(caregiver_worksheet_at_date, new_worksheet)
            is_ward_free = check_available(ward_worksheet_at_date, new_worksheet)
            if is_caregiver_free and is_ward_free:
                new_worksheet.save()
                return redirect('care_point:worksheet')
            elif not is_caregiver_free:
                info = "W godzinach " + new_worksheet.hour_from.__str__() + " - " + new_worksheet.hour_to.__str__() + " pracownik " + new_worksheet.caregiver.__str__() + " wykonuje inne obowiazki"
                form = WorksheetForm(data=request.POST, instance=new_worksheet)
                return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form, "info": info})
            elif not is_ward_free:
                info = "W godzinach " + new_worksheet.hour_from.__str__() + " - " + new_worksheet.hour_to.__str__() + " podopieczny " + new_worksheet.ward.__str__() + " ma inna wizyte"
                form = WorksheetForm(data=request.POST, instance=new_worksheet)
                return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form, "info": info})
    else:
        form = WorksheetForm()
        return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})


@login_required
def worksheet_details(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_id)
    decision = Decision.objects.filter(pk=worksheet.decision_id).first()
    illnesses, activities = _prepare_duties_for_decisoin(decision)
    return render(request, 'care_point/worksheet/worksheet_details.html', {'worksheet': worksheet,
                                                                           'illnesses': illnesses,
                                                                           'activities': activities})


@login_required
def worksheet_update(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_id)
    form = WorksheetForm(data=request.POST or None, instance=worksheet)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:worksheet')
    return render(request, 'care_point/worksheet/worksheet_update.html', {'form': form})


@login_required
def worksheet_delete(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_id)
    worksheet.delete()
    return redirect('care_point:worksheet')
