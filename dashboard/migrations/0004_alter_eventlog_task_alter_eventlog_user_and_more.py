# Generated by Django 5.0.6 on 2024-06-20 22:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_userprofile_managers_and_more'),
        ('dashboard', '0003_alter_eventlog_user_alter_forecast_user_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventlog',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_event_logs', to='dashboard.task'),
        ),
        migrations.AlterField(
            model_name='eventlog',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_event_logs', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_forecasts', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='forecast',
            name='weather',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='forecast', to='dashboard.weather'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='task_notifications', to='dashboard.task'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_reports', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='category_tasks', to='dashboard.category'),
        ),
        migrations.AlterField(
            model_name='task',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_tasks', to='accounts.userprofile'),
        ),
        migrations.AlterField(
            model_name='weather',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_weather', to='accounts.userprofile'),
        ),
    ]