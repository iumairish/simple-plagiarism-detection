# Generated by Django 3.2.8 on 2021-11-02 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_submissions_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='result',
            field=models.BooleanField(default=False),
        ),
    ]
