# Generated by Django 4.2.7 on 2023-12-03 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HomePage', '0005_controlvote_candidate_controlvote_timestamp'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotingPeriod',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField()),
                ('end_datetime', models.DateTimeField()),
            ],
        ),
    ]
