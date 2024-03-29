# Generated by Django 3.2.5 on 2022-12-08 15:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0033_auto_20221125_1741'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlepage',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='pages.people', verbose_name='Autor*in'),
        ),
        migrations.AlterField(
            model_name='exams',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('beginner', 'Anfänger'), ('intermediate', 'Examen'), ('advanced', 'Fortgeschrittene'), ('shortcases', 'Kurzfälle')], max_length=255, verbose_name='Schwierigkeitsgrad'),
        ),
    ]
