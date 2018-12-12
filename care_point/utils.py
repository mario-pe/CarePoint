import datetime as idt

from care_point.models import WardIllness, WardActivity


def check_available(worksheets, new_worksheet):
    new_time_from = idt.datetime.combine(idt.date(1, 1, 1), new_worksheet.hour_from)
    new_time_to = idt.datetime.combine(idt.date(1, 1, 1), new_worksheet.hour_to)
    compare_time = idt.timedelta(0, 0, 0)
    is_free = True
    if len(worksheets) > 0:
        for i in worksheets:
            i_time_from = idt.datetime.combine(idt.date(1, 1, 1), i.hour_from)
            i_time_to = idt.datetime.combine(idt.date(1, 1, 1), i.hour_to)
            if i_time_from - new_time_from < compare_time:
                if i_time_to - new_time_from > compare_time or i_time_to - new_time_to > compare_time:
                    is_free = False
            elif i_time_from - new_time_from > compare_time:
                if i_time_from - new_time_to < compare_time or i_time_to - new_time_to < compare_time:
                    is_free = False
            elif new_time_from - new_time_to >= compare_time:
                is_free = False
            else:
                is_free = False
    return is_free

# def _processing_duties(decision, new_illnesses, new_activites, old_illnesses=None, old_activity=None):
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


def _prepare_duties_for_ward(ward):
    illnesses = _prepare_illness_from_wrad_activity_for_ward(ward)
    activities = _prepare_activity_from_wrad_activity_for_ward(ward)
    return illnesses, activities


def _prepare_illness_from_wrad_activity_for_ward(ward):
    ward_illness_for_decision = WardIllness.objects.filter(ward=ward).select_related().all()
    illnesses = []
    for ward_illness in ward_illness_for_decision:
        illnesses.append(ward_illness.illness)
    illnesses = set(illnesses)
    return illnesses


def _prepare_activity_from_wrad_activity_for_ward(ward):
    ward_activity_for_decision = WardActivity.objects.filter(ward=ward).select_related().all()
    activities = []
    for ward_activity in ward_activity_for_decision:
        activities.append(ward_activity.activity)
    activities = set(activities)
    return activities

