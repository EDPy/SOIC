def uploadFunc(file, formdict):
    '''
    Data will be read into database in table T3000db. Iteration of all items of KBSUMME based on Posd
    object-class-database. Important: Hours and Cost reference value in Posd must be right otherwise
    wrong data will be inserted into database.
    '''

    kbmeta_inst = KbMeta()
    posd_objects = Posd.objects
    r = {'code':0, 'message':''}

    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['KBSUMME']
    except:
        r['code'] = 1
        r['message'] = 'Workbook could not be loaded or worksheet KBSUMME could not be read'
        return r

    '''
    #Not understandable for me why I try to open the stueckliste here as well.
        if formdict['box_stckl']:
            try:
                ws = wb['Stueckliste']
            except:
                r['code'] = 1
                r['message'] = 'Workbook Stueckliste could not be loaded or worksheet could not be read'
                return r
    '''

    #Fill in the META data to kbmeta database
    #PID, quotno, dateupload, filename cant be empty NULL or not allwed to be emtpy:
    kbmeta_inst.pid = formdict['pid'] #ws['G2'].value
    kbmeta_inst.quotno = ws['G2'].value
    kbmeta_inst.dateupload = timezone.datetime.now()
    kbmeta_inst.filename = file
    kbmeta_inst.phase = formdict['proptype']

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

    #if ws['G4'].value:
    kbmeta_inst.customer = formdict['customer'] #ws['G4'].value

    if ws['G5'].value:
        kbmeta_inst.endcustomer = ws['G5'].value
    if ws['S4'].value:
        kbmeta_inst.datecalc = ws['S4'].value

    kbmeta_inst.pk = None
    kbmeta_inst.kbsumme = True
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


    if formdict['box_stckl']:
        r = pdupStckliste(file, kbmeta_inst.pid)

    if formdict['box_calc']:
        r = pdupPBBFunc(file, kbmeta_inst.pid)

    # This doesnt work. R will be overwritten every time. Dictonaries have
    # to collect-append the messages.

    createDetailProjectGraphic(formdict['pid'])
    return r



def upStueckliste(file, pid):

    r = {'code':0, 'message':''}
    stueckliste_objects = Stueckliste.objects
    query_stueckliste = stueckliste_objects.filter(kbmeta__pid__iexact=pid)

    if query_stueckliste:
        print('Eintrag vorhanden')
        r['code'] = 1
        r['message'] = 'Stueckliste for this project already in database'
        return r

    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['Stueckliste']
    except:
        r['code'] = 1
        r['message'] = 'Workbook could not be loaded or worksheet KBSUMME could not be read'
        return r

    kbmeta_inst = KbMeta()
    kbmeta_objects = KbMeta.objects
    query_kb = kbmeta_objects.get(pid__iexact=str(pid))
    stueckl_inst = Stueckliste()

    col_list = list(map(chr, range(65, 91)))
    chk_module = 0
    chk_sheet = 0
    chk_ca = 0
    chk_descr = 0
    chk_mlfb = 0
    chk_qty = 0
    chk_cost = 0
    chk_typ = 0
    chk_tcost = 0

    chk = 0
    rw=0

    # Figur out where the col and row for each element starts
    for row in range(5): # row
        if chk != 0:
            break
        rw+=1
        c = 0
        for col in col_list: # column
            if 'Module' in str(ws['{}{}'.format(col, row+1)].value):
                chk_module = c
                chk = 1
            if 'Sheet' in str(ws['{}{}'.format(col, row+1)].value):
                chk_sheet = c
            if 'CA-name' in str(ws['{}{}'.format(col, row+1)].value):
                chk_ca = c
            if 'Description' in str(ws['{}{}'.format(col, row+1)].value):
                chk_descr = c
            if 'MLFB' in str(ws['{}{}'.format(col, row+1)].value):
                chk_mlfb = c
            if 'Quantity' in str(ws['{}{}'.format(col, row+1)].value):
                chk_qty = c
            if 'Single costs' in str(ws['{}{}'.format(col, row+1)].value):
                chk_cost = c
            if 'Typical' in str(ws['{}{}'.format(col, row+1)].value):
                chk_typ = c
            if 'Total costs' in str(ws['{}{}'.format(col, row+1)].value):
                chk_tcost = c
            c+=1

    ''' # check on chk_module... == 0 doesnt work; c can be zero
    if chk_module == 0 or chk_sheet == 0 or chk_ca == 0 or chk_descr == 0 or\
    chk_mlfb == 0 or chk_qty == 0 or chk_cost == 0 or chk_typ == 0 or chk_tcost == 0:
        r['code'] = 1
        r['message'] = 'Could not find all column in the Stueckliste'
        return r
    '''

    while rw < ws.max_row:
        rw+=1 #rw is the row with the headline
        if ws['{}{}'.format(col_list[chk_module],rw)].value:
            stueckl_inst.module = ws['{}{}'.format(col_list[chk_module], rw)].value
        if ws['{}{}'.format(col_list[chk_sheet], rw)].value:
            stueckl_inst.sheet = ws['{}{}'.format(col_list[chk_sheet], rw)].value
        if ws['{}{}'.format(col_list[chk_ca], rw)].value:
            stueckl_inst.caname = ws['{}{}'.format(col_list[chk_ca], rw)].value
        if ws['{}{}'.format(col_list[chk_descr], rw)].value:
            stueckl_inst.description = ws['{}{}'.format(col_list[chk_descr], rw)].value
        if ws['{}{}'.format(col_list[chk_mlfb], rw)].value:
            stueckl_inst.mlfb = ws['{}{}'.format(col_list[chk_mlfb], rw)].value
        if ws['{}{}'.format(col_list[chk_qty], rw)].value:
            stueckl_inst.qty = ws['{}{}'.format(col_list[chk_qty], rw)].value
        if ws['{}{}'.format(col_list[chk_cost], rw)].value:
            stueckl_inst.single_cost = ws['{}{}'.format(col_list[chk_cost], rw)].value
        if ws['{}{}'.format(col_list[chk_typ], rw)].value:
            stueckl_inst.typical = ws['{}{}'.format(col_list[chk_typ], rw)].value
        if ws['{}{}'.format(col_list[chk_tcost], rw)].value:
            stueckl_inst.total_cost = ws['{}{}'.format(col_list[chk_tcost], rw)].value

        stueckl_inst.kbmeta = query_kb
        stueckl_inst.pk = None
        stueckl_inst.kbmeta.stckliste = True #TODO Does not set the boolean to True in kbmeta. Right code required
        stueckl_inst.save()

    return r


def upPBBFunc(file, pid):
    '''
    Read in the calculation sheet. First right word is searched based on word
    'Business'. Linenumber is sotred in headline. Afterwards the 'Indidvidual Amount'
    field is searched and right column will be stored var col_total.

    Once found, values will be stored to database.
    '''


    r = {'code':0, 'message':''}

    # Check if calculation sheet is not uploaded already
    pbbmeta_objects = PbbMeta.objects
    query_pbbmeta = pbbmeta_objects.filter(kbmeta__pid__iexact=pid)

    if query_pbbmeta:
        print('Eintrag vorhanden')
        r['code'] = 1
        r['message'] = 'Project calculation sheet already in database'
        return r

    # --------------------------------------


    kbmeta_inst = KbMeta()
    kbmeta_objects = KbMeta.objects
    query_kb = kbmeta_objects.get(pid__iexact=str(pid))



    try:
        wb = openpyxl.load_workbook(BASE_DIR + file, read_only=True, data_only=True)
        ws = wb['Calculation']
    except:
        r['code'] = 1
        r['message'] = 'Workbook or worksheet could not be loaded'
        return r

    #Search for the right line in the calculation sheet. Once found remember
    #line number in var headline

    pbb_inst = Pbb()
    # Generate list with alphabet A-Z
    col_list = list(map(chr, range(65, 90)))
    #Find cell for offerno from A1 to Z23
    i = 0
    chk_offer = 0
    chk_fx = 0
    for col in col_list:
        i+=1
        #Goes through each column A to Z and do following:
        for row in range(1,23):
            #Goes through each row
            if ws['{}{}'.format(col, row)].value:
                if 'Offer-Nr' in str(ws['{}{}'.format(col, row)].value):
                    cell_offerno = col_list[i] + str(row)
                    chk_offer += 1
                if 'Basic rate' in str(ws['{}{}'.format(col, row)].value):
                    cell_forex = col_list[i] + str(row)
                    chk_fx += 1

    check = chk_offer + chk_fx

    # ================= CHECK both pbb and pbbmeta fields before saving to DB ========================

    if chk_offer == 0:
        r['code'] = 1
        r['message'] = 'Offer-No cell could not be found'
        return r

    e_pid = ws['{}'.format(cell_offerno)].value
    if e_pid == pid:
        r['code'] = 1
        r['message'] = 'Offerno in Calculation and PID do not match'
        return r

    row = 0
    i=0
    while i < ws.max_row:
        i+=1
        if 'Business' in str(ws['A{}'.format(i)].value):
            row = i
            break
    #If row with 'Business' could not be found. Print message to user
    if row == 0:
        r['code'] = 1
        r['message'] = 'Could not find headline "Business" in the sheet calculation'
        return r


    #Search for the right column in the calculation sheet. Once found remember db_column
    #in var col_total.
    col = ''
    col_len = 0
    while col_len < 27:
        if 'Individual' in str(ws['{}{}'.format(col_list[col_len], row)].value):
            col = col_list[col_len]
            break
        col_len += 1


    # ========================================= END OF CHECK cells ===============================

    pbbmeta_inst = PbbMeta()
    pbbmeta_inst.offer_no = pid #ws['{}'.format(cell_offerno)].value
    pbbmeta_inst.projname = ws['{}'.format('B3')].value #Optimze: Search for field projectname
    pbbmeta_inst.customer = ws['{}'.format('B4')].value #Optimize: Search for field customer

    if chk_fx == 1:
        pbbmeta_inst.fx_rate = ws['{}'.format(cell_forex)].value

    #TODO: Read in sheets without below value. Afterwards create html page to let somebody insert manually.

    #pbbmeta_inst.country_inst =
    #pbbmeta_inst.planttype =
    #pbbmeta_inst.qty_units =
    #pbbmeta_inst.total_output =
    #pbbmeta_inst.endcustomer =
    #pbbmeta_inst.bidmanager =

    pbbmeta_inst.total_surcharges = ws['{}{}'.format(col_list[col_len],(row+7))].value
    pbbmeta_inst.total_includings = ws['{}{}'.format(col_list[col_len],(row+16))].value
    pbbmeta_inst.total_sm = ws['{}{}'.format(col_list[col_len],(row+19))].value
    pbbmeta_inst.total_cost = ws['{}{}'.format(col_list[col_len],(row+23))].value
    pbbmeta_inst.total_price_euro = ws['{}{}'.format(col_list[col_len],(row+26))].value
    pbbmeta_inst.total_price_fx = ws['{}{}'.format(col_list[col_len+1],(row+26))].value

    pbbmeta_inst.pk = None
    pbbmeta_inst.kbmeta = query_kb
    pbbmeta_inst.kbmeta.pbb = True
    pbbmeta_inst.save()


        #Steht im Feld Single kost etwas drin und steht im B#headline 'T3000
        #oder Hardware' dann lese die Werte aus Spalte B ein.

    offset = [1,3,4,5,8,9,10,11,12,13,14,17,18,23,26,31]
    i=0
    while i < (col_len-2): #Loop all columns
        i+=1
        if ws['{}{}'.format(col_list[i],(row+offset[13]))].value: #Check if field single cost contains some value

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


            pbb_inst.pbbmeta = pbbmeta_inst
            pbb_inst.pk = None
            pbb_inst.save()

    r['code'] = 0
    r['message'] = ''
    return r
