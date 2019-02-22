from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import caregiver_required, manager_required
from care_point.forms import CaregiverForm
from care_point.models import Caregiver
import datetime as idt

from care_point.utils import prepare_calender


@manager_required
def caregiver(request):
    caregivers = Caregiver.objects.all()
    return render(request, 'care_point/caregiver/caregiver.html', {'caregivers': caregivers})


@manager_required
def caregiver_details(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, pk=caregiver_id)
    contract = caregiver.contract_set.all()
    worksheets = list(caregiver.worksheet_set.all())
    current_month = idt.datetime.now().month
    calendar = prepare_calender(worksheets, current_month, 'caregover')

    return render(request, 'care_point/caregiver/caregiver_details.html',
                  {'caregiver': caregiver, 'contract': contract, 'worksheet': worksheets, 'calendar': calendar})


@manager_required
def caregiver_update(request, caregiver_id):
    c = get_object_or_404(Caregiver, pk=caregiver_id)
    form = CaregiverForm(data=request.POST or None, instance=c)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:caregiver')
    return render(request, 'care_point/caregiver/caregiver_update.html', {'form': form})


@manager_required
def caregiver_delete(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, pk=caregiver_id)
    caregiver.delete()
    return redirect('care_point:caregiver')


@caregiver_required
def caregiver_schedule(request):
    caregiver = get_object_or_404(Caregiver, pk=request.user.id)
    contract = caregiver.contract_set.all()
    worksheets = list(caregiver.worksheet_set.all())
    current_month = idt.datetime.now().month
    calendar = prepare_calender(worksheets, current_month, caregiver)
    return render(request, 'care_point/caregiver/caregiver_details.html',
                  {'caregiver': caregiver, 'contract': contract, 'worksheet': worksheets, 'calendar': calendar})




