# Generated by Django 3.2.5 on 2022-11-21 11:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('pages', '0029_alter_people_role'),
    ]

    operations = [
        migrations.AddField(
            model_name='exams',
            name='sachverhalt_dl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='wagtaildocs.document'),
        ),
        migrations.AlterField(
            model_name='exams',
            name='difficulty',
            field=models.CharField(blank=True, choices=[('beginner', 'Anfänger'), ('intermediate', 'Fortgeschrittene'), ('advanced', 'Examen'), ('shortcases', 'Kurzfälle')], max_length=255, verbose_name='Schwierigkeitsgrad'),
        ),
    ]
