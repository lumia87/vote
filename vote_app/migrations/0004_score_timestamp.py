# Generated by Django 5.0.6 on 2024-07-05 07:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0003_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
