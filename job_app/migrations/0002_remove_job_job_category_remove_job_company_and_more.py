# Generated by Django 5.0.1 on 2024-09-13 07:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('job_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='job_category',
        ),
        migrations.RemoveField(
            model_name='job',
            name='company',
        ),
        migrations.RemoveField(
            model_name='job',
            name='location',
        ),
        migrations.DeleteModel(
            name='Application',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Company',
        ),
        migrations.DeleteModel(
            name='Job',
        ),
        migrations.DeleteModel(
            name='Location',
        ),
    ]
