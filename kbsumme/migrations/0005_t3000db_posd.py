# Generated by Django 2.0.7 on 2018-07-22 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kbsumme', '0004_auto_20180722_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='t3000db',
            name='posd',
            field=models.ManyToManyField(to='kbsumme.Posd'),
        ),
    ]