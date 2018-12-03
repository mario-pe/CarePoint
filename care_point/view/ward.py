from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from care_point.forms import WardForm, DecisionForm, AddressForm, WorksheetForm, IllnessForm
from care_point.models import Ward
from care_point.utils import _update_or_create_duties, _prepare_duties_for_ward


@login_required
def ward(request):
    ward = Ward.objects.all()
    return render(request, 'care_point/ward/ward.html', {'ward': ward})


@login_required
def ward_add(request):
    if request.method == 'POST':
        form_ward = WardForm(data=request.POST)
        form_decision = DecisionForm(data=request.POST)
        form_address = AddressForm(data=request.POST)
        if form_ward.is_valid() and form_decision.is_valid() and form_address.is_valid():
            ward = form_ward.save(commit=False)
            if _is_ward_created:
                info = "Podopieczny o tym imieniu, nazwisku oraz peselu znajduje sie w bazie."
                form_ward = WardForm()
                form_decision = DecisionForm()
                form_address = AddressForm()
                return render(request, 'care_point/ward/ward_add.html', {'form_ward': form_ward,
                                                                         'form_decision': form_decision,
                                                                         'form_address': form_address,
                                                                         'info': info})
            else:
                decision = form_decision.save(commit=False)
                address = form_address.save(commit=False)
                ward.save()
                decision.save()

                address.save()
                ward.decision_set.add(decision)
                ward.address_set.add(address)

                illnesses = form_decision.cleaned_data['illness']
                activites = form_decision.cleaned_data['activity']
                _update_or_create_duties(decision, illnesses, activites)

        return redirect('care_point:ward')
    else:
        form_ward = WardForm()
        form_decision = DecisionForm()
        form_address = AddressForm()
        return render(request, 'care_point/ward/ward_add.html', {'form_ward': form_ward,
                                                                 'form_decision': form_decision,
                                                                 'form_address': form_address, })


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


def _is_ward_created(new_ward):
    old_ward = Ward.objects.filter(name=new_ward.name).filter(sname=new_ward.sname).filter(pesel=new_ward.pesel).first()
    if old_ward:
        return True
    else:
        return False
