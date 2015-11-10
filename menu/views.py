import datetime
from django.shortcuts import render, get_object_or_404
from util.menu_parser import parse_menu_text, menu_entry_to_db
from menu.models import Menu


def home(request):
    return parse(request)


def parse(request):
    if request.method == 'POST':
        menu_text = request.POST.get('menu-text', None)
        entries = parse_menu_text(menu_text)
        menus = []
        for entry in entries:
            menu = menu_entry_to_db(entry)
            if menu not in menus:
                menus.append(menu)
        return menu_list(request, menus)
    return render(request, 'parse.html', {})


def email(request):
    today = datetime.date.today()
    menu = get_object_or_404(Menu, date=today)
    return render(request, 'menu_email.html', { 'date': today, 'menu': menu })


def menu_list(request, menus):
    return render(request, 'menu_list.html', { 'menus': menus })


def week(request, week_num=None):
    today = datetime.date.today()
    start_date = today - datetime.timedelta(days=today.weekday())
    end_date = start_date + datetime.timedelta(days=5)
    menus = Menu.objects.filter(date__gte=start_date, date__lte=end_date)
    return render(request, 'menu_list.html', {
        'menus': menus,
        'start_date': start_date,
        'end_date': end_date,
    })
