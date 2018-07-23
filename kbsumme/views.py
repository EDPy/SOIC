from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import os

import openpyxl
import matplotlib.path as plt
import pygal

from .models import Posd, T3000db, KbMeta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
posd_inst = Posd()  #Is an instance of class Posd to read into the database
posd_objects = Posd.objects # Is an object to pass all objects to html to list items in table format
t3000_inst = T3000db() # Same as post_inst
t3000_objects = T3000db.objects # Same as poad_object
kbmeta_inst = KbMeta()
kbmeta_objects = KbMeta.objects

def home(request):
    return render(request, 'kbsumme/home.html', {'kbmetaobj': kbmeta_objects.all()})

def upPosd(request):
    ''' After form sumitted in html 'POST', it will be catched here and evaluated
    This method checks if file has been passed if yes it forwards it to upPosdFunc.
    Afterwards html is opened with updated information.

    If file was not selected, error message will occur.
    If browser is only refreshed (updated), content will be shown, no error.. See last return render
    '''
    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name.replace(" ", ""), myfile)
            uploaded_file_url = fs.url(filename)
            upPosdFunc(request, uploaded_file_url)
            return render(request, 'kbsumme/upPosd.html', {
                'uploaded_file_url': uploaded_file_url,
                'success':'File successful loaded', 'posd_objects':posd_objects,})
        else:
            return render(request, 'kbsumme/upPosd.html', {
                'error':'Please select a file to upload', 'posd_objects': posd_objects,})
    else:
        return render(request, 'kbsumme/upPosd.html', {'posd_objects': posd_objects, })

def upPosdFunc(request, file):
    '''
    workbook will be opened, worsheet assigned. If not successfull error message will occur in the terminal.
    Otherwise all files are read into the Posd database. Filled in with data from the worksheet on pre-defined
    fields. Here: A2-A204, B2-B204, C2-C204, D2-D204, E2-E204

    :param file:
    :return:
    '''
    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True)
        ws = wb['T1_general']
    except:
        print('Error: Could not read workbook or worksheet')
        print('Please check if worksheet KBSUMME exists')
        return

    # Fetching excel sheet and stores into database.
    i=1 #Starts with number 2 to fetch data. Row 1 is the table header.
    #try:
    while i < ws.max_row:
        i+=1
        hg = str(ws['A{}'.format(i)].value)

        if len(str(ws['B{}'.format(i)].value)) == 1:
            pos = '0' + str(ws['B{}'.format(i)].value)
        else:
            pos = str(ws['B{}'.format(i)].value)

        hgpos = hg+pos
        posd_inst.hgpos = int(hgpos)
        if ws['C{}'.format(i)].value:
            posd_inst.description = ws['C{}'.format(i)].value
        if ws['D{}'.format(i)].value:
            posd_inst.hours = ws['D{}'.format(i)].value
        if ws['E{}'.format(i)].value:
            posd_inst.cost = ws['E{}'.format(i)].value
        #posd_inst.pk = None
        posd_inst.save()
"""
    except:
        return render(request, 'kbsumme/upPosd.html', {
            'error': 'Integrity Error, Project ID already exist in database', 'posd_objects': posd_objects})
        #TODO Does not show ERROR message on HTML page
"""

def upT3000_Meta(request):
    '''
    KBSUMME sheet will be read into database. First check if form request 'POST' otherwise error or
    just refresh (update) browser. Main database entry will happen in function upT3000Func.
    :param request:
    :return:
    '''

    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name.replace(" ", ""), myfile)
            print(filename)
            uploaded_file_url = fs.url(filename)
            upT3000Func(request, uploaded_file_url)
            return render(request, 'kbsumme/upT3000.html', {
        'uploaded_file_url': uploaded_file_url,
        'success': 'File successful loaded', 't3000_objects': t3000_objects, })
        else:
            return render(request, 'kbsumme/upT3000.html', {
            'error': 'Please select a file to upload', 't3000_objects': t3000_objects})

    else:
        return render(request, 'kbsumme/upT3000.html', {'t3000_objects': t3000_objects, })


def upT3000Func(request, file):
    '''
    Data will be read into database in table T3000db. Iteration of all items of KBSUMME based on Posd
    object-class-database. Important: Hours and Cost reference value in Posd must be right otherwise
    wrong data will be inserted into database.
    TODO: Some plausibility check to see if cell reference with ws[item.hours].value and ws[item.cost].value is right
    '''
    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['KBSUMME']
    except:
        print('Error: Could not read workbook or worksheet')
        print('Please check if worksheet KBSUMME exists')
        return render(request, 'kbsumme/upT3000.html', {
            'error': 'Workbook could not be loaded or worksheet could not be read', 't3000_objects': t3000_objects})

    #Fill in the META data to kbmeta database
    #PID, quotno, dateupload, filename cant be empty NULL or not allwed to be emtpy:
    kbmeta_inst.pid = ws['G2'].value
    kbmeta_inst.quotno = ws['G2'].value
    kbmeta_inst.dateupload = timezone.datetime.now()
    kbmeta_inst.filename = file

    #Values which can be empty. In this case value will output NULL, which is set to not allowed.
    #For char we only accept emtpy string, otherwise double meaning with NULL and empty string will be the case.
    if ws['S5'].value:
        kbmeta_inst.klaversion = ws['S5'].value
    if ws['S12'].value:
        kbmeta_inst.calcbase = ws['S12'].value
    if ws['S13'].value:
        kbmeta_inst.contractbase = ws['S13'].value
    if ws['G3'].value:
        kbmeta_inst.projname = ws['G3'].value
    if ws['G4'].value:
        kbmeta_inst.customer = ws['G4'].value
    if ws['G5'].value:
        kbmeta_inst.endcustomer = ws['G5'].value
    if ws['S4'].value:
        kbmeta_inst.datecalc = ws['S4'].value

    kbmeta_inst.save()

    # Fill in the hours and cost from excel KBSUMME.
    for item in posd_objects.all():
        if item.hours:
            t3000_inst.hours = float(ws[item.hours].value)
        if item.cost:
            t3000_inst.cost = float(ws[item.cost].value)
        t3000_inst.pid = kbmeta_inst
        t3000_inst.hgpos = item
        t3000_inst.pk = None
        t3000_inst.save()

    createDetailProjectGraphic(ws['G2'].value)

def projectStat(request, pid=205819):
    obj = get_object_or_404(kbmeta_objects, pid__iexact=str(pid))
    #createDetailProjectGraphic(pid)
    return render(request, 'kbsumme/projectStat.html', {'obj':obj})

def createProjectGraphic(pid):
    '''
    Chart will be generated right after KBSUMME sheet has been uploaded.
    Generate a bar chart with following information:
    - Cost of General activities TODO PM has to be changed to General activities, see below SQL Query
    - Cost of Engineering
    - Cost of Hardware
    '''

    chart_data = []
    chartStacked = pygal.StackedBar()
    chartStacked.title = 'Project Cost Structure'

    #TODO I am not sure if the below filter always will deliver only one value!
    # Generating Querry for PM, ENGINEERING and HARDWARE
    query_PM = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='1').filter(pos__iexact='10')
    query_Engineering = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='100').filter(pos__iexact='1')
    query_Hardware = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='100').filter(pos__iexact='2')

    qPM = query_PM.get()
    qEng = query_Engineering.get()
    qHW = query_Hardware.get()

    chartStacked.add('Project Management', qPM.cost)
    chartStacked.add('Engineering', qEng.cost)
    chartStacked.add('Hardware', qHW.cost)

    chart_data.append(qPM.cost)
    chart_data.append(qEng.cost)
    chart_data.append(qHW.cost)


    # Ploting the graph cost of each item in datafield chart_data, in a stacked bar chart.
    chart = pygal.StackedBar()
    chart.title = 'Cost Structure'

    #chart.x_labels = ('PM', 'Engineering', 'Hardware') #X-Labels like General, Engineering, Hardware
    chart.add('Project A', chart_data)
    fname = 'media/project_cost_'+str(pid)+'.svg'
    fname1 = 'media/project_cost_stacked'+str(pid)+'.svg'
    chart.render_to_file(fname)
    chartStacked.render_to_file(fname1)
    return


def projectName(pid):
    query_title = kbmeta_objects.filter(pid__iexact=str(pid))
    get_title = query_title.get()
    return get_title.projname

def createDetailProjectGraphic(pid):
    '''
        More detail cost calculation method. To be loaded right after KBSUMME upload.
        Generate a stackedbar chart with following information:
        - Cost of General activities
        - Misc Engineering
        - Cost of Basic Engineering
        - Cost of Detail Engineering
        - Customer Documentation
        - Unit Control
        - Measurement analysis
        - Interface to foreign systems
        - Basic E-Technology
        - Detail E-Technology
        - FAT
        - Installation
        - Commissioning
        - HW peripherals
        - HW DCS
        - HW ET1
        - HW ET2
        - HW Installation
        '''

    #This variable contains all ellements the sum of groups, e.g. basi enginering, hardware components etc.
    sum_Dict = {'sum_Eng_Misc':0.0, 'sum_Basic_Eng':0.0, 'sum_Detail_Eng':0.0, 'sum_Cust_Docu':0.0, 'sum_Unit_Control':0.0,
                'sum_Measurement':0.0, 'sum_Int_Foreign_Sys':0.0, 'sum_Basic_Eng_E':0.0, 'sum_Detail_Eng_E':0.0,
                'sum_FAT':0.0, 'sum_Installation':0.0, 'sum_Commissioning':0.0, 'sum_HW_Peri':0.0,
                'sum_HW_DCS':0.0, 'sum_HW_E1':0.0, 'sum_HW_E2':0.0, 'sum_HW_Installation':0.0, 'sum_General':0.0}

    #This is noly needed in order to give appropiate names to the graph.
    dict_Names = {'sum_Eng_Misc': 'Eng. Misc.', 'sum_Basic_Eng': 'Basic Eng.', 'sum_Detail_Eng': 'Detail Eng.',
                  'sum_Cust_Docu': 'Customer Doc.', 'sum_Unit_Control': 'Unit Control', 'sum_Measurement': 'Measurement',
                  'sum_Int_Foreign_Sys': 'Inteface', 'sum_Basic_Eng_E': 'Basic Eng. E.', 'sum_Detail_Eng_E': 'Detail Eng. E.',
                  'sum_FAT': 'FAT', 'sum_Installation': 'Installation', 'sum_Commissioning': 'Commissioning',
                  'sum_HW_Peri': 'HW Peripheral', 'sum_HW_DCS': 'HW DCS', 'sum_HW_E1': 'HW ETEC 1',
                  'sum_HW_E2': 'HW ETEC 2', 'sum_HW_Installation': 'HW Installation', 'sum_General':'General'}


    # Project Management. Get specific cost for PM.
    sum_PM = 0.0
    query_PM = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^1.0')
    for item in query_PM:
        sum_PM += item.cost

    # Project Commercial. Get specific cost for CPM.
    sum_CPM = 0.0
    query_CPM = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^96..')
    for item in query_CPM:
        sum_CPM += item.cost

    # GENERAL INCLUDING PM AND CPM
    # Querry fetches and filters all elements related to General section. Sum is stored in sum_Dict['sum_General']
    querry_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^[1-8].[0,1]')
    for item in querry_General:
        sum_Dict['sum_General'] += item.cost
    sum_Dict['sum_General'] += sum_CPM


    '''    
    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='2')
    for item in query_General:
        sum_General += item.cost
    
    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='3')
    for item in query_General:
        sum_General += item.cost
    
    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='4')
    for item in query_General:
        sum_General += item.cost

    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='5')
    for item in query_General:
        sum_General += item.cost

    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='6')
    for item in query_General:
        sum_General += item.cost

    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='7')
    for item in query_General:
        sum_General += item.cost

    query_General = t3000_objects.filter(pid__iexact=str(pid)).filter(hg__iexact='8')
    for item in query_General:
        sum_General += item.cost
'''



    # MISC ENGINEERING
    # Querry fetches and filters all elements related to Engineering
    query_Eng_Misc = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^10..')
    for item in query_Eng_Misc:
        sum_Dict['sum_Eng_Misc'] += item.cost

    # BASIC ENGINEERING
    query_Basic_Eng = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^11..')
    for item in query_Basic_Eng:
        sum_Dict['sum_Basic_Eng'] += item.cost

    # DETAIL ENGINEERING
    query_Detail_Eng = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^12..')
    for item in query_Detail_Eng:
        sum_Dict['sum_Detail_Eng'] += item.cost

    # CUSTOMER DOCUMENTATION
    query_Cust_Docu = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^13..')
    for item in query_Cust_Docu:
        sum_Dict['sum_Cust_Docu'] += item.cost

    # UNIT CONTROL
    query_Unit_Control = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^14..')
    for item in query_Unit_Control:
        sum_Dict['sum_Unit_Control'] += item.cost

    # MEASUREMENT ANALYSIS
    query_Measurement = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^15..')
    for item in query_Measurement:
        sum_Dict['sum_Measurement'] += item.cost

    # INTERFACE FOREIGN SYSTEM
    query_Int_Foreign_Sys = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^16..')
    for item in query_Int_Foreign_Sys:
        sum_Dict['sum_Int_Foreign_Sys'] += item.cost

    # BASIC ENGINEERING ETEC
    query_Basic_Eng_E = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^17..')
    for item in query_Basic_Eng_E:
        sum_Dict['sum_Basic_Eng'] += item.cost

    # DETAIL ENGINEERING ETEC
    query_Detail_Eng_E = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^18..')
    for item in query_Detail_Eng_E:
        sum_Dict['sum_Detail_Eng_E'] += item.cost

    # FAT
    query_FAT = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^19..')
    for item in query_FAT:
        sum_Dict['sum_FAT'] += item.cost

    # SERVICE AND HARDWARE FOR INSTALLATION
    query_Installation = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^2...')
    for item in query_Installation:
        sum_Dict['sum_Installation'] += item.cost

    # COMMISSIONING
    query_Commissioning = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^3...')
    for item in query_Commissioning:
        sum_Dict['sum_Commissioning'] += item.cost

    # HW PERIPHERALS
    query_HW_Peri = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^4...')
    for item in query_HW_Peri:
        sum_Dict['sum_HW_Peri'] += item.cost

    # HW FOR CENTRAL / DISTRIBUTED I&C
    query_HW_DCS = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^5...')
    for item in query_HW_DCS:
        sum_Dict['sum_HW_DCS'] += item.cost

    # HW ET1
    query_HW_E1 = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^6...')
    for item in query_HW_E1:
        sum_Dict['sum_HW_E1'] += item.cost

    # HW ET2
    query_HW_E2 = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^7...')
    for item in query_HW_E2:
        sum_Dict['sum_HW_E2'] += item.cost

    # HW FOR INSTALLATION
    query_HW_Installation = t3000_objects.filter(pid__iexact=str(pid)).filter(hgpos__regex=r'^8...')
    for item in query_HW_Installation:
        sum_Dict['sum_HW_Installation'] += item.cost



    sum_Misc = 0.0

    # Variables for the chart. Getting name and value.
    # Idea: Only show section of KBSUMME where cost are calculated.
    # In order not to show every minor cost, it can be adjusted with the Misc section.
    # If sum in sum_Dict is smaller than X (see value below), it shall be put into Misc.
    chart_Name = []
    chart_Value = []


    # In this loop it is decided which section will be shown in the graph, and which to be put in misc. section
    for value in sum_Dict:
        if sum_Dict[value] < 10.0:
            sum_Misc += sum_Dict[value]
        else:
            chart_Name.append(dict_Names[value])
            chart_Value.append(sum_Dict[value])

    if sum_Misc > 0.0:
        chart_Name.append('Misc')
        chart_Value.append(sum_Misc)

    print(chart_Name)
    print(chart_Value)
    print(sum(chart_Value))
    chartStacked = pygal.StackedBar()


    chartStacked.title = projectName(pid)


    for i in range(0,len(chart_Name)):
        chartStacked.add(chart_Name[i], chart_Value[i])


    # Ploting the graph cost of each item in datafield chart_data, in a stacked bar chart.

    fname = 'media/Graph_stacked_' + str(pid) + '.svg'
    chartStacked.render_to_file(fname)

    return