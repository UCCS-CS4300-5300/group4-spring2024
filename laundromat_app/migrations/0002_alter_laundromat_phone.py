# Generated by Django 4.2.6 on 2024-02-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('laundromat_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='laundromat',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
