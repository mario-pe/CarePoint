from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *


class ContractAdmin(admin.ModelAdmin):
    list_display = ('genre', 'date_from', 'date_to')


class Point_of_careAdmin(admin.ModelAdmin):
    list_display = ('city',)


class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'sname')


class CaregiverAdmin(admin.ModelAdmin):
    list_display = ('name', 'sname', 'point_of_care')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('city', 'street', 'number', 'zip_code')


class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'sname', 'pesel')


class DecisionAdmin(admin.ModelAdmin):
    list_display = ('percent_payment', 'hours', 'charge', 'ward')


class IllnessAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


class WorksheetAdmin(admin.ModelAdmin):
    list_display = ('genre', 'date', 'hour_from', 'hour_to', 'description')


admin.site.register(Contract, ContractAdmin)
admin.site.register(Point_of_care, Point_of_careAdmin)
admin.site.register(Manager, ManagerAdmin)
admin.site.register(Caregiver, CaregiverAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Decision, DecisionAdmin)
admin.site.register(Illness, IllnessAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Worksheet, WorksheetAdmin)