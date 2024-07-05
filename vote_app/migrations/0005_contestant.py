# Generated by Django 5.0.6 on 2024-07-05 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote_app', '0004_score_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contestant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=100)),
                ('date_of_birth', models.DateField()),
                ('position', models.CharField(max_length=50)),
            ],
        ),
    ]
