from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from account.decorators import manager_required
from care_point.forms import WardForm, WorksheetForm, IllnessFormCheckboxes, \
    ActivityFormCheckboxes, WardUpdateForm, AddressFormWard, DecisionFormWard
from care_point.models import Ward
from care_point.utils import _update_or_create_duties, prepare_duties_for_ward, prepare_calender
from care_point.view.worksheet import _add_multiple_worksheets
import datetime as idt


@manager_required
def ward(request):
    ward = Ward.objects.all()
    return render(request, 'care_point/ward/ward.html', {'ward': ward})


@manager_required
def ward_add(request):
    if request.method == 'POST':
        data = request.POST
        ward_form = WardForm(data=data)
        if ward_form.is_valid():
            if _is_ward_not_created(data['first_name'], data['last_name'], data['pesel']):
                info = "Podopieczny o tym imieniu, nazwisku oraz peselu znajduje sie w bazie."
                return render(request, 'care_point/ward/ward_add.html', {'ward_form': ward_form,
                                                                         'info': info})
            else:
                ward_form.save()
        return redirect('care_point:ward')
    else:
        ward_form = WardForm()
        return render(request, 'care_point/ward/ward_add.html', {'ward_form': ward_form })


@manager_required
def ward_details(request, ward_id, success_info=None):
    ward = get_object_or_404(Ward, pk=ward_id)
    decisions = ward.decision_set.all()
    worksheet = ward.worksheet_set.all()
    address = ward.address_set.all()
    illness, activity = prepare_duties_for_ward(ward)
    current_month = idt.datetime.now().month
    calendar = prepare_calender(worksheet, current_month, 'ward')

    return render(request, 'care_point/ward/ward_details.html', {'ward': ward,
                                                                 'decision': decisions,
                                                                 'worksheet': worksheet,
                                                                 'address': address,
                                                                 'illness': illness,
                                                                 'activity': activity,
                                                                 'success_info': success_info,
                                                                 'calendar': calendar})


@manager_required
def ward_update(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    form = WardUpdateForm(data=request.POST or None, instance=ward)
    addresses = ward.address_set.all()
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward')
    return render(request, 'care_point/ward/ward_update.html', {'form': form, 'addresses': addresses, 'ward': ward})


@manager_required
def ward_delete(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    ward.delete()
    return redirect('care_point:ward')


@manager_required
def new_worksheet_ward(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    ward_address = ward.address_set.order_by('-pk').first()
    ward_decision = ward.decision_set.order_by('-pk').first()
    if request.method == 'POST':
        form = WorksheetForm(data=request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            if quantity and quantity > 1:
                return _add_multiple_worksheets(request, form, quantity)
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward_details', ward_id=ward.id)
    else:
        form = WorksheetForm(initial={'ward': ward, 'address': ward_address, 'decision': ward_decision})
        return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})


@manager_required
def add_address_for_ward(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    if request.method == 'POST':
        form = AddressFormWard(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward_details', ward_id=ward.id)
    else:
        form = AddressFormWard({'ward': ward})
        return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})


@manager_required
def next_decision(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    if request.method == 'POST':
        decision_form = DecisionFormWard(data=request.POST)
        illness_form = IllnessFormCheckboxes(data=request.POST)
        activity_form = ActivityFormCheckboxes(data=request.POST)
        if decision_form.is_valid() and illness_form.is_valid() and activity_form.is_valid():
            decisoin = decision_form.save(commit=False)
            decisoin.save()
            new_decision = decision_form.instance
            illnesses = illness_form.cleaned_data['illness']
            activities = activity_form.cleaned_data['activity']
            _update_or_create_duties(decision=new_decision, new_illnesses=illnesses, new_activites=activities)
            return redirect(reverse('care_point:ward_details', kwargs={'ward_id': ward.id}))
        else:
            return render(request, 'care_point/decision/decision_add.html', {'form': decision_form,
                                                                             'illness_form': illness_form,
                                                                             'activity_form': activity_form,
                                                                             'info': 'Dodanie decyzji nie powiodło sie'})

    else:
        decision_form = DecisionFormWard(initial={'ward': ward})
        illness_form = IllnessFormCheckboxes()
        activity_form = ActivityFormCheckboxes()
        return render(request, 'care_point/decision/decision_add.html', {'form': decision_form,
                                                                         'illness_form': illness_form,
                                                                         'activity_form': activity_form})


def _is_ward_not_created(first_name, last_name, pesel):
    old_ward = Ward.objects.filter(first_name=first_name).filter(last_name=last_name).filter(pesel=pesel).first()
    if old_ward:
        return True
    else:
        return False
