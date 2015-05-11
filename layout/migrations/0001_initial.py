# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='main_aisle',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('width', models.FloatField(null=True)),
                ('length', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
                ('z', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='main_bay',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('width', models.FloatField(null=True)),
                ('length', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
                ('z', models.FloatField(null=True)),
                ('parent', models.ForeignKey(to='layout.main_aisle')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='main_enclosure',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('width', models.FloatField(null=True)),
                ('length', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='main_tray',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('width', models.FloatField(null=True)),
                ('length', models.FloatField(null=True)),
                ('height', models.FloatField(null=True)),
                ('x', models.FloatField(null=True)),
                ('y', models.FloatField(null=True)),
                ('z', models.FloatField(null=True)),
                ('num_rows', models.IntegerField()),
                ('num_cols', models.IntegerField()),
                ('parent', models.ForeignKey(to='layout.main_bay')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='main_aisle',
            name='parent',
            field=models.ForeignKey(default=1, to='layout.main_enclosure'),
        ),
    ]
