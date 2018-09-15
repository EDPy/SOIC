import models
import pandas as pd

def createdataframe():
    df_posd = pd.DataFrame.from_records(Posd.objects.all().values())
    df_kbmeta = pd.DataFrame.from_records(KbMeta.objects.all().values())
    df_stckl = pd.DataFrame.from_records(Stueckliste.objects.all().values())
    df_t3000 = pd.DataFrame.from_records(T3000db.objects.all().values())
    df_pbbmeta = pd.DataFrame.from_records(PbbMeta.objects.all().values())
    df_pbb = pd.DataFrame.from_records(Pbb.objects.all().values())
    df_customer = pd.DataFrame.from_records(Customer.objects.all().values())
