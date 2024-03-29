# Generated by Django 3.2.5 on 2022-11-21 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wagtaildocs', '0012_uploadeddocument'),
        ('pages', '0030_auto_20221121_1159'),
    ]

    operations = [
        migrations.AddField(
            model_name='exams',
            name='loesung_dl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Lösung [PDF]'),
        ),
        migrations.AlterField(
            model_name='exams',
            name='sachverhalt_dl',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='wagtaildocs.document', verbose_name='Sachverhalt [PDF]'),
        ),
    ]
