from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from account.decorators import manager_required
from care_point.forms import ContractForm, WorksheetForm
from care_point.models import Contract, Caregiver
from care_point.view import caregiver


@manager_required
def contract(request):
    contracts = Contract.objects.all()
    return render(request, 'care_point/contract/contract.html', {'contracts': contracts})


@manager_required
def contract_update(request, contract_id):
    c = get_object_or_404(Contract, pk=contract_id)
    form = ContractForm(data=request.POST or None, instance=c)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:contract')
    return render(request, 'care_point/contract/contract_update.html', {'form': form})


@manager_required
def contract_details(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    return render(request, 'care_point/contract/contract_details.html', {'contract': contract})


@manager_required
def contract_delete(request, contract_id):
    contract = get_object_or_404(Contract, pk=contract_id)
    contract.delete()
    return redirect('care_point:contract')


@manager_required
def contract_add(request):
    if request.method == 'POST':
        form = ContractForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:contract')
    else:
        form = ContractForm()
        return render(request, 'care_point/contract/contract_add.html', {'form': form})


@manager_required
def contract_add_caregiver(request):
    if request.method == 'POST':
        form = ContractForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:caregiver')
    else:
        form = ContractForm()
        return render(request, 'care_point/contract/contract_add.html', {'form': form})


@manager_required
def next_contract(request, caregiver_id):
    if request.method == 'POST':
        form = ContractForm(data=request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            caregiver = get_object_or_404(Caregiver, pk=caregiver_id)
            new.save()
            caregiver.contract_set.add(new)
            return redirect('care_point:caregiver_details', caregiver_id=caregiver_id)
        return render(request, 'care_point/contract/contract_add.html', {'form': form})
    else:
        form = ContractForm()
        return render(request, 'care_point/contract/contract_add.html', {'form': form})

#
# @login_required
# def new_worksheet_caregiver(request, caregiver_id):
#     if request.method == 'POST':
#         form = WorksheetForm(data=request.POST)
#         if form.is_valid():
#             new = form.save(commit=False)
#             new.save()
#             caregiver_id_new = new.caregiver.id
#             return redirect('care_point:caregiver')
#         # return render(request, 'care_point/caregiver/caregiver_details.html', {'caregiver_id': caregiver_id})
#     else:
#         form = WorksheetForm()
#         return render(request, 'care_point/worksheet/worksheet_add.html', {'form': form})
