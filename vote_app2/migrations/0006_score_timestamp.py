# Generated by Django 4.2.13 on 2024-07-07 17:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app2', '0005_alter_customuser_options_customuser_date_joined_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
