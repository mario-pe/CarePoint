from django.conf.urls import url

from care_point.view.contract import *
from care_point.view.caregiver import *
from care_point.view.illness import *
from care_point.view.activity import *
from care_point.view.ward import *
from care_point.view.decision import *
from care_point.view.address import *
from care_point.view.worksheet import *
from care_point.view.point_of_care import *
from care_point.view.manager import *
from . import views

app_name = 'care_point'

urlpatterns = [

    #index /carepoint
    url(r'^$', views.index, name='index'),

    #OPIEKINOWIE
    url(r'^caregiver/$', caregiver, name='caregiver'),
    url(r'^caregiver/schedule/$', caregiver_schedule, name='caregiver_schedule'),
    url(r'^caregiver/(?P<caregiver_id>[0-9]+)/$', caregiver_details, name='caregiver_details'),
    url(r'^caregiver/(?P<caregiver_id>[0-9]+)/delete/$', caregiver_delete, name='caregiver_delete'),
    url(r'^caregiver/(?P<caregiver_id>[0-9]+)/update/$', caregiver_update, name='caregiver_update'),

    # CONTRACT
    url(r'^contract/$', contract, name='contract'),
    url(r'^contract/add/$', contract_add, name='contract_add'),
    url(r'^contract/caregiver/$', contract_add_caregiver, name='contract_add_caregiver'),
    url(r'^contract/caregiver/(?P<caregiver_id>[0-9]+)/next$', next_contract, name='next_contract'),
    # url(r'^contract/caregiver/(?P<caregiver_id>[0-9]+)/$', new_worksheet_caregiver, name='new_worksheet_caregiver'),
    url(r'^contract/(?P<contract_id>[0-9]+)/$', contract_details, name='contract_details'),
    url(r'^contract/(?P<contract_id>[0-9]+)/delete/$', contract_delete, name='contract_delete'),
    url(r'^contract/(?P<contract_id>[0-9]+)/update/$', contract_update, name='contract_update'),

    # ILLNESS
    url(r'^illness/$', illness, name='illness'),
    url(r'^illness/add/$', illness_add, name='illness_add'),
    url(r'^illness/(?P<illness_id>[0-9]+)/$', illness_details, name='illness_details'),
    url(r'^illness/(?P<illness_id>[0-9]+)/delete/$', illness_delete, name='illness_delete'),
    url(r'^illness/(?P<illness_id>[0-9]+)/update/$', illness_update, name='illness_update'),

    # ACTIVITY
    url(r'^activity/$', activity, name='activity'),
    url(r'^activity/add/$', activity_add, name='activity_add'),
    url(r'^activity/(?P<activity_id>[0-9]+)/$', activity_details, name='activity_details'),
    url(r'^activity/(?P<activity_id>[0-9]+)/delete/$', activity_delete, name='activity_delete'),
    url(r'^activity/(?P<activity_id>[0-9]+)/update/$', activity_update, name='activity_update'),

    #WARD
    url(r'^ward/$', ward, name='ward'),
    url(r'^ward/add/$', ward_add, name='ward_add'),
    url(r'^worksheet/ward/(?P<ward_id>[0-9]+)/$', new_worksheet_ward, name='new_worksheet_ward'),
    url(r'^ward/(?P<ward_id>[0-9]+)/$', ward_details, name='ward_details'),
    # url(r'^ward/(?P<ward_id>[0-9]+)/(?P<success_info>[a-z A-Z]+)/$', ward_details, name='ward_details_info'),
    url(r'^ward/(?P<ward_id>[0-9]+)/delete/$', ward_delete, name='ward_delete'),
    url(r'^ward/(?P<ward_id>[0-9]+)/update/$', ward_update, name='ward_update'),
    url(r'^ward/(?P<ward_id>[0-9]+)/add_address/$', add_address_for_ward, name='add_address_for_ward'),
    url(r'^decision/(?P<ward_id>[0-9]+)/ward$', next_decision, name='next_decision'),

    # #DECYZJE
    url(r'^decision/$', decision, name='decision'),
    url(r'^decision/add/$', decision_add, name='decision_add'),

    url(r'^decision/(?P<decision_id>[0-9]+)/$', decision_details, name='decision_details'),
    url(r'^decision/(?P<decision_id>[0-9]+)/delete/$', decision_delete, name='decision_delete'),
    url(r'^decision/(?P<decision_id>[0-9]+)/update/$', decision_update, name='decision_update'),

    #MANAGER
    url(r'^manager/$', managers, name='managers'),
    # url(r'^manager/add/$', manager_add, name='manager_add'),
    url(r'^manager/(?P<manager_id>[0-9]+)/$', manager_details, name='manager_details'),
    url(r'^manager/(?P<manager_id>[0-9]+)/delete/$', manager_delete, name='manager_delete'),
    url(r'^manager/(?P<manager_id>[0-9]+)/update/$', manager_update, name='manager_update'),

    #ADDRESS
    url(r'^address/$', address, name='address'),
    url(r'^address/add/$', address_add, name='address_add'),
    url(r'^address/(?P<address_id>[0-9]+)/$', address_details, name='address_details'),
    url(r'^address/(?P<address_id>[0-9]+)/delete/$', address_delete, name='address_delete'),
    url(r'^address/(?P<address_id>[0-9]+)/update/$', address_update, name='address_update'),

    # WORKSHEET
    url(r'^worksheet/$', worksheet, name='worksheet'),
    url(r'^worksheet/add/$', worksheet_add, name='worksheet_add'),
    url(r'^worksheet/(?P<worksheet_id>[0-9]+)/$', worksheet_details, name='worksheet_details'),
    url(r'^worksheet/(?P<worksheet_id>[0-9]+)/delete/$', worksheet_delete, name='worksheet_delete'),
    url(r'^worksheet/(?P<worksheet_id>[0-9]+)/update/$', worksheet_update, name='worksheet_update'),

    # POINT OF CARE
    url(r'^points/$', points, name='points'),
    url(r'^point/add/$', point_add, name='point_add'),
    url(r'^point/(?P<point_id>[0-9]+)/$', point_details, name='point_details'),
    url(r'^point/(?P<point_id>[0-9]+)/delete/$', point_delete, name='point_delete'),
    url(r'^point/(?P<point_id>[0-9]+)/update/$', point_update, name='point_update'),
]


