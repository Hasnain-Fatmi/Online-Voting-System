# Generated by Django 4.2.7 on 2023-11-30 07:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate_Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.CharField(max_length=20)),
                ('Last_Name', models.CharField(max_length=20)),
                ('Father_Name', models.CharField(max_length=20)),
                ('Email', models.CharField(max_length=50)),
                ('CNIC', models.CharField(max_length=13)),
                ('Address', models.TextField()),
                ('City', models.CharField(max_length=13)),
                ('Phone_Number', models.CharField(max_length=11)),
                ('Gender', models.CharField(max_length=6)),
                ('Age', models.CharField(max_length=6)),
                ('Nationalities', models.TextField()),
                ('Party', models.CharField(max_length=15)),
                ('symbol', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Voter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('First_Name', models.TextField(max_length=20)),
                ('Last_Name', models.TextField(max_length=20)),
                ('Email', models.TextField(max_length=30)),
                ('CNIC', models.TextField(max_length=13)),
                ('Address', models.TextField()),
                ('Phone_Number', models.TextField(max_length=11)),
                ('Gender', models.TextField(max_length=6)),
                ('Password', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ControlVote',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePage.position')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=100)),
                ('Email', models.TextField(max_length=30)),
                ('CNIC', models.TextField(max_length=13)),
                ('Party', models.TextField(max_length=15)),
                ('symbol', models.TextField(max_length=15)),
                ('image', models.ImageField(upload_to='images/', verbose_name='Candidate Pic')),
                ('total_vote', models.IntegerField(default=0, editable=False)),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='HomePage.position')),
            ],
        ),
    ]
