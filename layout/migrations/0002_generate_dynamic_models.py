# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from layout.operations import CreateDynamicModels


class Migration(migrations.Migration):

    dependencies = [
        ('layout', '0001_initial'), ('control', '0002_setup')
    ]

    operations = [
        CreateDynamicModels()
    ]
