from .models import Stueckliste, KbMeta
import matplotlib.path as plt
import pygal

def iograph():
    stueckl_obj = Stueckliste.objects
    kbmeta_objects = KbMeta.objects

    projects_pid = [] #holds the PID number of all projects in database
    iocount = [] # Holds the total IO qty of all projects in database

    for item in kbmeta_objects:
        projects_pid.append(item.pid)

    for i in range(0, len(projects_pid)):
        iocount.append(total_IO(projects_pid[i]))
    '''
    plt.scatter(proj_name, iocount, c=colors, alpha=0.5)
    plt.show()
    '''

def total_IO(pid):
    '''This function shall deliver following information out of the Stueckliste sheet:
    - Qty and cost of IO-modules, controller and cabinets.
    - It shall also deliver the total sum of hardware equipment'''

    stueckl_obj = Stueckliste.objects

    query_SM321_16DI = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7321-1BH02-0AA0')
    query_SM321_16SOE = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7321-7BH01-0AB0')
    query_SM322_16DO = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7322-1BH01-0AA0')
    query_SM322_32DO_FS = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7322-1BL00-0AA0')
    query_SM326_24DI_FS = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7326-1BK02-0AB0')
    query_SM326_10DO_FS = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7326-2BF10-0AB0')
    query_SM331_8AI = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7331-7NF00-0AB0')
    query_SM332_4AO = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7332-5HD01-0AB0')
    query_SM332_8AO = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7332-5HF00-0AB0')
    query_SM336_6AI_FS = stueckl_obj.filter(pid__iexact=str(pid)).filter(mlfb__icontains='6ES7336-4GE00-0AB0')

    query_AS3000_HW3 = stueckl_obj.filter(mlfb__icontains='6DU1173-1BA00-0AA0')

    qty_modules_dict = {'sum_SM321_16DI':0.0, 'sum_SM321_16SOE':0.0, 'sum_SM322_16DO':0.0,
                          'sum_SM322_32DO_FS':0.0, 'sum_SM326_24DI_FS':0.0, 'sum_SM326_10DO_FS':0.0,
                          'sum_SM331_8AI':0.0, 'sum_SM332_4AO':0.0, 'sum_SM332_8AO':0.0,
                          'sum_SM336_6AI_FS':0.0, 'sum_AS3000_HW3':0.0}


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

    totalIO = 0.0
    totalIO =   (qty_modules_dict['sum_SM321_16DI'] + qty_modules_dict['sum_SM321_16SOE'] +
                qty_modules_dict['sum_SM322_16DO']) * 16 +\
                (qty_modules_dict['sum_SM322_32DO_FS'] *32) + (qty_modules_dict['sum_SM326_24DI_FS']*24) +\
                (qty_modules_dict['sum_SM326_10DO_FS'] * 10) + (qty_modules_dict['sum_SM331_8AI'] * 8) +\
                (qty_modules_dict['sum_SM332_4AO'] * 4) + (qty_modules_dict['sum_SM332_8AO'] * 8) +\
                (qty_modules_dict['sum_SM336_6AI_FS'] *6)

    return totalIO