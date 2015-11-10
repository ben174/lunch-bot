import datetime
import logging
from django.http import HttpResponse
from django.shortcuts import render
from util.menu_parser import parse_menu_text
from menu.models import Menu, MenuItem


def parse(request):
    if request.method == 'POST':
        menu_text = request.POST.get('menu-text', None)
        menus = parse_menu_text(menu_text)
        print menus

    return render(request, 'parse.html', {})


def email(request):
    today = datetime.date.today()
    if not Menu.objects.filter(date=today).exists():
        message = "No menu exists for today."
        logging.warning(message)
        return HttpResponse(message)
    try:
        lunch_menu = Menu.objects.get(date=today, menu_type='L')
    except Menu.DoesNotExist:
        message = "Lunch menu does not exist for today."
        logging.warning(message)
        return HttpResponse(message)
    dinner_menu = None
    try:
        dinner_menu = Menu.objects.get(date=today, menu_type='D')
    except Menu.DoesNotExist:
        message = "Dinner menu does not exist for today."
        logging.warning(message)

    return render(request, 'menu_email.html', { 'date': today, 'lunch_menu': lunch_menu, 'dinner_menu': dinner_menu })

