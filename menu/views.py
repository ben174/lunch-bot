import datetime
import json
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import unicodedata
from django.views.generic import TodayArchiveView, DateDetailView, DayArchiveView, ListView, WeekArchiveView
from util.menu_parser import parse_menu_text, menu_entry_to_db
from menu.models import Menu, MenuItem, Meal, Allergen


def parse(request):
    """
    A form to manually enter in this week's menu. Parses out the input and enters it into ORM.

    """
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
    """
    A preview of the email which will be sent for today.

    """
    today = datetime.date.today()
    menu = get_object_or_404(Menu, date=today)
    return render(request, 'menu_email.html', { 'date': today, 'menu': menu })


def menu_list(request, menus):
    """
    Outputs the specified menus for review after entry.

    """
    return render(request, 'menu_list.html', { 'menus': menus })


def week(request, year=None, month=None, day=None):
    """
    Displays this week's menu in a friendly layout.

    """
    today = datetime.date.today()
    current_week_number = str(today.isocalendar()[1])
    current_year = str(today.year)
    return MenuWeekArchiveView.as_view()(request, year=current_year, week=current_week_number)



def text(request, meal='B'):
    day=datetime.date.today()
    return HttpResponse(Menu.objects.get(date=day).to_text(meal=meal), content_type="text/plain")

def subscribe(request):
    return render(request, 'subscribe.html')


@csrf_exempt
def submit(request):
    menus = []
    payload = json.loads(request.body)
    for p in payload:
        date = datetime.datetime.strptime(p['date'], "%Y-%m-%dT%H:%M:%S.%fZ")
        menu, _ = Menu.objects.get_or_create(date=date)
        meal = Meal.objects.create(meal_type=p['mealType'], vendor=p['vendor'])
        for item_name in p['items']:
            item_name = unicodedata.normalize('NFKD', item_name).encode('ascii','ignore')
            item_allergens = []
            for allergen in Allergen.objects.all():
                code_string = '(' + allergen.code + ')'
                if code_string in item_name:
                    item_allergens.append(allergen)
                    item_name = item_name.replace(code_string, '')
            item_name = item_name.strip()
            item, _ = MenuItem.objects.get_or_create(name=item_name)
            item.allergens.clear()
            for allergen in item_allergens:
                item.allergens.add(allergen)
            meal.items.add(item)
        meal.cuisine = p['cuisine']
        meal.save()
        if meal.meal_type == 'L':
            if menu.lunch:
                menu.lunch.delete()
            menu.lunch = meal
        elif meal.meal_type == 'D':
            if menu.dinner:
                menu.dinner.delete()
            menu.dinner = meal
        else:
            raise Exception("Unknown meal type!")
        menu.save()
        menus.append(menu)
    today = datetime.date.today()
    return render(request, 'menus_block.html', {
        'menus': menus,
        'today': today,
    })


def provision_allergens(request):
    allergen_string = '''Alcohol (A), Bell Pepper (BP), Cilantro (Cil), Coriander (Cor), Dairy (D), Egg (E), Gluten (G),
    Garlic (Gar), Mango (Mg), Nut (N), Olives (O), Pork (P), Shellfish (Sh), Soy (Soy), Spicy (Sp),
    Vegan (Vegan), Vegetarian (Veget), Wheat (W)'''
    ret = ''
    for ae in allergen_string.split(','):
        ae = ae.replace(')', '')
        name, code = [x.strip() for x in ae.split('(')]
        allergen, created = Allergen.objects.get_or_create(name=name, code=code)
        ret += '{} ({}) - Created: {}\n'.format(name, code, str(created))
    return HttpResponse(ret, content_type="text/plain")


class MenuDayArchiveView(DayArchiveView):
    queryset = Menu.objects.all()
    date_field = "date"
    allow_future = True
    allow_empty = True


class MenuList(ListView):
    model = Menu


class MenuWeekArchiveView(WeekArchiveView):
    queryset = Menu.objects.all()
    date_field = "date"
    allow_future = True
    allow_empty = True
    ordering = 'date'
    week_format = "%W"

    def get_context_data(self, **kwargs):
        context = super(MenuWeekArchiveView, self).get_context_data(**kwargs)
        context['today'] = datetime.date.today()
        return context


