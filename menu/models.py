from django.db import models


class MenuItem(models.Model):
    name = models.CharField(max_length=200)

    @property
    def is_vegan(self):
        return 'vegan' in self.name.lower()

    def __str__(self):
        return self.name


class Menu(models.Model):
    LUNCH = 'L'
    DINNER = 'D'
    MENU_TYPE_CHOICES = (
        (LUNCH, 'Lunch'),
        (DINNER, 'Dinner'),
    )
    menu_type = models.CharField(max_length=1, choices=MENU_TYPE_CHOICES)
    date = models.DateField()
    items = models.ManyToManyField(MenuItem)
    vendor = models.CharField(max_length=50, null=True, blank=True)
    notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ("menu_type", "date")

    def __str__(self):
        return '{} ({}) - {}'.format(
            str(self.date),
            'Lunch' if self.menu_type == 'L' else 'Dinner',
            self.vendor
        )
