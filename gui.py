#remember pyinstaller
from pickle import FALSE, TRUE
import PySimpleGUI as sg
import re
from datetime import date
todays_date = date.today()
#set the theme for the screen/window
sg.theme("DarkTanBlue")

#######################################################
#field of column name select
#table relationship
table=[
    {
        "name":"PolicyMaster",
        "primary":"PoliyNumber",
        "foreign":[
            {
            "key":"PolicyNumber",
            "reference":["B"],
            #connect on
            "conon":"PolicyNumber"
            },
            {
            "key":"PolicyNumber",
            "reference":["A"],
            "conon":"PolicyNumber"
            },
        ]
    },
    {
        "name":"A",
        "primary":"PoliyNumber",
        "foreign":[
            {
            "key":"IC",
            "reference":["C"],
            "conon":"IC"
            }
        ]
    },
    {
        "name":"B",
        "primary":"PoliyNumber",
        "foreign":[]
        
    },
    {
        "name":"C",
        "primary":"IC",
        "foreign":[]
        
    },
]

column_data=[
    {
        "name":"PolicyNumber",
        "type":"multi-input",
        "id": 1,
        "table": "PolicyMaster"

    }, 
    {
        "name":"Status",
        "type":"multi-select",
        "criteria":['xxx','bbb','ccc'],
        "id": 2,
        "table": "PolicyMaster"

    }, 
    {
        "name": "Date",
        "type": "date",
        "id": 3,
        "table":"PolicyMaster"
    },
    {
        "name": "IC",
        "type": "multi-input",
        "id":4,
        "table":"A"
    },
    {
        "name": "Product",
        "type": "multi-select",
        "criteria":['abc','cde','efg'],
        "id":5,
        "table":"B"
    },
    {
        "name":"Payment Method",
        "type":"multi-select",
        "criteria":['credit card','cash'],
        "id": 6,
        "table": "A"

    },
    {
        "name":"Age",
        "type":"range",
        "id": 7,
        "table": "C"

    }
]

# column_data = [
#     {
#         "name":"Payment Method",
#         "type":"multi-select",
#         "criteria":['credit card','cash'],
#         "id": 1,
#         "table": "Pay"

#     }, 
#     {
#         "name": "Date",
#         "type": "date",
#         "id":2,
#         "table":"Pay"
#     },
#     {
#         "name": "CustomerID",
#         "type": "multi-input",
#         "id":3,
#         "table":"Pay"
#     },
#     {
#         "name": "Id",
#         "type": "multi-input",
#         "id":4,
#         "table":"Pay"
#     },
#     {
#         "name": "Amount",
#         "type": "range",
#         "id":5,
#         "table":"Pay"
#     },
#     {
#         "name": "Product",
#         "type": "multi-select",
#         "criteria":['abc','cde','efg'],
#         "id":6,
#         "table":"Cus"
#     }
   
   
# ]

# all the columns in policymaster and column not in policymaster
# if column repeated only the senior table's data needed to be recorded

collist=[]
for entry in column_data:
    collist.append(entry["name"])

col_options = [
    [sg.Text('Search:')],
    [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHCOL-'),sg.Button("X",key="-CLEARCOL-")],
    [sg.Listbox(values=collist, size=(20, 8), enable_events=True, select_mode='multiple', key='-LISTCOL-')]]

filter_options=[
    [sg.Text('Search:')],
    [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHFIL-'),sg.Button("X",key="-CLEARFIL-")],
    [sg.Listbox(values=collist, size=(20, 8), enable_events=True, select_mode='multiple', key='-LISTFIL-')]]

# col_options = [
#           [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHCOL-'),sg.Button('Search',enable_events=True,key='-FIND1-')]]
# for entry in column_data:
#     col_options.append([sg.Checkbox(entry["name"], key=f'-COL{entry["name"].lower()}-')])
    
# filter_options=[
#           [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHFIL-'),sg.Button('Search',enable_events=True,key='-FIND2-')]]
# for entry in column_data:
#     filter_options.append([sg.Checkbox(entry["name"], key=f'-FIL{entry["name"].lower()}-')])

frame1 = [
    [sg.Text('New Table Name:')],
    [sg.Input(size=(40, 1),key='-TABLE-')],
    [sg.Column([[sg.Frame('Choose Columns to be Included', layout= col_options)]],size = (None, 240), element_justification='c'),
    sg.Column([[sg.Frame('Choose Columns to be Filtered',layout=filter_options)]],size = (None, 240), element_justification='c')]
]

##########################################################


SYMBOL_UP =    '▲'
SYMBOL_DOWN =  '▼'
def collapse(layout, key):
    """
    Helper function that creates a Column that can be later made hidden, thus appearing "collapsed"
    :param layout: The layout for the section
    :param key: Key used to make this seciton visible / invisible
    :return: A pinned column that can be placed directly into your layout
    :rtype: sg.pin
    """
    return sg.pin(sg.Column(layout, key=key, visible=False))
#########################DDOKOKDOKOKODKDOKDOKO
#########################################################
#field of filter options
#drop down (open section)


layout2=[]
section=[]
list2=[]

for entry in column_data:
    if entry['type']=="multi-select":
        section.append({
            "opened":True,
            "name":entry["name"],
            "list":[sg.Text("Select Criteria"),sg.Listbox(values=entry['criteria'], select_mode='multiple', key=f'-MULTIS{entry["id"]}-', size=(30, 6))],
            "id": entry["id"]
            })
    elif entry['type']=="date":
        section.append({
            "opened":True,
            "name":entry["name"],
            # "list":[sg.Input(key=f'-FROM{entry["id"]}-', size=(20,1)), 
            #     sg.CalendarButton('From',  target=f'-FROM{entry["id"]}-', format='%m-%d-%Y', default_date_m_d_y=(todays_date.day,todays_date.month,todays_date.year), ),
            #     sg.Input(key=f'-TO{entry["id"]}-', size=(20,1)), 
            #     sg.CalendarButton('To',  target=f'-TO{entry["id"]}-', format='%m-%d-%Y', default_date_m_d_y=(todays_date.day,todays_date.month,todays_date.year), )],
            "list":[sg.Input(key=f'-FROM{entry["id"]}-', size=(20,1)), 
                sg.Button('From', key=f'-CAAL{entry["id"]}-' ),
                sg.Input(key=f'-TO{entry["id"]}-', size=(20,1)), 
                sg.Button('To',key=f'-CABL{entry["id"]}-' )],
            "id": entry["id"]
            })
    elif entry['type']=="multi-input":  
        section.append({
            "opened":True,
            "name":entry["name"],
            "list":[
                sg.Listbox(values=[], key=f'-LIST{entry["id"]}-', size=(30, 6),enable_events=True),
                sg.Input(key=f'-IN{entry["id"]}-',size=(10,1)),
                sg.Button("Add",key=f'Show{entry["id"]}'), sg.Button("Delete",key=f'Delete{entry["id"]}')
            ],
            "id": entry["id"]
            
        })
    elif entry['type']=="range":
        section.append({
            "opened":True,
            "name":entry["name"],
            "list":[
                sg.Text("Start value"),
                sg.Input(key=f'-START{entry["id"]}-',size=(5, 1)),
                sg.Text("End value"),
                sg.Input(key=f'-END{entry["id"]}-',size=(5, 1))
                ],
            "id": entry["id"]
        
        })
    
cnt=1
for sec in section:
    section=[sec["list"]]
    list= [
        [sg.T(SYMBOL_DOWN, enable_events=True, k=f'-OPEN SEC{cnt}-', text_color='yellow', visible=False), sg.T(sec["name"], enable_events=True, text_color='yellow', k=f'-OPEN SEC{cnt}-TEXT', visible=False)],
        [collapse(section, f'-SEC{cnt}-')]
    ]
    layout2=layout2+list
    cnt+=1

frame2= [
    [sg.Column(
        [[sg.Frame('Filter Field', layout=[[sg.Text("Columns to be filtered",)]]+layout2)]],size=(600,800),scrollable=True,vertical_scroll_only=True,key='-COLUMN-'
        )]
]

####################################################################
#field of code output
cprint = sg.cprint

ML_KEY = '-ML-'+sg.WRITE_ONLY_KEY        # multiline element's key. Indicate it's an output only element

output_key = ML_KEY
code = [
        [sg.Button('PROC SQL', size=(10, 1), button_color='white on green', key='-B-')],
        [sg.Multiline(size=(None, 40), write_only=True, key='ML_KEY')],
        [sg.Button('RUN', key='-RUN-'), sg.Button('Copy Me',key='-COPY-')]
        # [sg.CalendarButton('From',  target=f'-FROM3-', format='%m-%d-%Y', default_date_m_d_y=(todays_date.day,todays_date.month,todays_date.year), )]
       
    ]
       

# Create layout with two columns using precreated frames
layout = [[sg.Column(frame1+frame2, element_justification='c'), sg.Column(code, element_justification='c')]]

#Define Window
window =sg.Window("SAS Code Generator",layout).Finalize()
#Read  values entered by user
window.Maximize()
event,values=window.read()

#access all the values and if selected add them to a string
# strx=""
# for val in values:
#     if window.FindElement(val).get()==True:
#         strx=strx+ " "+ val+","

down = True
newlist=[]
newlist2=[]
sg.cprint_set_output_destination(window, output_key)
while True:
    event, values = window.read()  # Read  values entered by user
    if event == sg.WIN_CLOSED:  # If window is closed by user terminate While Loop
        break
    # if event == 'Submit':# If submit button is clicked display chosen values
    #     window['options'].update(strx)  # output the final string
    # for sec in section:
    #     if event.startswith(f'-OPEN SEC{sec[3]}-'):
    #         sec["opened"]= not sec["opened"]
    #         window[f'-OPEN SEC{sec[3]}-'].update(SYMBOL_DOWN if sec["opened"] else SYMBOL_UP)
    #         window[f'-SEC{sec[3]}-'].update(visible=sec["opened"])
    #     if event==f'Show{sec[3]}':
    #         list2.append([values[f'-IN{sec[3]}-']])
    #         window.Element(f'-LIST{sec[3]}-').update(values=list2)
    #     if event== f'Delete{sec[3]}':
    #         list2.remove(values[f'-LIST{sec[3]}-'][0])
    #         window.Element(f'-LIST{sec[3]}-').update(values=list2)
    
    # if event.startswith('-OPEN SEC1-'):
    #     opened1 = not opened1
    #     window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
    #     window['-SEC1-'].update(visible=opened1)

    # if event.startswith('-OPEN SEC2-'):
    #     opened2 = not opened2
    #     window['-OPEN SEC2-'].update(SYMBOL_DOWN if opened2 else SYMBOL_UP)
    #     window['-SEC2-'].update(visible=opened2)
    
    # if event.startswith('-OPEN SEC3-'):
    #     opened3 = not opened3
    #     window['-OPEN SEC3-'].update(SYMBOL_DOWN if opened3 else SYMBOL_UP)
    #     window['-SEC3-'].update(visible=opened3)
    
    # if event.startswith('-OPEN SEC4-'):
    #     opened4 = not opened4
    #     window['-OPEN SEC4-'].update(SYMBOL_DOWN if opened4 else SYMBOL_UP)
    #     window['-SEC4-'].update(visible=opened4)
        
    # if event == 'Show3':
    #     list2.append([values['-IN3-']])
    #     window.Element('-LIST3-').update(values=list2)
    if event.startswith('Show'):
        k=re.findall(r'[0-9]+', event)
        kl="Show"+k[0]
        if [d[kl] for d in list2 if kl in d]==[]:
            list2.append({kl:[values[f'-IN{k[0]}-']]})
        else:
            [d[kl].append(values[f'-IN{k[0]}-']) for d in list2 if kl in d]
        window.Element(f'-LIST{k[0]}-').update(values=[d[kl] for d in list2 if kl in d][0])
       
    if event.startswith('Delete'):
        k=re.findall(r'[0-9]+', event)
        kl="Show"+k[0]
        [d[kl].remove(values[f'-LIST{k[0]}-'][0]) for d in list2 if kl in d][0]
        window.Element(f'-LIST{k[0]}-').update(values=[d[kl] for d in list2 if kl in d][0])


    if values['-SEARCHCOL-'] != '':                         # if a keystroke entered in search field
        search = values['-SEARCHCOL-']
        new_values = [x for x in collist if search in x]  # do the filtering
        window['-LISTCOL-'].update(new_values)     # display in the listbox
    
    if values['-SEARCHFIL-'] != '':                         # if a keystroke entered in search field
        search = values['-SEARCHFIL-']
        new_values = [x for x in collist if search in x]  # do the filtering
        window['-LISTFIL-'].update(new_values)     # display in the listbox
    # else:
    #     # display original unfiltered list
    #     # window['-LISTFIL-'].update(collist, set_to_index=[x["id"] for x in newlist])
    #     j=[]
    #     for i in newlist:
    #         j.append(i["id"]-1)
    #     window['-LISTFIL-'].update(collist,set_to_index=j)
    if event == '-LISTCOL-' and len(values['-LISTCOL-']):
        newlist2=[]
        for i in values['-LISTCOL-']:
            newlist2.append((next(x for x in column_data if x["name"] ==i)))

    if event == '-LISTFIL-':
        newlist=[]
        for i in values['-LISTFIL-']:
            newlist.append((next(x for x in column_data if x["name"] ==i)))
    
        for i in column_data:
            window[f'-SEC{i["id"]}-'].update(visible=False)
            window[f'-OPEN SEC{i["id"]}-'].update(visible=False)
            window[f'-OPEN SEC{i["id"]}-TEXT'].update(visible=False)

        for i in newlist:
            window[f'-SEC{i["id"]}-'].update(visible=True)
            window[f'-OPEN SEC{i["id"]}-'].update(visible=True)
            window[f'-OPEN SEC{i["id"]}-TEXT'].update(visible=True)
        window['-COLUMN-'].contents_changed() 
    if event=='-CLEARFIL-':
        j=[]
        for i in newlist:
            j.append(i["id"]-1)
        window['-LISTFIL-'].update(collist,set_to_index=j)

    if event=='-CLEARCOL-':
        j=[]
        for i in newlist2:
            j.append(i["id"]-1)
        window['-LISTCOL-'].update(collist,set_to_index=j)
    
    if event == '-B-':                # if the normal button that changes color and text
            down = not down
            window['-B-'].update(text='PROC SQL' if down else 'DATA', button_color='white on green' if down else 'white on red')
    
    if event == '-COPY-':
        text = window['ML_KEY'].Widget.selection_get()
        window.TKroot.clipboard_clear()
        window.TKroot.clipboard_append(text)
    
    if event.startswith('-CAAL'):
        k=k=re.findall(r'[0-9]+', event)
        date = sg.popup_get_date(close_when_chosen=True)
        if date:
            month, day, year = date
        window[f'-FROM{k[0]}-'].update(f"{year}-{month:0>2d}-{day:0>2d}")
    
    if event.startswith('-CABL'):
        k=k=re.findall(r'[0-9]+', event)
        date = sg.popup_get_date(close_when_chosen=True)
        if date:
            month, day, year = date
        window[f'-TO{k[0]}-'].update(f"{year}-{month:0>2d}-{day:0>2d}")
    
    if event=='-RUN-':
        window['ML_KEY'].update("")
        procsql=down
        columninclude=values['-LISTCOL-']
        columnfilter=values['-LISTFIL-']
        newtablename=values['-TABLE-']
        detailoffilter=[]
        detailofinclude=[]

        for i in columnfilter:
            detailoffilter.append((next(x for x in column_data if x["name"] ==i)))

        for i in columninclude:
            detailofinclude.append((next(x for x in column_data if x["name"] ==i)))

        
        #maintable <- ABC <- ABC <-.....
        #maintable <- join <- join1 <-.....
        # for i in detailofinclude:
        #     if i['table'] != "PolicyMaster":
        #         maintable=next(x for x in column_data if x["name"] =="PolicyMaster")
        #         for j in maintable["foreign"]:
        #             if i['table'] in j['reference']:
        #                join = i["table"]
        #                on = j['key']
        #                loop= False
        #             else:
        #                 for k in column_data:
        #                     for l in k["foreign"]:
        #                         if i['table'] in l['reference']:
        #                             join1= i['table']
        #                             on1 = l['key']
        #                             join = k["table"]
        #                             loop=False
        # joinlist=[]
        # onlist=[]
        # def findinmain(table):
        #     maintable=next(x for x in column_data if x["name"] =="PolicyMaster")
        #     for j in maintable["foreign"]:
        #         if table in j['reference']:
        #             join = table
        #             joinlist.append(table)
        #             on = j['key']
        #             onlist.append(on)
        #             loop= False
        #         else:
        #             join = table
        #             loop=True
        #     return join,on,loop
        
        # def findother(table):
        #     for k in column_data:
        #         for l in k["foreign"]:
        #             if table in l['reference']:
        #                 join1 = table
        #                 on1 = l['key']
        #                 join = k["table"]
        #                 joinlist.append(join,join1)
        #                 onlist.append(on1)
        #                 loop = False
        #             else: 
        #                 loop=True
        #     return join1,on1,join,loop

        # for i in detailofinclude:
        #     loop=True
        #     join= i['table']
        #     if i['table'] != "PolicyMaster":
        #         findinmain(i['table'])
        #     while loop==True:
        #         findother(join)
        #         while loop==True:
        #             findinmain(join)


        #################################################################
        #code for joinning table

        joinlist = []
        onlist = []

        def findinmain(table1):
            global loop
            global joinlist
            global onlist
            maintable = next((x for x in table if x["name"] == "PolicyMaster"),False)
            for j in maintable["foreign"]:
                if table1 in j['reference']:
                    join = {
                        "table":table1,
                        "on":"PolicyMaster",
                        "by.l":"PolicyMaster."+j['key'],
                        "by.r":table1+"."+j['conon']
                        }
                    # joinlist.append(table1)
                    joinlist.append(join)
                    # on = j['key']
                    # onlist.append([on,j['conon']])
                    loop = False
                
            
        def findinmain1(table1):
            global loop1
            global joinlist
            global onlist
            maintable = next((x for x in table if x["name"] == "PolicyMaster"),False)
            for j in maintable["foreign"]:
                if table1 in j['reference']:
                    # join = table1

                    # new=joinlist[-1:][0]
                    # new=[table1]+new
                    # joinlist.pop()
                    # joinlist.append(new)

                    # on = j['key']
                    # new2=[onlist[-1:][0]]
                    # new2=[[on,j['conon']]]+new2
                    # onlist.pop()
                    # onlist.append(new2)

                    join={
                        "table":table1,
                        "on":"PolicyMaster",
                        "by.l":"PolicyMaster."+j["key"],
                        "by.r":table1+"."+j["conon"]
                    }
                    joinlist.append(join)

                    loop1 = False
            

        def findother(table1):
            global loop1
            global joinlist
            global onlist
            global join55
            for k in table:
                if k["foreign"]!=[]:
                    for l in k["foreign"]:
                        if table1 in l['reference']:
                            # join1 = table1
                            # on1 = l['key']
                            join = k["name"]   

                            # joinlist.append([join, join1])

                            join3={
                                "table":table1,
                                "on":k["name"],
                                "by.l":k["name"]+"."+l['key'],
                                "by.r":table1+"."+l['conon']
                            }
                            joinlist.append(join3)
                            # onlist.append([on1,l['conon']])
                            loop1 = True
                            join55=join

        def findother1(table1):
            global loop1
            global joinlist
            global onlist
            global join55
            for k in table:
                if k["foreign"]!=[]:
                    for l in k["foreign"]:
                        if table1 in l['reference']:
                            # join1 = table1
                            # on1 = l['key']
                            join = k["name"]
                            # new=joinlist[-1:][0]
                            # new=[join, join1]+new
                            # joinlist.pop()
                            # joinlist.append([join, join1])

                            join3={
                                "table":table1,
                                "on":k["name"],
                                "by.l":k["name"]+"."+l['key'],
                                "by.r":table1+"."+l['conon']
                            }
                            joinlist.append(join3)

                            # new2=onlist[-1:][0]
                            # new2=[[on1,l['conon']]]+new2
                            # onlist.pop()
                            # onlist.append(new2)

                            loop1 = True
                            join55=join
        for i in detailofinclude:
            loop=True
            loop1=True
            join55=None
            join = i['table']
            if i['table'] != "PolicyMaster":
                findinmain(i['table'])
                if loop == True:
                    findother(join)
                    while loop1 == True:
                        findinmain1(join55)
                        
                        if loop1==True:
                            findother1(join)
                            
        selectitems=[]
        for i in detailofinclude:
            selectitems.append(i['name'])
        if procsql:
            sg.cprint("PROC SQL;",key='ML_KEY')
            sg.cprint("CREATE TABLE work."+ values['-TABLE-']+ " AS", key='ML_KEY')
            p1="SELECT " + ",".join(selectitems)
            sg.cprint(p1,key='ML_KEY')
            sg.cprint("FROM PolicyMaster",key='ML_KEY')
            for i in joinlist:
                p2="LEFT JOIN " + i["table"] + " ON " + i["by.l"] + " = " + i["by.r"]
                sg.cprint (p2,key='ML_KEY')     
                    
            ###################################################################################
            #code for where
            sg.cprint("WHERE",key='ML_KEY')
            count=1
            for i in detailoffilter:
                if count!=1:
                    sg.cprint ("AND",key='ML_KEY')
                if i['type']=="multi-select":
                    criteria=values[f'-MULTIS{i["id"]}-']
                    string=i['table']+ "."+i['name']+ " IN ('" + ",'".join(str(elem) for elem in criteria) + "')"
                    sg.cprint (string,key='ML_KEY')
                elif i['type']=="date":
                    startdate=values[f'-FROM{i["id"]}-']
                    enddate=values[f'-TO{i["id"]}-']
                    string="'" + startdate + "'d <= " + i['table'] + "." + i['name'] + "<= '" + enddate + "'d"
                    sg.cprint (string,key='ML_KEY')
                elif i['type']=="multi-input":  
                    kl="Show"+str(i["id"])
                    window[f'-LIST{i["id"]}-'].update(set_to_index=[0,1,2,3,4,5,6,7])
                    multilist=[d[kl] for d in list2 if kl in d][0]
                    string=i['table']+ "."+i['name']+ " IN ('" + ",'".join(str(elem) for elem in multilist) + "')"
                    sg.cprint (string,key='ML_KEY')
                elif entry['type']=="range":
                    startvalue=values[f'-START{i["id"]}-']
                    endvalue=values[f'-END{entry["id"]}-']
                    string="'" + startvalue + "' <= " + i['table'] + "." + i['name'] + "<= '" + endvalue + "'"
                    sg.cprint (string,key='ML_KEY')
                count+=1
            sg.cprint (";",key='ML_KEY')
            sg.cprint ("QUIT;",key='ML_KEY')
        ##############################################################################################################
        # DATA code
        else:
            # for i in joinlist:
            #     # if i["table"]=="PolicyMaster":
            #     string1="PORT SORT data=" + i["on"] + " out= work.S" + i["on"] + ";"
            #     string2="BY " + i["by.l"] + ";"
            #     string3="RUN;"
            #     string4=""
            #     string5="PORT SORT data=" + i["table"] + " out= work.S" + i["table"] + ";"
            #     string6="BY " + i["by.r"] + ";"
            #     string7="RUN;"
            #     string8=""
            #     string9="DATA work." + i["on"] + ";"
            #     string10= "MERGE work.S"+ i["on"]  + "(in=a)"
            #     string11= "work.S" + i["table"] + "(in=b);"
            #     string12= "BY " + i["by.l"] +";"
            #     string13="IF a THEN output; RUN;"
            #     for i in [string1,string2,string3,string4,string5,string6,string7,string8,string9,string10,string11,string12,string13]:
            #         sg.cprint (i,key='ML_KEY')

                

            # count=1
            # for i in detailoffilter:
            #     if count==1:
            #         sg.cprint("",key='ML_KEY')
            #         sg.cprint ("DATA work." + values['-TABLE-'] + ";",key='ML_KEY')
            #         sg.cprint ("SET work.PolicyMaster (WHERE=",key='ML_KEY')
            #     if count!=1:
            #         sg.cprint ("AND",key='ML_KEY')
            #     if i['type']=="multi-select":
            #         criteria=values[f'-MULTIS{i["id"]}-']
            #         string=  "("+ i['name']+ " IN ('" + ",'".join(str(elem) for elem in criteria) + "'))" 
            #         sg.cprint (string,key='ML_KEY')
            #     elif i['type']=="date":
            #         startdate=values[f'-FROM{i["id"]}-']
            #         enddate=values[f'-TO{i["id"]}-']
            #         string="("+ i['name'] + " >= '" + startdate + "'d AND " +i['name']+ "<= ' " + enddate + "'d)"
            #         sg.cprint (string,key='ML_KEY')
            #     elif i['type']=="multi-input":  
            #         kl="Show"+str(i["id"])
            #         window[f'-LIST{i["id"]}-'].update(set_to_index=[0,1,2,3,4,5,6,7])
            #         multilist=[d[kl] for d in list2 if kl in d][0]
            #         string="("+i['name']+ " IN ('" + ",'".join(str(elem) for elem in multilist) + "'))"
            #         sg.cprint (string,key='ML_KEY')
            #     elif entry['type']=="range":
            #         startvalue=values[f'-START{i["id"]}-']
            #         endvalue=values[f'-END{entry["id"]}-']
            #         string="("+i['name'] + ">= '" + startvalue + "' AND " + i['name'] + "<= '" + endvalue + "')"
            #         sg.cprint (string,key='ML_KEY')
            #     if count==len(detailoffilter):
            #         sg.cprint("); RUN",key='ML_KEY')
            #     count+=1

            for i in detailoffilter:
                if i['type']=="multi-select":
                    criteria=values[f'-MULTIS{i["id"]}-']
                    string=  "("+ i['name']+ " IN ('" + ",'".join(str(elem) for elem in criteria) + "'))" 
                    sg.cprint ("DATA work." + i['table'] + ";",key='ML_KEY')
                    sg.cprint ("SET " + i['table'] + "(WHERE=",key='ML_KEY')
                    sg.cprint (string,key='ML_KEY')
                    sg.cprint ("); RUN;",key='ML_KEY')
                    sg.cprint ("",key='ML_KEY')
                elif i['type']=="date":
                    startdate=values[f'-FROM{i["id"]}-']
                    enddate=values[f'-TO{i["id"]}-']
                    string="("+ i['name'] + " >= '" + startdate + "'d AND " +i['name']+ "<= ' " + enddate + "'d)"
                    sg.cprint ("DATA work." + i['table'] + ";",key='ML_KEY')
                    sg.cprint ("SET " + i['table'] + "(WHERE=",key='ML_KEY')
                    sg.cprint (string,key='ML_KEY')
                    sg.cprint ("); RUN;",key='ML_KEY')
                    sg.cprint ("",key='ML_KEY')
                elif i['type']=="multi-input":  
                    kl="Show"+str(i["id"])
                    window[f'-LIST{i["id"]}-'].update(set_to_index=[0,1,2,3,4,5,6,7])
                    multilist=[d[kl] for d in list2 if kl in d][0]
                    string="("+i['name']+ " IN ('" + ",'".join(str(elem) for elem in multilist) + "'))"
                    sg.cprint ("DATA work." + i['table'] + ";",key='ML_KEY')
                    sg.cprint ("SET " + i['table'] + "(WHERE=",key='ML_KEY')
                    sg.cprint (string,key='ML_KEY')
                    sg.cprint ("); RUN;",key='ML_KEY')
                    sg.cprint ("",key='ML_KEY')
                elif entry['type']=="range":
                    startvalue=values[f'-START{i["id"]}-']
                    endvalue=values[f'-END{entry["id"]}-']
                    string="("+i['name'] + ">= '" + startvalue + "' AND " + i['name'] + "<= '" + endvalue + "')"
                    sg.cprint ("DATA work." + i['table'] + ";",key='ML_KEY')
                    sg.cprint ("SET " + i['table'] + "(WHERE=",key='ML_KEY')
                    sg.cprint (string,key='ML_KEY')
                    sg.cprint ("); RUN;",key='ML_KEY')
                    sg.cprint ("",key='ML_KEY')


            for i in joinlist:
                if next((x for x in detailoffilter if x["table"] == i["table"]),False) and next((x for x in detailoffilter if x["table"] == i["on"]),False):
                    string1="PORT SORT data=work." + i["on"] + " out= work." + i["on"] + ";"
                    string2="BY " + i["by.l"] + ";"
                    string3="RUN;"
                    string4=""
                    string5="PORT SORT data=work." + i["table"] + " out= work.S" + i["table"] + ";"
                    string6="BY " + i["by.r"] + ";"
                    string7="RUN;"
                    string8=""
                elif next((x for x in detailoffilter if x["table"] == i["table"]),True) or next((x for x in detailoffilter if x["table"] == i["on"]),False):
                    string1="PORT SORT data=work." + i["on"] + " out= work." + i["on"] + ";"
                    string2="BY " + i["by.l"] + ";"
                    string3="RUN;"
                    string4=""
                    string5="PORT SORT data=" + i["table"] + " out= work." + i["table"] + ";"
                    string6="BY " + i["by.r"] + ";"
                    string7="RUN;"
                    string8=""
                elif next((x for x in detailoffilter if x["table"] == i["table"]),False) or next((x for x in detailoffilter if x["table"] == i["on"]),True):
                    string1="PORT SORT data=" + i["on"] + " out= work." + i["on"] + ";"
                    string2="BY " + i["by.l"] + ";"
                    string3="RUN;"
                    string4=""
                    string5="PORT SORT data=work." + i["table"] + " out= work." + i["table"] + ";"
                    string6="BY " + i["by.r"] + ";"
                    string7="RUN;"
                    string8=""
                elif next((x for x in detailoffilter if x["table"] == i["table"]),True) or next((x for x in detailoffilter if x["table"] == i["on"]),True):
                    string1="PORT SORT data=" + i["on"] + " out= work." + i["on"] + ";"
                    string2="BY " + i["by.l"] + ";"
                    string3="RUN;"
                    string4=""
                    string5="PORT SORT data=" + i["table"] + " out= work." + i["table"] + ";"
                    string6="BY " + i["by.r"] + ";"
                    string7="RUN;"
                    string8=""
                
                string9="DATA work." + i["on"] + ";"
                string10= "MERGE work."+ i["on"]  + "(in=a)"
                string11= "work." + i["table"] + "(in=b);"
                string12= "BY " + i["by.l"] +";"
                string13="IF a THEN output; RUN;"
                for i in [string1,string2,string3,string4,string5,string6,string7,string8,string9,string10,string11,string12,string13]:
                    sg.cprint (i,key='ML_KEY')
                
                sg.cprint ("",key='ML_KEY')
                finalstring1="DATA work." + values['-TABLE-'] + ";"
                finalstring2="SET work.PolicyMaster"+ "(keep="+ " ".join(str(elem) for elem in columninclude) +"); RUN;"  
                for i in [finalstring1,finalstring2]:
                    sg.cprint (i,key='ML_KEY')
#Close Window
window.close()    
