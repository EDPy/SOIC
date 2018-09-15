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


def compare2N(pid1, pid2):
    ''' Comparision graph between two projects'''

    #Get project data and create pandas dataframe, variables pids and projectnames
    df_kbmeta = pd.DataFrame.from_records(KbMeta.objects.all().values())
    pdprojects = pd.DataFrame()
    df_pbb = pd.DataFrame.from_records(Pbb.objects.filter(pbbmeta_id=str(pid1)).values())

    pids = [str(pid1), str(pid2)]
    pnames = []

    dict_Names = {'sum_General': 'General','sum_Eng_Misc': 'Eng. Misc.', 'sum_Basic_Eng': 'Basic Eng.',
                  'sum_Detail_Eng': 'Detail Eng.',
                  'sum_Cust_Docu': 'Customer Doc.', 'sum_Unit_Control': 'Unit Control',
                  'sum_Measurement': 'Measurement',
                  'sum_Int_Foreign_Sys': 'Inteface', 'sum_Basic_Eng_E': 'Basic Eng. E.',
                  'sum_Detail_Eng_E': 'Detail Eng. E.',
                  'sum_FAT': 'FAT', 'sum_Installation': 'Installation', 'sum_Commissioning': 'Commissioning',
                  'sum_HW_Peri': 'HW Peripheral', 'sum_HW_DCS': 'HW DCS', 'sum_HW_E1': 'HW ETEC 1',
                  'sum_HW_E2': 'HW ETEC 2', 'sum_HW_Installation': 'HW Installation',}

    #Get all sum calculation for each project and store it to pandas dataframe pdprojects
    for pid in pids:
        series = pd.Series(sum_calculation(pid))
        pdprojects[projectName(pid)] = series
        pnames.append(projectNameSummary(pid))

    pdprojects[projectName(pid1)].append(df_pbb[['kind_of_business', 'single_cost_euro']][df_pbb.pbbmeta_id == pid1])
    print(pdprojects)
    print(df_pbb[['kind_of_business', 'single_cost_euro']][df_pbb.pbbmeta_id == pid1])
    #Create additional column Difference, which is the difference of both selected projects
    pdprojects['Difference'] = pdprojects[projectName(pid1)] - pdprojects[projectName(pid2)]
    pnames.append('Difference')

    pdprojectsT = pdprojects.T

    #Define color and x axis for the plot, plot size and standard style
    plt.style.use('ggplot')
    colors = plt.cm.tab20(np.linspace(0,1,len(dict_Names)+1))
    fig = plt.figure()

    #Bar chart settings
    ix = np.arange(len(pnames))+0.3
    ax1  = fig.add_subplot(1,1,1)

    #Cell_value is required for the input data in table
    cell_value = []
    xtable = []

    #Charttop is required for the stacked chart to define the top of the chart to begin new bar
    charttop = 0
    pie_index = []
    pie_value = []
    pie_colors = []




    #i is required to change color for each stackedbar
    #The loop will go through each row and create the stacked bar
    i=0
    for key, value in pdprojects.iterrows(): # key = sum_General, sum_Basic_Eng...
        if (pdprojectsT[key].sum()-pdprojectsT[key][pdprojectsT.index == 'Difference'].sum()) != 0:
            i+=1
            ax1.bar(ix, pdprojectsT[key].abs(), 0.35, bottom=charttop, label=dict_Names[key], color=colors[i])
            charttop += pdprojectsT[key].abs() #Barchart Difference always positive even if negative value
            pie_index.append(key)
            pie_value.append(pdprojects['Difference'].T[key])

        #Create table content.
        if key == 'sum_HW_DCS':
            cell_value.append(['%1.1f' % (x / 1000) for x in pdprojectsT[key]])
            xtable.append(dict_Names[key])
        if key == 'sum_Basic_Eng':
            cell_value.append(['%1.1f' % (x / 1000) for x in pdprojectsT[key]])
            xtable.append(dict_Names[key])
        if key == 'sum_Detail_Eng':
            cell_value.append(['%1.1f' % (x / 1000) for x in pdprojectsT[key]])
            xtable.append(dict_Names[key])


    #Cost chart from CALCULATION sheet
    #for x in df_pbb
    #df_pbb[['single_cost_euro', 'kind_of_business']][df_pbb.pbbmeta_id == 205970]


    #pdprojects[projectName([])]
    cell_value.append(['%1.1f' % (x / 1000) for x in pdprojects.sum()])
    xtable.append('Total SLI Cost')

    #Create attributes for the Table, and create the table itself
    the_table = plt.table(cellText = cell_value,
                         rowLabels=xtable,
                         colLabels=pnames,
                         loc='bottom')

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(8)
    plt.subplots_adjust(left=0.2, bottom=0.2)
    #plt.cm.ScalarMappable.to_rgba(x=pie_colors)
    ax1.set(title='Project Comparison', ylabel='Cost', xticks=[])
    ax1.legend()

    #Create Pie chart
    #ax2 = fig.add_subplot(1,2,2)
    #ax2.pie(pie_value, labels=pie_index, startangle=90)
    #ax2.set(title='Difference cost')
    plt.show()
