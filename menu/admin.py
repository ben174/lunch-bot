from django.contrib import admin
from menu.models import Menu, Meal, MenuItem

admin.site.register([Menu, Meal, MenuItem])
