from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import os
import openpyxl


from .models import Posd, T3000db, KbMeta #, Stueckliste
from .project_graph import createDetailProjectGraphic

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

t3000_inst = T3000db() # Same as post_inst
kbmeta_objects = KbMeta.objects
#stueckl_inst = Stueckliste()

def home(request):
    return render(request, 'kbsumme/home.html', {'kbmetaobj': kbmeta_objects.all()})

def upPosd(request):
    ''' After form sumitted in html 'POST', it will be catched here and evaluated
    This method checks if file has been passed if yes it forwards it to upPosdFunc.
    Afterwards html is opened with updated information.

    If file was not selected, error message will occur.
    If browser is only refreshed (updated), content will be shown, no error.. See last return render
    '''
    posd_objects = Posd.objects  # Is an object to pass all objects to html to list items in table format

    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name.replace(" ", ""), myfile)
            uploaded_file_url = fs.url(filename)
            upPosdFunc(request, uploaded_file_url, posd_objects)
            return render(request, 'kbsumme/upPosd.html', {
                'uploaded_file_url': uploaded_file_url,
                'success':'File successful loaded', 'posd_objects':posd_objects,})
        else:
            return render(request, 'kbsumme/upPosd.html', {
                'error':'Please select a file to upload', 'posd_objects': posd_objects,})
    else:
        return render(request, 'kbsumme/upPosd.html', {'posd_objects': posd_objects, })

def upPosdFunc(request, file, posd_objects):
    '''
    workbook will be opened, worsheet assigned. If not successfull error message will occur in the terminal.
    Otherwise all files are read into the Posd database. Filled in with data from the worksheet on pre-defined
    fields. Here: A2-A204, B2-B204, C2-C204, D2-D204, E2-E204
    '''
    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True)
        ws = wb['T1_general']
    except:
        print('Error: Could not read workbook or worksheet')
        print('Please check if worksheet KBSUMME exists')
        return

    posd_inst = Posd()  # Is an instance of class Posd to read into the database

    # Fetching excel sheet and stores into database.
    i=1 #Starts with number 2 to fetch data. Row 1 is the table header.
    try:
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
            posd_inst.pk = None
            posd_inst.save()

    except:
        return render(request, 'kbsumme/upPosd.html', {
            'error': 'Integrity Error, Project ID already exist in database', 'posd_objects': posd_objects})
        #TODO Does not show ERROR message on HTML page


def upT3000_Meta(request):
    '''
    KBSUMME sheet will be read into database. First check if form request 'POST' otherwise error or
    just refresh (update) browser. Main database entry will happen in function upT3000Func.
    '''

    t3000_objects = T3000db.objects  # Same as poad_object

    if request.method == 'POST':
        if request.FILES:
            myfile = request.FILES['myfile']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name.replace(" ", ""), myfile)
            print(filename)
            uploaded_file_url = fs.url(filename)
            query_obj = upT3000Func(request, uploaded_file_url, t3000_objects)
            return render(request, 'kbsumme/upT3000.html', {
        'uploaded_file_url': uploaded_file_url,
        'success': 'File successful loaded', 't3000_objects': query_obj})
        else:
            return render(request, 'kbsumme/upT3000.html', {
            'error': 'Please select a file to upload'})

    else:
        return render(request, 'kbsumme/upT3000.html')


def upT3000Func(request, file, t3000_objects):
    '''
    Data will be read into database in table T3000db. Iteration of all items of KBSUMME based on Posd
    object-class-database. Important: Hours and Cost reference value in Posd must be right otherwise
    wrong data will be inserted into database.
    TODO: Some plausibility check to see if cell reference with ws[item.hours].value and ws[item.cost].value is right
    '''

    kbmeta_inst = KbMeta()
    posd_objects = Posd.objects

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

    kbmeta_inst.pk = None
    kbmeta_inst.save()

    # Fill in the hours and cost from excel KBSUMME.
    for item in posd_objects.all():
        if item.hours:
            t3000_inst.hours = float(ws[item.hours].value)
        if item.cost:
            t3000_inst.cost = float(ws[item.cost].value)
        t3000_inst.kbmeta = kbmeta_inst
        t3000_inst.posd = item
        t3000_inst.pk = None
        t3000_inst.save()

    query_obj = t3000_objects.filter(kbmeta__pid__iexact=str(t3000_inst.kbmeta.pid))
    #stueckliste_func(file)
    createDetailProjectGraphic(ws['G2'].value, t3000_objects)
    return query_obj

'''
def stueckliste_func(file):
    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['Stueckliste']
    except:
        print('Error: Could not read workbook or worksheet')
        print('Please check if worksheet KBSUMME exists')
        return render(request, 'kbsumme/upT3000.html', {
            'error': 'Workbook could not be loaded or worksheet could not be read', 't3000_objects': t3000_objects})

    i = 1
    while i < ws.max_row:
        i+=1

        if ws['A{}'.format(i)].value:
            stueckl_inst.module = ws['A{}'.format(i)].value
        if ws['B{}'.format(i)].value:
            stueckl_inst.sheet = ws['B{}'.format(i)].value
        if ws['C{}'.format(i)].value:
            stueckl_inst.caname = ws['C{}'.format(i)].value
        if ws['D{}'.format(i)].value:
            stueckl_inst.description = ws['D{}'.format(i)].value
        if ws['E{}'.format(i)].value:
            stueckl_inst.mlfb = ws['E{}'.format(i)].value
        if ws['F{}'.format(i)].value:
            stueckl_inst.qty = ws['F{}'.format(i)].value
        if ws['G{}'.format(i)].value:
            stueckl_inst.single_cost = ws['G{}'.format(i)].value
        if ws['H{}'.format(i)].value:
            stueckl_inst.typical = ws['H{}'.format(i)].value
        if ws['I{}'.format(i)].value:
            stueckl_inst.total_cost = ws['I{}'.format(i)].value

        stueckl_inst.kbmeta = kbmeta_inst
        #posd_inst.pk = None
        stueckl_inst.save()
'''


def projectStat(request, pid=205819):
    t3000_obj = T3000db.objects
    obj = get_object_or_404(kbmeta_objects, pid__iexact=str(pid))
    createDetailProjectGraphic(pid, t3000_obj)
    return render(request, 'kbsumme/projectStat.html', {'obj':obj})


def projectlist(request):
    return render(request, 'kbsumme/projectlist.html', {'kbmeta_obj':kbmeta_objects})