from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import DateDetailView
from menu.models import Menu
import menu.views




urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^parse/$', menu.views.parse, name='parse'),
    url(r'^$', menu.views.week, name='week'),
    url(r'^email/$', menu.views.email, name='email'),
    url(r'^text/(?P<meal>[BLD])$', menu.views.text, name='text'),
    url(r'^submit/$', menu.views.submit, name='submit'),
    url(r'^allergens/$', menu.views.provision_allergens, name='provision_allergens'),
    url(r'^week/$', menu.views.week, name='week'),

    url(r'^menus/$', menu.views.MenuList.as_view()),
    url(r'^subscribe/$', menu.views.subscribe, name='subscribe'),
    url(r'^(?P<year>[0-9]{4})/week/(?P<week>[0-9]+)/$', menu.views.MenuWeekArchiveView.as_view(), name="menu_week"),
    url(r'^(?P<year>[0-9]{4})/(?P<month>[-\w]+)/(?P<day>[0-9]+)/$', menu.views.MenuDayArchiveView.as_view(), name="menu_day"),


]
