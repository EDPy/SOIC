from django.db import models

class Posd(models.Model):
    #This class is just repsresenting the cost position in KBSUMME
    hgpos = models.IntegerField(unique=True)
    description = models.CharField(max_length=200)
    hours = models.CharField(max_length=5)
    cost = models.CharField(max_length=5)

class KbMeta(models.Model):
    #This class is representing the meta data for one project. One row per project only.
    pid = models.IntegerField(unique=True)
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

    '''
    class Meta:
        unique_together = (("pid", "phase"),)
    '''

class T3000db(models.Model):
    #This is the T3000 detail cost calculation
    kbmeta = models.ForeignKey(KbMeta, to_field="pid", db_column="kbmeta", on_delete=models.CASCADE)
    posd = models.ForeignKey(Posd, to_field="hgpos", db_column="posd", on_delete=models.CASCADE)
    hours = models.FloatField()
    cost = models.FloatField()

class Stueckliste(models.Model):
    #Represents the Stueckliste
    kbmeta = models.ForeignKey(KbMeta, to_field="pid", db_column="kbmeta", on_delete=models.CASCADE)
    module = models.CharField(max_length=50)
    sheet = models.CharField(max_length=50)
    caname = models.CharField(max_length=50)
    description = models.TextField()
    mlfb = models.CharField(max_length=100)
    qty = models.FloatField()
    single_cost = models.FloatField()
    typlical = models.CharField(max_length=50)
    total_cost = models.FloatField()

class PbbMeta(models.Model):
    #Represents the PBB table
    kbmeta = models.ForeignKey(KbMeta, to_field="pid", db_column="kbmeta", on_delete=models.CASCADE)
    offer_no = models.IntegerField(unique=True)
    country_inst = models.CharField(max_length=100, blank=True)
    planttype = models.CharField(max_length=50, blank=True)
    projname = models.CharField(max_length=100, blank=True)
    qty_units = models.IntegerField(null=True)
    total_output = models.FloatField(null=True)
    customer = models.CharField(max_length=100, blank=True)
    endcustomer = models.CharField(max_length=100, blank=True)
    bidmanager = models.CharField(max_length=100, blank=True)
    fx_rate = models.FloatField(null=True)

class Pbb(models.Model):
    #PBB tatle cost, price information
    pbbmeta = models.ForeignKey(PbbMeta, to_field="offer_no", db_column="pbbmeta", on_delete=models.CASCADE)
    kind_of_business = models.CharField(max_length=150)
    entity = models.CharField(max_length=20, null=True)
    escalation = models.FloatField(null=True)
    transportation = models.FloatField(null=True)
    custom_tax = models.FloatField(null=True)
    fx_gain_loss = models.FloatField(null=True)
    financing = models.FloatField(null=True)
    insurance = models.FloatField(null=True)
    bank_charges = models.FloatField(null=True)
    technical_risk = models.FloatField(null=True)
    warranty = models.FloatField(null=True)
    sales_oh = models.FloatField(null=True)
    net_margin = models.FloatField(null=True)
    single_cost_euro = models.FloatField(null=True)
    price = models.FloatField(null=True)
    price_nego = models.FloatField(null=True)
    total_surcharges = models.FloatField(null=True)
    total_includings = models.FloatField(null=True)
    total_sm = models.FloatField(null=True)
    total_cost = models.FloatField(null=True)
    total_price_euro = models.FloatField(null=True)
    total_price_fx = models.FloatField(null=True)
