# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('recetas', '0002_auto_20151124_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente',
            name='activo',
        ),
        migrations.AlterField(
            model_name='pedidofijo',
            name='fecha_inicio',
            field=models.DateField(default=datetime.date(2015, 11, 20)),
        ),
    ]
