import re
from datetime import date
import unicodedata
from menu.models import Menu, MenuItem

days_of_week = ('Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday')
months = ['', 'January', 'February', 'March', 'April', 'May', 'June', 'July',
        'August', 'September', 'October', 'November', 'December']


def parse_menu_text(menu_text):
    lunch_date = None
    lines = menu_text.split('\n')
    menu_type = 'L'
    current_menu = None
    new_menus = []
    for line in lines:
        # lunch menu header
        if line.lower().startswith('lunch menu'):
            menu_type = 'L'
        # dinner menu header
        elif line.lower().startswith('dinner menu'):
            menu_type = 'D'
        # menu date header
        elif line.startswith(days_of_week):
            matches = re.findall(r'.*, (.*) ([0-9]+).*: (.*)', line)[0]
            month_name, day, vendor = matches
            day = int(day)
            month = months.index(month_name)
            #TODO: Determine year somehow
            lunch_date = date(2015, month, day)
            menu, _ = Menu.objects.get_or_create(date=lunch_date, menu_type=menu_type)
            menu.vendor = vendor
            menu.items.clear()
            new_menus.append(menu)
            menu.save()
        # delicious menu item
        else:
            if lunch_date and line.strip():
                item_name = line.strip()
                item_name = unicodedata.normalize('NFKD', item_name).encode('ascii','ignore')
                menu_item, _ = MenuItem.objects.get_or_create(name=item_name)
                menu.items.add(menu_item)
    return new_menus
