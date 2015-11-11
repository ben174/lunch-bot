import re
from datetime import date
import unicodedata
from menu.models import Menu, MenuItem, Meal

days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


class MenuEntry:
    """
    A class to hold a given date's meal. This class is then converted into its ORM counterpart.

    """
    def __init__(self, meal_type=None):
        self.meal_type = meal_type
        self.items = []
        self.vendor = None
        self.date = None


def parse_menu_text(menu_text):
    """
    Parses plain text menu as found at https://sites.google.com/a/intrafile.com/intranet/home/lunch-menu
    and turns it into a list of MenuEntry objects.

    """
    meals = []
    curr_meal = None

    current_meal_type = 'L'
    lines = menu_text.split('\n')
    for line in lines:
        # lunch menu header
        if line.lower().startswith('lunch menu'):
            current_meal_type = 'L'
        # dinner menu header
        elif line.lower().startswith('dinner menu'):
            current_meal_type = 'D'
        # menu date header
        elif line.startswith(days_of_week):
            curr_meal = MenuEntry(meal_type=current_meal_type)
            meals.append(curr_meal)
            matches = re.findall(r'.*, (.*) ([0-9]+).*: (.*)', line)[0]
            month_name, day, vendor = matches
            day = int(day)
            month = months.index(month_name)
            #TODO: Determine year somehow
            meal_date = date(2015, month, day)
            curr_meal.date = meal_date
            curr_meal.vendor = vendor
        # delicious menu item
        else:
            if line.strip():
                item_name = line.strip()
                item_name = unicodedata.normalize('NFKD', item_name).encode('ascii','ignore')
                curr_meal.items.append(item_name)
    return meals


def menu_entry_to_db(entry):
    """
    Converts a MenuEntry into Meal, Menu, and MenuItem objects which are stored in the database.

    """
    menu, _ = Menu.objects.get_or_create(date=entry.date)
    meal = Meal.objects.create(meal_type=entry.meal_type, vendor=entry.vendor)
    for item_name in entry.items:
        item, _ = MenuItem.objects.get_or_create(name=item_name)
        meal.items.add(item)
    if entry.meal_type == 'L':
        if menu.lunch:
            menu.lunch.delete()
        menu.lunch = meal
    if entry.meal_type == 'D':
        if menu.dinner:
            menu.dinner.delete()
        menu.dinner = meal
    menu.save()
    return menu
