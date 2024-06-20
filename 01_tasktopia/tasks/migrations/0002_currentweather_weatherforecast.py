# Generated by Django 5.0.6 on 2024-06-20 16:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CurrentWeather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_direction', models.CharField(max_length=50)),
                ('precipitation', models.FloatField()),
                ('uv_index', models.FloatField(default=0)),
                ('air_pressure', models.FloatField()),
                ('visibility', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Current Weather',
                'ordering': ['-timestamp'],
            },
        ),
        migrations.CreateModel(
            name='WeatherForecast',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=100)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('temperature', models.FloatField()),
                ('humidity', models.FloatField()),
                ('wind_speed', models.FloatField()),
                ('wind_direction', models.CharField(max_length=50)),
                ('precipitation', models.FloatField()),
                ('uv_index', models.FloatField(default=0)),
                ('air_pressure', models.FloatField()),
                ('visibility', models.FloatField()),
                ('forecast_time', models.DateTimeField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Weather Forecasts',
                'ordering': ['-forecast_time'],
            },
        ),
    ]
