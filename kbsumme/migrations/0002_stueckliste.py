# Generated by Django 2.0.7 on 2018-07-24 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('kbsumme', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Stueckliste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('module', models.CharField(max_length=50)),
                ('sheet', models.CharField(max_length=50)),
                ('caname', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=200)),
                ('mlfb', models.CharField(max_length=100)),
                ('qty', models.FloatField()),
                ('single_cost', models.FloatField()),
                ('typlical', models.CharField(max_length=50)),
                ('total_cost', models.FloatField()),
                ('kbmeta', models.ForeignKey(db_column='kbmeta', on_delete=django.db.models.deletion.CASCADE, to='kbsumme.KbMeta', to_field='pid')),
            ],
        ),
    ]
