# Generated by Django 5.0.2 on 2024-03-01 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('laundromat_app', '0002_alter_laundromat_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='laundromat',
            old_name='email',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='laundromat',
            name='password',
        ),
        migrations.RemoveField(
            model_name='laundromat',
            name='phone',
        ),
    ]
