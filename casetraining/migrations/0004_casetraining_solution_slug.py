# Generated by Django 3.2.5 on 2023-01-30 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casetraining', '0003_casetraining_submission'),
    ]

    operations = [
        migrations.AddField(
            model_name='casetraining',
            name='solution_slug',
            field=models.TextField(blank=True, null=True),
        ),
    ]
