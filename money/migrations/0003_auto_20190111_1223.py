# Generated by Django 2.1.1 on 2019-01-11 05:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money', '0002_auto_20190111_1035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2019, 1, 11, 12, 23, 55, 951441)),
        ),
    ]
