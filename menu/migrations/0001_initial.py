# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menu_type', models.CharField(max_length=1, choices=[(b'L', b'Lunch'), (b'D', b'Dinner')])),
                ('date', models.DateField()),
                ('vendor', models.CharField(max_length=50, null=True, blank=True)),
                ('notified', models.BooleanField(default=False)),
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
            model_name='menu',
            name='items',
            field=models.ManyToManyField(to='menu.MenuItem'),
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('menu_type', 'date')]),
        ),
    ]
