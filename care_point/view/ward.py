from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from care_point.forms import WardForm, DecisionForm, WorksheetForm, IllnessForm, IllnessFormCheckboxes, \
    ActivityFormCheckboxes, AddressForm, WardUpdateForm, AddressFormWard, DecisionFormWard
from care_point.models import Ward
from care_point.utils import _update_or_create_duties, _prepare_duties_for_ward


@login_required
def ward(request):
    ward = Ward.objects.all()
    return render(request, 'care_point/ward/ward.html', {'ward': ward})


@login_required
def ward_add(request):
    if request.method == 'POST':
        data = request.POST
        ward_form = WardForm(data=data)
        if ward_form.is_valid():
            if _is_ward_not_created(data['name'], data['sname'], data['pesel']):
                info = "Podopieczny o tym imieniu, nazwisku oraz peselu znajduje sie w bazie."
                return render(request, 'care_point/ward/ward_add.html', {'ward_form': ward_form,
                                                                         'info': info})
            else:
                ward_form.save()
        return redirect('care_point:ward')
    else:
        ward_form = WardForm()
        return render(request, 'care_point/ward/ward_add.html', {'ward_form': ward_form })


@login_required
def ward_details(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    decisions = ward.decision_set.all()
    worksheet = ward.worksheet_set.all()
    address = ward.address_set.all()
    illness, activity = _prepare_duties_for_ward(ward)

    return render(request, 'care_point/ward/ward_details.html', {'ward': ward,
                                                                 'decision': decisions,
                                                                 'worksheet': worksheet,
                                                                 'address': address,
                                                                 'illness': illness,
                                                                 'activity': activity, })


@login_required
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


@login_required
def ward_delete(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    ward.delete()
    return redirect('care_point:ward')


@login_required
def new_worksheet_ward(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    ward_address = ward.address_set.first()
    ward_decision = ward.decision_set.order_by('-pk').first()
    if request.method == 'POST':
        form = WorksheetForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward_details', ward_id=ward.id)
    else:
        form = WorksheetForm({'ward': ward, 'address': ward_address, 'decision': ward_decision})
        return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})


@login_required
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


@login_required
def next_decision(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    if request.method == 'POST':
        form = DecisionFormWard(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward_details', ward_id=ward.id)
    else:
        form = DecisionFormWard({'ward': ward})
        return render(request, 'care_point/decision/decision_add.html', {'form': form})


def _is_ward_not_created(name, sname, pesel):
    old_ward = Ward.objects.filter(name=name).filter(sname=sname).filter(pesel=pesel).first()
    if old_ward:
        return True
    else:
        return False
