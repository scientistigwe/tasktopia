# Generated by Django 5.0.6 on 2024-06-21 09:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_userprofile_groups_and_more'),
        ('dashboard', '0005_alter_eventlog_user_alter_forecast_user_and_more'),
        ('reports', '0006_alter_reportdetail_user_profile_and_more'),
        ('tasks', '0004_remove_taskforecast_forecast_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
