# Generated by Django 2.0.7 on 2018-09-10 03:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbsumme', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posd',
            name='cost',
            field=models.CharField(blank=True, max_length=5),
        ),
        migrations.AlterField(
            model_name='posd',
            name='description',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='posd',
            name='hours',
            field=models.CharField(blank=True, max_length=5),
        ),
    ]
