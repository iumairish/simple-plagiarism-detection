# Generated by Django 3.2.8 on 2021-11-04 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_submissions_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='exclude_urls',
            field=models.TextField(blank=True),
        ),
    ]
