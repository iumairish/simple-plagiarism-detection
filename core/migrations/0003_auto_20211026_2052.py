# Generated by Django 3.2.8 on 2021-10-26 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20211026_2049'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submissions',
            name='assignment',
        ),
        migrations.AddField(
            model_name='submissions',
            name='assignment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.assignment'),
        ),
    ]