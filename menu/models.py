from django.db import models


class Allergen(models.Model):
    """
    A food alleren. MenuItems may contain zero or more of these

    Alcohol (A), Bell Pepper (BP), Cilantro (Cil), Coriander (Cor), Dairy (D), Egg (E), Gluten (G),
    Garlic (Gar), Mango (Mg), Nut (N), Olives (O), Pork (P), Shellfish (Sh), Soy (Soy), Spicy (Sp),
    Vegan (Vegan), Vegetarian (Veget), Wheat (W)

    """
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)


class MenuItem(models.Model):
    """
    An item on the menu.

    This is a many-to-many with meals, so multiple meals might have the same
    menu item. This would come in handy if we ever wanted to query for other days containing the same
    menu items.

    """
    name = models.CharField(max_length=200)
    allergens = models.ManyToManyField(Allergen)

    @property
    def vegetarian(self):
        return (
            'vegan' in self.name.lower() or
            'vegetarian' in self.name.lower() or
            '(veg)' in self.name.lower()
        )

    def __str__(self):
        return self.name


class Meal(models.Model):
    """
    A meal, provided by a vendor, containing items (MenuItem).

    """
    LUNCH = 'L'
    DINNER = 'D'
    MENU_TYPE_CHOICES = (
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    )
    meal_type = models.CharField(max_length=1, choices=MENU_TYPE_CHOICES)
    cuisine = models.CharField(max_length=50, null=True, blank=True)
    items = models.ManyToManyField(MenuItem)
    vendor = models.CharField(max_length=50, null=True, blank=True)

    @property
    def friendly_type(self):
        if self.meal_type == 'L':
            return 'Lunch'
        elif self.meal_type == 'D':
            return 'Dinner'
        return None

    def __str__(self):
        return '{} - {}'.format(
            self.friendly_type,
            self.vendor
        )


class Menu(models.Model):
    """
    The menu for a specific date. Has a one-to-one to Meal for both lunch and dinner.

    A notified flag indicates whether this date's menu has been mailed out.

    """
    date = models.DateField()
    notified = models.BooleanField(default=False)
    lunch = models.OneToOneField(Meal, related_name='lunch', null=True, blank=True)
    dinner = models.OneToOneField(Meal, related_name='dinner', null=True, blank=True)


    class Meta:
        ordering = ['date']

    def to_text(self, meal='B'):
        ret = ""
        if meal == 'B' or meal == 'L':
            ret += "LUNCH - {}\n\n".format(self.lunch.vendor)
            if not self.lunch:
                if meal == 'L':
                    return 'No lunch menu entered for {}. '.format(self.date)
            else:
                for item in self.lunch.items.all():
                    ret += '  {}\n'.format(item.name)
                ret += '\n\n'
        if meal == 'B' or meal == 'D':
            ret += "DINNER - {}\n\n".format(self.dinner.vendor)
            if not self.dinner:
                if meal == 'D':
                    return 'No dinner menu entered for {}. '.format(self.date)
            else:
                for item in self.dinner.items.all():
                    ret += '  {}\n'.format(item.name)
                ret += '\n'
        return ret

    def __str__(self):
        leg = 'No meals'

        if self.lunch and self.dinner:
            leg = 'Lunch and Dinner'
        elif self.lunch:
            leg = 'Lunch only'
        elif self.dinner:
            leg = 'Dinner only'
        return '{} - {} (Notified: {})'.format(
            self.date,
            leg,
            str(self.notified),
        )

