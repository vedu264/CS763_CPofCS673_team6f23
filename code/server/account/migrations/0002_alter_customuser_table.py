# Generated by Django 4.2.6 on 2023-11-10 00:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='customuser',
            table='users',
        ),
    ]
