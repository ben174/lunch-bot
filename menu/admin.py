from django.contrib import admin
from menu.models import Menu, Meal, MenuItem, Allergen

admin.site.register([Menu, Meal, MenuItem, Allergen])
