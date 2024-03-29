# Generated by Django 3.2.5 on 2022-11-03 15:06

from django.db import migrations, models
import django.db.models.deletion

from core.models import Submission

class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0007_auto_20221103_1102'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='article_revision',
        ),
        migrations.AddField(
            model_name='submission',
            name='content_id',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='submission',
            name='content_type',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype'),
            preserve_default=False,
        ),
    ]
