from django.conf.urls import include, url
from django.contrib import admin
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
    url(r'^week/(?P<year>[0-9]{4})-(?P<month>[0-9]{2})-(?P<day>[0-9]+)/$', menu.views.week, name='week'),
]
