from .models import KbMeta, T3000db

import matplotlib.path as plt
import pygal
from pygal.style import BlueStyle

def sum_calculation(pid, t3000_objects):
        '''
        More detail cost calculation method. To be loaded right after KBSUMME upload.
        Generate sum calculation from KBSUMME table with following information:

        Cost of General activities, Misc Engineering, Cost of Basic Engineering,
        Cost of Detail Engineering, Customer Documentation, Unit Control,
        Measurement analysis, Interface to foreign systems, Basic E-Technology,
        Detail E-Technology, FAT, Installation, Commissioning, HW peripherals,
        HW DCS, HW ET1, HW ET2, HW Installation

        returns back a dictionary with all the interim sum
        '''

        # This variable contains all ellements the sum of groups, e.g. basi enginering, hardware components etc.
        sum_Dict = {'sum_General': 0.0, 'sum_Eng_Misc': 0.0, 'sum_Basic_Eng': 0.0, 'sum_Detail_Eng': 0.0, 'sum_Cust_Docu': 0.0,
                    'sum_Unit_Control': 0.0,
                    'sum_Measurement': 0.0, 'sum_Int_Foreign_Sys': 0.0, 'sum_Basic_Eng_E': 0.0, 'sum_Detail_Eng_E': 0.0,
                    'sum_FAT': 0.0, 'sum_Installation': 0.0, 'sum_Commissioning': 0.0, 'sum_HW_Peri': 0.0,
                    'sum_HW_DCS': 0.0, 'sum_HW_E1': 0.0, 'sum_HW_E2': 0.0, 'sum_HW_Installation': 0.0, }


        # Project Management. Get specific cost for PM.
        sum_PM = 0.0
        query_PM = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^1.0')
        for item in query_PM:
            sum_PM += item.cost

        # Project Commercial. Get specific cost for CPM.
        sum_CPM = 0.0
        query_CPM = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^96..')
        for item in query_CPM:
            sum_CPM += item.cost


        # GENERAL INCLUDING PM AND CPM
        # Querry fetches and filters all elements related to General section. Sum is stored in sum_Dict['sum_General']

        query_General = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).\
            filter(posd__hgpos__regex=r'^[1-8]..\y')
        for item in query_General:
            sum_Dict['sum_General'] += item.cost
        sum_Dict['sum_General'] += sum_CPM


        # MISC ENGINEERING
        # Query fetches and filters all elements related to Engineering
        query_Eng_Misc = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^10[1-6]0')
        for item in query_Eng_Misc:
            sum_Dict['sum_Eng_Misc'] += item.cost

        # BASIC ENGINEERING
        query_Basic_Eng = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^11..')
        for item in query_Basic_Eng:
            sum_Dict['sum_Basic_Eng'] += item.cost

        # DETAIL ENGINEERING
        query_Detail_Eng = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^12..')
        for item in query_Detail_Eng:
            sum_Dict['sum_Detail_Eng'] += item.cost

        # CUSTOMER DOCUMENTATION
        query_Cust_Docu = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^13..')
        for item in query_Cust_Docu:
            sum_Dict['sum_Cust_Docu'] += item.cost

        # UNIT CONTROL
        query_Unit_Control = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^14..')
        for item in query_Unit_Control:
            sum_Dict['sum_Unit_Control'] += item.cost

        # MEASUREMENT ANALYSIS
        query_Measurement = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^15..')
        for item in query_Measurement:
            sum_Dict['sum_Measurement'] += item.cost

        # INTERFACE FOREIGN SYSTEM
        query_Int_Foreign_Sys = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^16..')
        for item in query_Int_Foreign_Sys:
            sum_Dict['sum_Int_Foreign_Sys'] += item.cost

        # BASIC ENGINEERING ETEC
        query_Basic_Eng_E = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^17..')
        for item in query_Basic_Eng_E:
            sum_Dict['sum_Basic_Eng'] += item.cost

        # DETAIL ENGINEERING ETEC
        query_Detail_Eng_E = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^18..')
        for item in query_Detail_Eng_E:
            sum_Dict['sum_Detail_Eng_E'] += item.cost

        # FAT
        query_FAT = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^19..')
        for item in query_FAT:
            sum_Dict['sum_FAT'] += item.cost

        # SERVICE AND HARDWARE FOR INSTALLATION
        query_Installation = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^2...')
        for item in query_Installation:
            sum_Dict['sum_Installation'] += item.cost

        # COMMISSIONING
        query_Commissioning = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^3...')
        for item in query_Commissioning:
            sum_Dict['sum_Commissioning'] += item.cost

        # HW PERIPHERALS
        query_HW_Peri = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^4...')
        for item in query_HW_Peri:
            sum_Dict['sum_HW_Peri'] += item.cost

        # HW FOR CENTRAL / DISTRIBUTED I&C
        query_HW_DCS = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^5...')
        for item in query_HW_DCS:
            sum_Dict['sum_HW_DCS'] += item.cost

        # HW ET1
        query_HW_E1 = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^6...')
        for item in query_HW_E1:
            sum_Dict['sum_HW_E1'] += item.cost

        # HW ET2
        query_HW_E2 = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^7...')
        for item in query_HW_E2:
            sum_Dict['sum_HW_E2'] += item.cost

        # HW FOR INSTALLATION
        query_HW_Installation = t3000_objects.filter(kbmeta__pid__iexact=str(pid)).filter(posd__hgpos__regex=r'^8...')
        for item in query_HW_Installation:
            sum_Dict['sum_HW_Installation'] += item.cost

        return sum_Dict


def createDetailProjectGraphic(pid):
    '''
    This function takes the interim functions from sum_calculation and plots
    a StackedBar. Items below a certain amount will be shifted to 'MISC'
    in order not to overblow the chart
    '''

    t3000_objects = T3000db.objects
    # This is noly needed in order to give appropiate names to the graph.
    dict_Names = {'sum_General': 'General','sum_Eng_Misc': 'Eng. Misc.', 'sum_Basic_Eng': 'Basic Eng.',
                  'sum_Detail_Eng': 'Detail Eng.',
                  'sum_Cust_Docu': 'Customer Doc.', 'sum_Unit_Control': 'Unit Control',
                  'sum_Measurement': 'Measurement',
                  'sum_Int_Foreign_Sys': 'Inteface', 'sum_Basic_Eng_E': 'Basic Eng. E.',
                  'sum_Detail_Eng_E': 'Detail Eng. E.',
                  'sum_FAT': 'FAT', 'sum_Installation': 'Installation', 'sum_Commissioning': 'Commissioning',
                  'sum_HW_Peri': 'HW Peripheral', 'sum_HW_DCS': 'HW DCS', 'sum_HW_E1': 'HW ETEC 1',
                  'sum_HW_E2': 'HW ETEC 2', 'sum_HW_Installation': 'HW Installation',}


    sum_Dict = {}
    sum_Dict = sum_calculation(pid, t3000_objects)

    sum_Misc = 0.0

    # Variables for the chart. Getting name and value.
    # Idea: Only show section of KBSUMME where cost are calculated.
    # In order not to show every minor cost, it can be adjusted with the Misc section.
    # If sum in sum_Dict is smaller than X (see value below), it shall be put into Misc.
    chart_Name = []
    chart_Value = []

    # In this loop it is decided which section will be shown in the graph, and which to be put in misc. section
    for value in sum_Dict:
        if sum_Dict[value] < 20000.0:
            sum_Misc += sum_Dict[value]
        else:
            chart_Name.append(dict_Names[value])
            chart_Value.append(sum_Dict[value])

    if sum_Misc > 0.0:
        chart_Name.append('Misc')
        chart_Value.append(sum_Misc)

    chartStacked = pygal.StackedBar(interpolate='cubic', style=BlueStyle)

    chartStacked.title = projectName(pid)

    for i in range(0, len(chart_Name)):
        chartStacked.add(chart_Name[i], chart_Value[i])

    # Ploting the graph cost of each item in datafield chart_data, in a stacked bar chart.

    fname = 'media/Graph_stacked_' + str(pid) + '.svg'
    chartStacked.render_to_file(fname)

    return

def projectName(pid):
    kbmeta_objects = KbMeta.objects
    query_title = kbmeta_objects.filter(pid__iexact=str(pid))
    get_title = query_title.get()
    return get_title.projname
