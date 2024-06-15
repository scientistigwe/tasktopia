# Generated by Django 5.0.6 on 2024-06-13 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='currentweather',
            options={'ordering': ['-timestamp'], 'verbose_name_plural': 'Current Weather'},
        ),
        migrations.AlterModelOptions(
            name='weatherforecast',
            options={'ordering': ['-forecast_time'], 'verbose_name_plural': 'Weather Forecasts'},
        ),
        migrations.AlterField(
            model_name='currentweather',
            name='uv_index',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='weatherforecast',
            name='uv_index',
            field=models.FloatField(default=0),
        ),
    ]
