from finance.views import home, add_charge, account_status,random_example, add_account, send_total, total, register,\
    add_goal, login_view, account_goal_status, profile, logout_view, add_value_goal, edit_profile, edit_account,\
    edit_charge
from django.conf.urls import include, url
from api.views import AccountViewSet, ChargeViewSet,StatisticsView
from rest_framework import routers


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^charges/$', random_example),
    url(r'^charges/(?P<account_id>\d{1,16})/$', account_status, name='status'),
    url(r'^addcharge/(?P<account_id>\d{1,16})/$', add_charge, name='add_charge'),
    url(r'^charges/edit/(?P<account_id>\d{1,16})/(?P<charge_id>\d{1,16})/$', edit_charge, name='edit_charge'),
    url(r'^addgoal/(?P<account_id>\d{1,16})/$', add_goal, name='add_goal'),
    url(r'^addaccount/$', add_account, name='add_account'),
    url(r'^account/edit/(?P<account_id>\d{1,16})$', edit_account, name='edit_account'),
    url(r'^download/total/(?P<account_id>\d{1,16})/$', send_total, name='total_line'),
    url(r'^statistic/total/(?P<account_id>\d{1,16})/$', total, name='total_table'),
    url(r'^profile/edit/$', edit_profile, name='edit_profile'),
    url(r'^register/$', register, name='register'),
    url(r'^login/$', login_view, name='login'),
    url(r'^goals/(?P<account_id>\d{1,16})/$', account_goal_status, name='goals'),
    url(r'^goals/addvalue/(?P<account_id>\d{1,16})/(?P<goal_id>\d{1,16})/$', add_value_goal, name='add_value_goal'),
    url(r'^profile/$', profile, name='profile'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'^api/accounts/(?P<pk>\d{1,16})/$', AccountViewSet.as_view({'get': 'retrieve'})),
    url(r'^api/accounts/create/$', AccountViewSet.as_view({'post': 'create'})),
    url(r'^api/accounts/delete/(?P<pk>\d{1,16})/$', AccountViewSet.as_view({'delete': 'destroy'})),
    url(r'^api/accounts/update/(?P<pk>\d{1,16})/$', AccountViewSet.as_view({'put': 'update'})),

    url(r'^api/charges/(?P<pk>\d{1,16})/$', ChargeViewSet.as_view({'get': 'retrieve'})),
    url(r'^api/charges/create/$', ChargeViewSet.as_view({'post': 'create'})),
    url(r'^api/charges/delete/(?P<pk>\d{1,16})/$', ChargeViewSet.as_view({'delete': 'destroy'})),
    url(r'^api/charges/update/(?P<pk>\d{1,16})/$', ChargeViewSet.as_view({'put': 'update'})),
    url(r'^api/statistics/(?P<pk>\d{1,16})/$', StatisticsView.as_view()),
    ]
