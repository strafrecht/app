# Generated by Django 3.1.8 on 2021-07-01 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_articlepage_sidebar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articlepage',
            name='cover',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='cover_caption',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='intro',
        ),
        migrations.RemoveField(
            model_name='articlepage',
            name='subtitle',
        ),
    ]
