from django.db import models

class Posd(models.Model):
    #This class is just repsresenting the cost position in KBSUMME
    hgpos = models.IntegerField(primary_key=True)
    description = models.CharField(max_length=200)
    hours = models.CharField(max_length=5)
    cost = models.CharField(max_length=5)

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
    phase = models.CharField(max_length=50, blank=True) # Budget / Firm-Bid

class T3000db(models.Model):
    #This is the T3000 detail cost calculation
    hours = models.FloatField()
    cost = models.FloatField()
    pid = models.ForeignKey(KbMeta, on_delete=models.CASCADE)
    hgpos = models.ForeignKey(Posd, on_delete=models.CASCADE)

'''
class Stueckliste(models.Model):
    #Represents the Stueckliste
    module = models.CharField(max_length=50)
    sheet = models.CharField(max_length=50)
    caname = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    mlfb = models.CharField(max_length=100)
    qty = models.FloatField()
    single_cost = models.FloatField()
    typlical = models.CharField(max_length=50)
    total_cost = models.FloatField()
    kbmeta = models.ForeignKey(KbMeta, on_delete=models.CASCADE)
'''