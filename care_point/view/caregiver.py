from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from care_point.forms import CaregiverForm, ContractForm
from care_point.models import Caregiver
import datetime as idt


@login_required
def caregiver(request):
    c = Caregiver.objects.all()
    return render(request, 'care_point/caregiver/caregiver.html', {'caregivers': c})


@login_required
def caregiver_add(request):
    if request.method == 'POST':
        form_caregiver = CaregiverForm(data=request.POST)

        # form_contract.clean_data['data']  : dostep do pola formularza

        form_contract = ContractForm(data=request.POST)

        if form_caregiver.is_valid() and form_contract.is_valid():
            caregiver = form_caregiver.save(commit=False)
            check_caregiver = Caregiver.objects.filter(name=caregiver.name).filter(sname=caregiver.sname).first()
            if check_caregiver != None:
                if caregiver.name == check_caregiver.name and caregiver.sname == check_caregiver.sname:
                    info = "Opiekun o tym imieniu i nazwisku znajduje sie w bazie."
                    form_contract = ContractForm()
                    form_caregiver = CaregiverForm()
                    return render(request, 'care_point/caregiver/caregiver_add.html',
                                  {'form_caregiver': form_caregiver, 'form_contract': form_contract, 'info': info})
            else:
                contract = form_contract.save(commit=False)
                contract.save()
                caregiver.save()
                caregiver.contract_set.add(contract)
        return redirect('care_point:caregiver')
    else:
        form_contract = ContractForm()
        form_caregiver = CaregiverForm()
        # dodawanie wartosci do formularza
        # from = searchTeeamForm({'name': " fc b "})
        return render(request, 'care_point/caregiver/caregiver_add.html',
                      {'form_caregiver': form_caregiver, 'form_contract': form_contract})


@login_required
def caregiver_details(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, pk=caregiver_id)
    contract = caregiver.contract_set.all()
    worksheet = list(caregiver.worksheet_set.all())
    iterator = 1
    month_now = idt.datetime.now().month
    url_str = "care_point:worksheet_details"

    calendar = '<div class="col-sm-12 col-md-12"><div class="conteiner-fluid">'
    calendar += '<table id="calendar"><tbody>'
    for i in range(0, 5):
        if iterator % 7 == 1:
            calendar += '<tr class="calendar_tr">'
        for j in range(0, 7):
            for w in worksheet:
                if w.date.month == month_now:
                    if w.date.day == iterator:
                        if iterator % 7 == 1:
                            calendar += '<tr class="calendar_tr">'
                        calendar += '<td class="calendar_td">' + iterator.__str__() + '<br>'
                        for w_for_day in worksheet:
                            if w_for_day.date.day == iterator:
                                calendar += '<a href="' + '/care_point/worksheet/'+ w_for_day.id.__str__() + '/'  '"> ' + w_for_day.ward.__str__() +'</a><br>'
                        iterator += 1
                        calendar += '</td>'
                        if iterator % 7 == 1:
                            calendar += '</tr>'
            else:
                if iterator < 32:
                    calendar += '<td class="calendar_td">' +iterator.__str__() + '<br></td>'
                    iterator += 1
            if iterator % 7 == 1:
                calendar += '</tr>'

    calendar += '</tbody></table></div></div>'

    return render(request, 'care_point/caregiver/caregiver_details.html',
                  {'caregiver': caregiver, 'contract': contract, 'worksheet': worksheet, 'calendar': calendar})


@login_required
def caregiver_update(request, caregiver_id):
    c = get_object_or_404(Caregiver, pk=caregiver_id)
    form = CaregiverForm(data=request.POST or None, instance=c)
    if request.method == 'POST':
        if form.is_valid():
            new = form.save(commit=False)
            new.save()
        return redirect('care_point:caregiver')
    return render(request, 'care_point/caregiver/caregiver_update.html', {'form': form})


@login_required
def caregiver_delete(request, caregiver_id):
    caregiver = get_object_or_404(Caregiver, pk=caregiver_id)
    caregiver.delete()
    return redirect('care_point:caregiver')