# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meal_type', models.CharField(max_length=1, choices=[(b'L', b'Lunch'), (b'D', b'Dinner')])),
                ('vendor', models.CharField(max_length=50, null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('notified', models.BooleanField(default=False)),
                ('dinner', models.OneToOneField(related_name='dinner', null=True, blank=True, to='menu.Meal')),
                ('lunch', models.OneToOneField(related_name='lunch', null=True, blank=True, to='menu.Meal')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.AddField(
            model_name='meal',
            name='items',
            field=models.ManyToManyField(to='menu.MenuItem'),
        ),
    ]
