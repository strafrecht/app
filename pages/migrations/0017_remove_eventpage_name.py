# Generated by Django 3.2.5 on 2021-07-26 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0016_eventspage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='eventpage',
            name='name',
        ),
    ]
