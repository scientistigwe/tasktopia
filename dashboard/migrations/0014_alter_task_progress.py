# Generated by Django 5.0.6 on 2024-07-02 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0013_task_progress'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
