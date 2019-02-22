from care_point.models import WardIllness, WardActivity, Worksheet


def _update_or_create_duties(decision, new_illnesses, new_activites, old_illnesses=None, old_activity=None):
    if not old_illnesses and not old_activity:
        old_illnesses, old_activity = _prepare_duties_for_decisoin(decision)
    ward = decision.ward

    _update_illness(list(new_illnesses), list(old_illnesses), ward, decision)
    _update_activity(list(new_activites), list(old_activity), ward, decision)


def _update_illness(new_illnesses, old_illnesses, ward, decision):
    for new_illness in new_illnesses:
        if new_illness not in old_illnesses:
            ward_illness = WardIllness(ward=ward, illness=new_illness, decision=decision)
            ward_illness.save()
    for old_illness in old_illnesses:
        if old_illness not in new_illnesses:
            ward_activity = WardIllness.objects.filter(ward=ward, illness=old_illness, decision=decision).first()
            ward_activity.delete()


def _update_activity(new_activities, old_activities, ward, decision):
    for new_activity in new_activities:
        if new_activity not in old_activities:
            ward_activity = WardActivity(ward=ward, activity=new_activity, decision=decision)
            ward_activity.save()
    for old_activity in old_activities:
        if old_activity not in new_activities:
            ward_activity = WardActivity.objects.filter(ward=ward, activity=old_activity, decision=decision).first()
            ward_activity.delete()


def _prepare_duties_for_decisoin(decision):
    illnesses = _prepare_illness_from_wrad_activity_for_decision(decision)
    activities = _prepare_activity_from_wrad_activity_for_decision(decision)
    return illnesses, activities


def _prepare_illness_from_wrad_activity_for_decision(decison):
    ward_illness_for_decision = WardIllness.objects.filter(decision=decison).select_related().all()
    illnesses = []
    for ward_illness in ward_illness_for_decision:
        illnesses.append(ward_illness.illness)
    return illnesses


def _prepare_activity_from_wrad_activity_for_decision(decison):
    ward_activity_for_decision = WardActivity.objects.filter(decision=decison).select_related().all()
    activities = []
    for ward_activity in ward_activity_for_decision:
        activities.append(ward_activity.activity)
    return activities


def prepare_duties_for_ward(ward):
    illnesses = __prepare_illness_from_wrad_activity_for_ward(ward)
    activities = __prepare_activity_from_wrad_activity_for_ward(ward)
    return illnesses, activities


def __prepare_illness_from_wrad_activity_for_ward(ward):
    ward_illness_for_decision = WardIllness.objects.filter(ward=ward).select_related().all()
    illnesses = []
    for ward_illness in ward_illness_for_decision:
        illnesses.append(ward_illness.illness)
    illnesses = set(illnesses)
    return illnesses


def __prepare_activity_from_wrad_activity_for_ward(ward):
    ward_activity_for_decision = WardActivity.objects.filter(ward=ward).select_related().all()
    activities = []
    for ward_activity in ward_activity_for_decision:
        activities.append(ward_activity.activity)
    activities = set(activities)
    return activities


def prepare_calender(worksheets, month, object):
    iterator = 1
    calendar = '<div class="col-sm-12 col-md-12"><div class="conteiner-fluid">'
    calendar += '<table id="calendar"><tbody>'
    for i in range(0, 5):
        if iterator % 7 == 1:
            calendar += '<tr class="calendar_tr">'
        for j in range(0, 7):
            for w in worksheets:
                if w.date.month == month:
                    if w.date.day == iterator:
                        if iterator % 7 == 1:
                            calendar += '<tr class="calendar_tr">'
                        calendar += '<td class="calendar_td">' + iterator.__str__() + '<br>'
                        for w_for_day in worksheets:
                            if w_for_day.date.day == iterator:
                                calendar += '<a href="' + '/care_point/worksheet/'+ w_for_day.id.__str__() + '/'  '"> '
                                if object is 'ward':
                                    calendar += w_for_day.caregiver.__str__() +'</a><br>'
                                else:
                                    calendar += w_for_day.ward.__str__() + '</a><br>'
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
    return calendar
