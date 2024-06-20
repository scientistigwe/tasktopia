# Generated by Django 5.0.6 on 2024-06-18 01:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.category')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('forecast', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.forecast')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.report')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
            ],
        ),
        migrations.CreateModel(
            name='TaskWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
                ('weather', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.weather')),
            ],
        ),
        migrations.CreateModel(
            name='UserTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_log', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.eventlog')),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.userprofile')),
            ],
        ),
    ]