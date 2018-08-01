from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.storage import FileSystemStorage
from django.utils import timezone
import os
import openpyxl


from .models import Posd, T3000db, KbMeta, Stueckliste
from .project_graph import createDetailProjectGraphic
from .io_statistic import iograph, total_IO


#global variables objects
t3000_inst = T3000db() # Same as post_inst
kbmeta_objects = KbMeta.objects
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def home(request):
    t3000_objects = T3000db.objects
    iograph()
    '''
    query_total = t3000_objects.filter(posd__hgpos__regex=r'^(10000)\y')
    query_dict = {'totalcost': [0.0], 'projname':['Test'], 'customer':['SK'],
    'datecalc':['2017-01-01'], 'ExcelCalc': ['file'], 'dateupload':['2017-01-02'] }
    '''

    return render(request, 'kbsumme/home.html', {'kbmetaobj': kbmeta_objects.all(),})

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
    '''

    kbmeta_inst = KbMeta()
    posd_objects = Posd.objects

    #try:
    wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
    ws = wb['KBSUMME']
    #except:
    #    print('Error: Could not read workbook or worksheet')
    #    print('Please check if worksheet KBSUMME exists')
    #    return render(request, 'kbsumme/upT3000.html', {
    #        'error': 'Workbook could not be loaded or worksheet could not be read', 't3000_objects': t3000_objects})

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

    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['Stueckliste']
    except:
        print('Error: Could not read workbook or worksheet')
        print('Please check if worksheet Stueckliste exists')
        return render(request, 'kbsumme/upT3000.html', {
            'error': 'Workbook could not be loaded or worksheet could not be read'})

    stueckl_inst = Stueckliste()
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
        stueckl_inst.pk = None
        stueckl_inst.save()

    createDetailProjectGraphic(ws['G2'].value, t3000_objects)
    return query_obj

def projectStat(request, pid=205819):
    t3000_obj = T3000db.objects
    obj = get_object_or_404(kbmeta_objects, pid__iexact=str(pid))

    createDetailProjectGraphic(pid, t3000_obj)
    return render(request, 'kbsumme/projectStat.html', {'obj':obj})

def projectlist(request):
    return render(request, 'kbsumme/projectlist.html', {'kbmeta_obj':kbmeta_objects})

def iocount(request):
    return render(request, 'kbsumme/iostat.html')

def upPBB(request):
    if request.method == 'POST':
        if (bool(request.FILES.get('myfile', False)) == True) and (bool(int(request.POST['pid'])) == True):
            myfile = request.FILES['myfile']
            pid = request.POST['pid']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name.replace(" ", ""), myfile)
            uploaded_file_url = fs.url(filename)
            upPBBFunc(request, uploaded_file_url, pid)
            #query_pid = kbmeta_objects.get(pid__iexact=str(pid))
            return render(request, 'kbsumme/upPBB.html', {'kbmetaobj':kbmeta_objects})

        return render(request, 'kbsumme/upPBB.html', {'kbmetaobj':kbmeta_objects})

    else:
        return render(request, 'kbsumme/upPBB.html', {'kbmetaobj':kbmeta_objects})

def upPBBFunc(request, file, pid):
    '''
    Read in the calculation sheet. First right wor is searched based on word
    'Business'. Linenumber is sotred in headline. Afterwards the 'Indidvidual Amount'
    field is searched and right column will be stored var col_total.

    Once found, values will be stored to database.
    '''
    kbmeta_inst = KbMeta()

    #try:
    wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
    ws = wb['calculation']
    #except:
    #    print('Error: Could not read workbook or worksheet')
    #    print('Please check if worksheet calculation exists')
    #    return render(request, 'kbsumme/upPBB.html', {
    #        'error': 'Workbook could not be loaded or worksheet could not be read', 't3000_objects': t3000_objects})


    #Search for the right line in the calculation sheet. Once found remember
    #line number in var headline

    pbb_inst = Pbb()
    # Generate list with alphabet A-Z
    col_list = list(map(chr, range(65, 90)))

    #Find cell for offerno from A1 to Z23
    i=0
    for col in col_list:
        i+=1
        #Goes through each column A to Z and do following:
        for row in range(1,23):
            #Goes through each row
            if 'offer' in ws['{}{}'.format(col, row)].value:
                cell_offerno = col_list[i+1] + str(row)
            if 'forex' in ws['{}{}'.format(col, row)].value:
                cell_forex = col_list[i+1] + str(row)


    pbbmeta_inst = PbbMeta()
    pbbmeta_inst.offer_no = ws['{}'.format(cell_offerno)].value
    pbbmeta_inst.projname = ws['{}'.format()].value #TODO: Put the cell reference here
    pbbmeta_inst.customer = ws['{}'.format()].value #TODO: Put the cell reference here as well
    pbbmeta_inst.fx_rate = ws['{}'.format(cell_forex)].value

    #pbbmeta_inst.country_inst =
    #pbbmeta_inst.planttype =
    #pbbmeta_inst.qty_units =
    #pbbmeta_inst.total_output =
    #pbbmeta_inst.endcustomer =
    #pbbmeta_inst.bidmanager =

    pbbmeta_inst.pk = None
    pbbmeta_inst.kbmeta = kbmeta_inst
    pbbmeta_inst.save()

    row = 0
    while i < ws.max_row:
        i+=1
        if row == 0 and 'Business' in str(ws['A{}'.format(i)].value):
            row = i
            break

    #If row with 'Business' could not be found. Print message to user
    if row == 0:
        return render(request, 'kbsumme/upPBB.html', {
            'error': 'Could not find headline "Business" in the sheet calculation'
        })
    #Search for the right column in the calculation sheet. Once found remember db_column
    #in var col_total.
    col = ''
    col_len = 0
    while col_len < 27:
        if 'Individual' in str(ws['{}{}'.format(col_list[col_len], row)].value):
            col = col_list[col_len]
            break
        col_len += 1

        #Steht im Feld Single kost etwas drin und steht im B#headline 'T3000
        #oder Hardware' dann lese die Werte aus Spalte B ein.

    pbbmeta_inst = PbbMeta()
    offset = [1,3,4,5,8,9,10,11,12,13,14,17,18,23,26,31]
    i=0
    while i < (col_len): #Loop all columns
        i+=1
        if ws['{}{}'.format(col_list[i],(row+offset[13]))].value: #Check if field single cost contains some value
            #while ii < len(offset): #Loop all rows
            if ('T3000' in ws['{}{}'.format(col_list[i],row)].value) or ('Hardware' in ws['{}{}'.format(col_list[i],row)].value):
                pbb_inst.kind_of_business = 'T3000 Hardware'
            elif ('Engineering' in ws['{}{}'.format(col_list[i],row)].value):
                pbb_inst.kind_of_business = 'SLI Engineering'
            elif ('PM' in ws['{}{}'.format(col_list[i],row)].value) or ('CPM' in ws['{}{}'.format(col_list[i],row)].value):
                pbb_inst.kind_of_business = 'PM/CPM'
            elif ('Furniture' in ws['{}{}'.format(col_list[i],row)].value):
                pbb_inst.kind_of_business = 'Furniture, Printer, Monitor'
            else:
                pbb_inst.kind_of_business = ws['{}{}'.format(col_list[i],row)].value

            pbb_inst.entity = ws['{}{}'.format(col_list[i],(row+offset[0]))].value
            pbb_inst.escalation = ws['{}{}'.format(col_list[i],(row+offset[1]))].value
            pbb_inst.transportation = ws['{}{}'.format(col_list[i],(row+offset[2]))].value
            pbb_inst.custom = ws['{}{}'.format(col_list[i],(row+offset[3]))].value
            pbb_inst.tax = ws['{}{}'.format(col_list[i],(row+offset[4]))].value
            pbb_inst.fx_gain_loss = ws['{}{}'.format(col_list[i],(row+offset[5]))].value
            pbb_inst.financing = ws['{}{}'.format(col_list[i],(row+offset[6]))].value
            pbb_inst.insurance = ws['{}{}'.format(col_list[i],(row+offset[7]))].value
            pbb_inst.bank_charges = ws['{}{}'.format(col_list[i],(row+offset[8]))].value
            pbb_inst.technical_risk = ws['{}{}'.format(col_list[i],(row+offset[9]))].value
            pbb_inst.warranty = ws['{}{}'.format(col_list[i],(row+offset[10]))].value
            pbb_inst.sales_oh = ws['{}{}'.format(col_list[i],(row+offset[11]))].value
            pbb_inst.net_margin = ws['{}{}'.format(col_list[i],(row+offset[12]))].value
            pbb_inst.single_cost_euro = ws['{}{}'.format(col_list[i],(row+offset[13]))].value
            pbb_inst.price = ws['{}{}'.format(col_list[i],(row+offset[14]))].value
            pbb_inst.price_nego = ws['{}{}'.format(col_list[i],(row+offset[15]))].value
            #ii += 1

            pbb_inst.total_surcharges = ws['{}{}'.format(col_list[col_len],(row+7))].value
            pbb_inst.total_includings = ws['{}{}'.format(col_list[col_len],(row+16))].value
            pbb_inst.total_sm = ws['{}{}'.format(col_list[col_len],(row+19))].value
            pbb_inst.total_cost = ws['{}{}'.format(col_list[col_len],(row+23))].value
            pbb_inst.total_price_euro = ws['{}{}'.format(col_list[col_len],(row+26))].value
            pbb_inst.total_price_fx = ws['{}{}'.format(col_list[col_len+1],(row+26))].value

            pbb_inst.pbbmeta = pbbmeta_inst
            pbb_inst.pk = None
            pbb_inst.save()
