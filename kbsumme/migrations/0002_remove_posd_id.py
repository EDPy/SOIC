# Generated by Django 2.0.7 on 2018-07-23 06:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kbsumme', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posd',
            name='id',
        ),
    ]