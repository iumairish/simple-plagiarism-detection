# Generated by Django 3.2.8 on 2021-10-27 13:02

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20211027_1621'),
    ]

    operations = [
        migrations.AddField(
            model_name='submissions',
            name='submit_date',
            field=models.DateTimeField(default=datetime.datetime.now, max_length=100),
        ),
    ]