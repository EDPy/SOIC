from django.db import models

class Posd(models.Model):
    # TODO ALSO excel sheet source shall be stored in database as proof or in case of doubt of the value to validate it.
    #This class is just repsresenting the cost position in KBSUMME
    hg = models.IntegerField()
    pos = models.IntegerField()
    description = models.CharField(max_length=200)
    hours = models.CharField(max_length=5)
    cost = models.CharField(max_length=5)

    class Meta:
        unique_together = (('hg', 'pos'),)

class KbMeta(models.Model):
    #This class is representing the meta data for one project. One row per project only.
    pid = models.IntegerField(primary_key=True)
    klaversion = models.CharField(max_length=50, blank=True)
    calcbase = models.CharField(max_length=10, blank=True)
    contractbase = models.CharField(max_length=10, blank=True)
    quotno = models.CharField(max_length=50)
    filename = models.CharField(max_length=100)
    datecalc = models.DateField(default='1999-09-09')
    dateupload = models.DateTimeField(default='1999-09-09')
    projname = models.CharField(max_length=100, blank=True)
    customer = models.CharField(max_length=100, blank=True)
    endcustomer = models.CharField(max_length=100, blank=True)

class T3000db(models.Model):
    #TODO ALSO excel sheet source shall be stored in database as proof or in case of doubt of the value to validate it.
    #This is the T3000 detail cost calculation
    pid = models.IntegerField()
    hg = models.IntegerField()
    pos = models.IntegerField()
    hours = models.FloatField()
    cost = models.FloatField()

    class Meta:
        unique_together = (('pid', 'hg', 'pos'),)
