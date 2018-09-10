from .models import Stueckliste, KbMeta, T3000db
import matplotlib.pyplot as plt
import pygal
import numpy as np
from .project_graph import sum_calculation

def iograph():
    '''
    This function is to create a graph based on year and market price.
    Market price needs to be equalized first to commpare projects with each
    other.

    In order to equalize:
    TODO: Take total DCS cost per project
    TODO: Take total number of IO in DCS
    TODO: Assume SLS PM/CPM cost and add it to DCS cost
    TODO: Check Marshalling cabinet and Furniture to assume both values if required
    TODO: Put 10% on total DCS cost (levelized) and compare with our price level
    If price gap very high, assume add-ons, those need to be deleted from the market price.
    TODO: Print adjusted market price/IO based on submission year
    '''
    stueckl_obj = Stueckliste.objects
    kbmeta_objects = KbMeta.objects
    t3000db_objects = T3000db.objects

    lpid = [] #Holds PID of all projects
    ldatecalc = [] #Holds the calculation date of all projects in database
    lio_count = [] #Holds the total IO qty of all projects in database
    ldcs_cost = [] #Holds all totalcost of
    lprojname = [] #Holds all project name in the database

    for item in kbmeta_objects.all():
        lpid.append(item.pid)
        lprojname.append(item.projname)
        ldatecalc.append(item.datecalc)

    for i in range(0, len(lpid)):
        lio_count.append(total_IO(lpid[i]))

    for i in range(0, len(lpid)):
        sum_Dict = sum_calculation(lpid[i], t3000db_objects)
        ldcs_cost.append(sum(sum_Dict.values()))

    for i in range(0, len(lpid)):
        print('Project {},  PID {},     Date {},    IO {},  Cost {}'.format(lprojname[i], lpid[i], ldatecalc[i], lio_count[i], ldcs_cost[i]))

    fname = 'media/iocount.svg'

    #Calculate the IO-cost
    np_ldcs_cost = np.array(ldcs_cost)
    np_lio_count = np.array(lio_count)
    lio_cost = np_ldcs_cost/np_lio_count

    lprojname_s = []
    for item in lprojname:
        lprojname_s.append(item)

    x = [x for x in range(len(lprojname_s))]

    plt.scatter(lprojname_s, lio_cost, s=(np_lio_count/100))
    plt.ylabel('IO-Qty')
    plt.xticks(x,lprojname_s, rotation='vertical')
    plt.savefig(fname)


def total_IO(pid):
    '''This function shall deliver following information out of the Stueckliste sheet:
    - Qty and cost of IO-modules, controller and cabinets.
    - It shall also deliver the total sum of hardware equipment'''

    stueckl_obj = Stueckliste.objects


    #ET 200 Modules
    query_SM321_16DI = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7321-1BH02-0AA0')
    query_SM321_16SOE = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7321-7BH01-0AB0')
    query_SM322_16DO = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7322-1BH01-0AA0')
    query_SM322_32DO_FS = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7322-1BL00-0AA0')
    query_SM326_24DI_FS = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7326-1BK02-0AB0')
    query_SM326_10DO_FS = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7326-2BF10-0AB0')
    query_SM331_8AI = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7331-7NF00-0AB0')
    query_SM332_4AO = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7332-5HD01-0AB0')
    query_SM332_8AO = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7332-5HF00-0AB0')
    query_SM336_6AI_FS = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6ES7336-4GE00-0AB0')

    #SPHA Modules
    query_SPHA_16DI = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6DL1131-6BH00-0EH1')
    query_SPHA_16DQ = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6DL1132-6BH00-0EH1')
    query_SPHA_16AIDIDQ_HART = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6DL1133-6EW00-0EH1')
    query_SPHA_8AQ = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6DL1135-6TF00-0EH1')

    #Controller
    query_AS3000_HW3 = stueckl_obj.filter(kbmeta__pid__iexact=str(pid)).filter(mlfb__icontains='6DU1173-1BA00-0AA0')

    qty_modules_dict = {'sum_SM321_16DI':0.0, 'sum_SM321_16SOE':0.0, 'sum_SM322_16DO':0.0,
                          'sum_SM322_32DO_FS':0.0, 'sum_SM326_24DI_FS':0.0, 'sum_SM326_10DO_FS':0.0,
                          'sum_SM331_8AI':0.0, 'sum_SM332_4AO':0.0, 'sum_SM332_8AO':0.0,
                          'sum_SM336_6AI_FS':0.0, 'sum_AS3000_HW3':0.0}

    qty_SPHA_dict = {'sum_SPHA_16DI': 0.0, 'sum_SPHA_16DQ':0.0, 'sum_SPHA_16AIDIDQ_HART':0.0,
    'query_SPHA_8AQ':0.0}

    #Sum of all ET200M modules
    for item in query_SM321_16DI:
        qty_modules_dict['sum_SM321_16DI'] += item.qty

    for item in query_SM321_16SOE:
        qty_modules_dict['sum_SM321_16SOE'] += item.qty

    for item in query_SM322_16DO:
        qty_modules_dict['sum_SM322_16DO'] += item.qty

    for item in query_SM322_32DO_FS:
        qty_modules_dict['sum_SM322_32DO_FS'] += item.qty

    for item in query_SM326_24DI_FS:
        qty_modules_dict['sum_SM326_24DI_FS'] += item.qty

    for item in query_SM326_10DO_FS:
        qty_modules_dict['sum_SM326_10DO_FS'] += item.qty

    for item in query_SM331_8AI:
        qty_modules_dict['sum_SM331_8AI'] += item.qty

    for item in query_SM332_4AO:
        qty_modules_dict['sum_SM332_4AO'] += item.qty

    for item in query_SM332_8AO:
        qty_modules_dict['sum_SM332_8AO'] += item.qty

    for item in query_SM336_6AI_FS:
        qty_modules_dict['sum_SM336_6AI_FS'] += item.qty

    for item in query_AS3000_HW3:
        qty_modules_dict['sum_AS3000_HW3'] += item.qty

    #Sum of each SPHA modules
    for item in query_SPHA_16DI:
        qty_SPHA_dict['sum_SPHA_16DI'] += item.qty

    for item in query_SPHA_16DQ:
        qty_SPHA_dict['sum_SPHA_16DQ'] += item.qty

    for item in query_SPHA_16AIDIDQ_HART:
        qty_SPHA_dict['sum_SPHA_16AIDIDQ_HART'] += item.qty

    for item in query_SPHA_8AQ:
        qty_SPHA_dict['query_SPHA_8AQ'] += item.qty


    total_M =   (qty_modules_dict['sum_SM321_16DI'] + qty_modules_dict['sum_SM321_16SOE'] +
                qty_modules_dict['sum_SM322_16DO']) * 16 +\
                (qty_modules_dict['sum_SM322_32DO_FS'] *32) + (qty_modules_dict['sum_SM326_24DI_FS']*24) +\
                (qty_modules_dict['sum_SM326_10DO_FS'] * 10) + (qty_modules_dict['sum_SM331_8AI'] * 8) +\
                (qty_modules_dict['sum_SM332_4AO'] * 4) + (qty_modules_dict['sum_SM332_8AO'] * 8) +\
                (qty_modules_dict['sum_SM336_6AI_FS'] *6)

    total_SPHA = (qty_SPHA_dict['sum_SPHA_16DI'] + qty_SPHA_dict['sum_SPHA_16DQ'] +
    qty_SPHA_dict['sum_SPHA_16AIDIDQ_HART']) * 16 + (qty_SPHA_dict['query_SPHA_8AQ'] * 8)


    return (total_M + total_SPHA)

    def totalcost(pid):
        pass
