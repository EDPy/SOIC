# Generated by Django 2.0.7 on 2018-07-19 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KbMeta',
            fields=[
                ('pid', models.IntegerField(primary_key=True, serialize=False)),
                ('klaversion', models.CharField(max_length=50)),
                ('calcbase', models.CharField(max_length=10)),
                ('contractbase', models.CharField(max_length=10)),
                ('quotno', models.CharField(max_length=50)),
                ('filename', models.CharField(max_length=100)),
                ('datecalc', models.DateField(default='1999-09-09')),
                ('projname', models.CharField(max_length=100)),
                ('customer', models.CharField(max_length=100)),
                ('endcustomer', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Posd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hg', models.IntegerField()),
                ('pos', models.IntegerField()),
                ('description', models.CharField(max_length=200)),
                ('hours', models.CharField(max_length=5)),
                ('cost', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='T3000db',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('hg', models.IntegerField()),
                ('pos', models.IntegerField()),
                ('hours', models.FloatField()),
                ('cost', models.FloatField()),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='t3000db',
            unique_together={('pid', 'hg', 'pos')},
        ),
        migrations.AlterUniqueTogether(
            name='posd',
            unique_together={('hg', 'pos')},
        ),
    ]
