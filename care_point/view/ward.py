from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from care_point.forms import WardForm, DecisionForm, WorksheetForm, IllnessForm, IllnessFormCheckboxes, \
    ActivityFormCheckboxes, AddressForm
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
    decision = ward.decision_set.all()
    worksheet = ward.worksheet_set.all()
    address = ward.address_set.all()
    illness, activity = _prepare_duties_for_ward(ward)

    return render(request, 'care_point/ward/ward_details.html', {'ward': ward,
                                                                 'decision': decision,
                                                                 'worksheet': worksheet,
                                                                 'address': address,
                                                                 'illness': illness,
                                                                 'activity': activity, })


@login_required
def ward_update(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    form = WardForm(data=request.POST or None, instance=ward)
    addresses = ward.address_set.all()
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward')
    return render(request, 'care_point/ward/ward_update.html', {'form': form, 'addresses': addresses})


@login_required
def ward_delete(request, ward_id):
    ward = get_object_or_404(Ward, pk=ward_id)
    ward.delete()
    return redirect('care_point:ward')


@login_required
def new_worksheet_ward(request, ward_id):
    if request.method == 'POST':
        form = WorksheetForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:ward')
        # return render(request, 'care_point/caregiver/caregiver_details.html', {'caregiver_id': caregiver_id})
    else:
        form = WorksheetForm()
        return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})


def _is_ward_not_created(name, sname, pesel):
    old_ward = Ward.objects.filter(name=name).filter(sname=sname).filter(pesel=pesel).first()
    if old_ward:
        return True
    else:
        return False
