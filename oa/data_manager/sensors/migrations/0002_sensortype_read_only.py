# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sensors', '0001_squashed_0004_auto_20150812_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='sensortype',
            name='read_only',
            field=models.BooleanField(editable=False, default=False),
        ),
    ]
