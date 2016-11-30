from finance.views import home,add_charge,account_status,random_example, add_account, send_total, total, register, add_goal
from django.conf.urls import include, url
urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^charges/$', random_example),
    url(r'^charges/(?P<account_id>\d{1,16})/$', account_status, name='status'),
    url(r'^addcharge/(?P<account_id>\d{1,16})/$', add_charge, name='add_charge'),
    url(r'^addgoal/(?P<account_id>\d{1,16})/$', add_goal, name='add_goal'),
    url(r'^addaccount/$', add_account, name='add_account'),
    url(r'^download/total/(?P<account_id>\d{1,16})/$', send_total, name='total_line'),
    url(r'^statistic/total/(?P<account_id>\d{1,16})/$', total, name='total_table'),
    url(r'^register/$', register, name='register')
    ]
