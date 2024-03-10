# Generated by Django 5.0.2 on 2024-03-09 23:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundromat_app', '0003_rename_email_laundromat_location_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machines',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('machine_ID', models.CharField(max_length=100, unique=True)),
                ('machine_choice', models.CharField(choices=[('Dryer', 'Dryer'), ('Washer', 'Washer')], max_length=6)),
                ('status', models.CharField(choices=[('Open', 'Open'), ('Resvered', 'Reserved')], default='Open', max_length=8)),
                ('laundromat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laundromat_app.laundromat')),
            ],
        ),
    ]