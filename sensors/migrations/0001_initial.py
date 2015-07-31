# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def load_fixture(apps, schema_editor):
    from django.core.management import call_command
    call_command('loaddata', 'initial_sensors', app_label='sensors')

def unload_fixture(apps, schema_editor):
    SensorType = apps.get_model("sensors", "SensorType")
    SensorType.objects.filter(read_only=True).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('resources', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('timestamp', models.IntegerField()),
                ('value', models.FloatField()),
            ],
            options={
                'get_latest_by': 'timestamp',
                'ordering': ['timestamp'],
            },
        ),
        migrations.CreateModel(
            name='SensingPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('property', models.ForeignKey(to='resources.ResourceProperty', related_name='sensing_points')),
            ],
            options={
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Sensor',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100, blank=True)),
                ('resource', models.ForeignKey(to='resources.Resource', related_name='sensors')),
            ],
            options={
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='SensorType',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('resource_type', models.ForeignKey(to='resources.ResourceType', related_name='sensor_types')),
                ('read_only', models.BooleanField(default=False, editable=False)),
                ('properties', models.ManyToManyField(related_name='sensor_types', to='resources.ResourceProperty')),
            ],
            options={
                'abstract': False,
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='sensor',
            name='sensor_type',
            field=models.ForeignKey(to='sensors.SensorType', related_name='sensors'),
        ),
        migrations.AddField(
            model_name='sensingpoint',
            name='sensor',
            field=models.ForeignKey(to='sensors.Sensor', related_name='sensing_points'),
        ),
        migrations.AddField(
            model_name='datapoint',
            name='origin',
            field=models.ForeignKey(to='sensors.SensingPoint', related_name='data_points+'),
        ),
        migrations.RunPython(load_fixture, reverse_code=unload_fixture)
    ]
