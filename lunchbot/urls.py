from django.conf.urls import include, url
from django.contrib import admin
import menu.views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^parse/$', menu.views.parse, name='parse'),
    url(r'^$', menu.views.week, name='week'),
    url(r'^email/$', menu.views.email, name='email'),
]
