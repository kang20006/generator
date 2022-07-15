# required packages
from pickle import FALSE, TRUE
from turtle import left
import PySimpleGUI as sg
import re
from datetime import date
todays_date = date.today()

sg.theme("DarkTanBlue")

#######################################################
#table relationship
#key = column on the table
#conon = column on foreign table
##in this case the master table is PolicyMaster
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

#column data
#if there is repeated column from other table (other than in the main table, not need to include just need to state it in the table list)
#there are 4 types of filter type (i.e. multi-input, multi-select, date, range)
# !!!!note: id must follow ascending order
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
###########################################################################################

#collist record all the available columns
collist=[]
for entry in column_data:
    collist.append(entry["name"])

#select column to be included gui
col_options = [
    [sg.Text('Search:')],
    [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHCOL-'),sg.Button("X",key="-CLEARCOL-")],
    [sg.Listbox(values=collist, size=(20, 8), enable_events=True, select_mode='multiple', key='-LISTCOL-')]]

#select column to be filtered gui
filter_options=[
    [sg.Text('Search:')],
    [sg.Input(size=(20, 1),enable_events=True, key='-SEARCHFIL-'),sg.Button("X",key="-CLEARFIL-")],
    [sg.Listbox(values=collist, size=(20, 8), enable_events=True, select_mode='multiple', key='-LISTFIL-')]]

#the frame
frame1 = [
    [sg.Text('New Table Name:')],
    [sg.Input(size=(40, 1),key='-TABLE-')],
    [sg.Column([[sg.Frame('Choose Columns to be Included', layout= col_options)]],size = (None, 240), element_justification='c'),
    sg.Column([[sg.Frame('Choose Columns to be Filtered',layout=filter_options)]],size = (None, 240), element_justification='c')]
]

##########################################################

#collapsible column in filter field but not functioning

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

#########################################################

#field of filter options

layout2=[]
section=[]

#list2 append the multi-input criteria
list2=[]

#loop through all the column in the column data
#append dictionary into list section
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
#cnt generate id number
# !!note: all the key word match with the id of the column
cnt=1
for sec in section:
    section=[sec["list"]]
    # make the all the element unvisible 
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
window =sg.Window("SAS Code Generator",layout,icon="icon.ico").Finalize()
#Read  values entered by user
#make window maximize
window.Maximize()
event,values=window.read()

down = True
newlist=[]
newlist2=[]
sg.cprint_set_output_destination(window, output_key)
while True:
    event, values = window.read()  
    if event == sg.WIN_CLOSED:  
        break
    
    #function of collapsible column but not in use

    # if event.startswith('-OPEN SEC1-'):
    #     opened1 = not opened1
    #     window['-OPEN SEC1-'].update(SYMBOL_DOWN if opened1 else SYMBOL_UP)
    #     window['-SEC1-'].update(visible=opened1)
    
    # all event start with Show{id}
    # multi-input add button
    if event.startswith('Show'):
        # find id of event
        k=re.findall(r'[0-9]+', event)
        kl="Show"+k[0]
        # if the column has no filter then open new dictionary
        #Show{id}:[<input>,<input>,...]
        if [d[kl] for d in list2 if kl in d]==[]:
            list2.append({kl:[values[f'-IN{k[0]}-']]})
        # else  if Show{id} exists then append to the Show{id}'s list
        else:
            [d[kl].append(values[f'-IN{k[0]}-']) for d in list2 if kl in d]
        # after that update the LIST{id}
        window.Element(f'-LIST{k[0]}-').update(values=[d[kl] for d in list2 if kl in d][0])
    
    # multi-input delete button
    if event.startswith('Delete'):
        try:
            k=re.findall(r'[0-9]+', event)
            kl="Show"+k[0]
            [d[kl].remove(values[f'-LIST{k[0]}-'][0]) for d in list2 if kl in d][0]
            window.Element(f'-LIST{k[0]}-').update(values=[d[kl] for d in list2 if kl in d][0])
        except:
            sg.Popup('Please Select Item to Delete',keep_on_top=True,title="Warning")

    #select column search input field
    if values['-SEARCHCOL-'] != '':                         # if a keystroke entered in search field
        search = values['-SEARCHCOL-']
        new_values = [x for x in collist if search in x]  # do the filtering
        window['-LISTCOL-'].update(new_values)     # display in the listbox
    
    #select filter search input field
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

    #select column field
    if event == '-LISTCOL-' and len(values['-LISTCOL-']):
        #append the selected item to newlist2
        newlist2=[]
        for i in values['-LISTCOL-']:
            newlist2.append((next(x for x in column_data if x["name"] ==i)))

    #select filter field
    if event == '-LISTFIL-':
        #append the selected item to newlist2
        newlist=[]
        for i in values['-LISTFIL-']:
            newlist.append((next(x for x in column_data if x["name"] ==i)))

        # make all the column unvisible in the filter field below first
        for i in column_data:
            window[f'-SEC{i["id"]}-'].update(visible=False)
            window[f'-OPEN SEC{i["id"]}-'].update(visible=False)
            window[f'-OPEN SEC{i["id"]}-TEXT'].update(visible=False)

        # make the selected filter column visible in the filter field below
        for i in newlist:
            window[f'-SEC{i["id"]}-'].update(visible=True)
            window[f'-OPEN SEC{i["id"]}-'].update(visible=True)
            window[f'-OPEN SEC{i["id"]}-TEXT'].update(visible=True)
        window['-COLUMN-'].contents_changed() 
    
    #the "x" button
    if event=='-CLEARFIL-':
        #when "x" is press update back the orignal column
        #and also set the back the selected list
        j=[]
        for i in newlist:
            j.append(i["id"]-1)
        window['-LISTFIL-'].update(collist,set_to_index=j)

    #the "x" button
    if event=='-CLEARCOL-':
        j=[]
        for i in newlist2:
            j.append(i["id"]-1)
        window['-LISTCOL-'].update(collist,set_to_index=j)
    
    if event == '-B-':                # if the normal button that changes color and text
            down = not down
            window['-B-'].update(text='PROC SQL' if down else 'DATA', button_color='white on green' if down else 'white on red')
    
    if event == '-COPY-':
        #user must select the code to copy
        try:
            text = window['ML_KEY'].Widget.selection_get()
            window.TKroot.clipboard_clear()
            window.TKroot.clipboard_append(text)
        except:
            sg.Popup('Please Select the Code', keep_on_top=True,title="Warning")
    
    #show calendar popup
    #date button "FROM"
    if event.startswith('-CAAL'):
        k=k=re.findall(r'[0-9]+', event)
        date = sg.popup_get_date(close_when_chosen=True)
        if date:
            month, day, year = date
        window[f'-FROM{k[0]}-'].update(f"{year}-{month:0>2d}-{day:0>2d}")

    #date button "TO"
    if event.startswith('-CABL'):
        k=k=re.findall(r'[0-9]+', event)
        date = sg.popup_get_date(close_when_chosen=True)
        if date:
            month, day, year = date
        window[f'-TO{k[0]}-'].update(f"{year}-{month:0>2d}-{day:0>2d}")
    
    if event=='-RUN-':
        # try to prevent error due to the empty multi-input
        try:
            #set the code field empty
            window['ML_KEY'].update("")
            #record all the input
            procsql=down
            columninclude=values['-LISTCOL-']
            columnfilter=values['-LISTFIL-']
            newtablename=values['-TABLE-']
            detailoffilter=[]
            detailofinclude=[]

            #take out all the data detail of filter chosen
            for i in columnfilter:
                detailoffilter.append((next(x for x in column_data if x["name"] ==i)))

            #take out all the data detail of colun include chosen
            for i in columninclude:
                detailofinclude.append((next(x for x in column_data if x["name"] ==i)))

            #################################################################
            #code for joinning table
            #join logic....
            #maintable <- A/B/C <- A/B/C <-.....

            joinlist = []
            onlist = []

            #find in the main table for reference
            # join={
            #     "table": the right table
            #     "on": the left table
            #     "by.l": join key of left
            #     "by.r": join key of right
            # }
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
            # global -- make all the variable to be able to access outside the function
            # same as findinmain just the loop1    
            def findinmain1(table1):
                global loop1
                global joinlist
                global onlist
                maintable = next((x for x in table if x["name"] == "PolicyMaster"),False)
                # because foeign is a list
                for j in maintable["foreign"]:
                    # if the table1 name in the reference
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
                        #stop loop1
                        loop1 = False
                
            # if cannot find in main table we find it in all the table
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

                                #loop1 have to be true because the found table must finally be join onto main table
                                loop1 = True

                                #join55 is the table that needed to be loop again in loop1
                                join55=join
            #duplicate
            # same as findother
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

            # the real loop to find the relationship for table joinning
            for i in detailofinclude:
                loop=True
                loop1=True
                join55=None
                #join is the table name
                join = i['table']
                #if the column is from the main table not need to join table
                if i['table'] != "PolicyMaster":
                    #if not from main table
                    #find it in the main table for reference table
                    findinmain(i['table'])
                    #if loop== true means cannot be found in the main table reference
                    if loop == True:
                        #we find it in other table reference
                        findother(join)
                        #even we can find in other table we need to take the other table to join it into the main table
                        #so loop1 == true
                        # enter while loop
                        while loop1 == True:
                            findinmain1(join55)
                            
                            if loop1==True:
                                findother1(join)
            ##################################################################################################
            #remove the duplicate table and on combination
            import pandas as pd
            joinlist2=pd.DataFrame(joinlist)      
            joinlist2=joinlist2.drop_duplicates(subset=['table','on'],keep="first")
            joinlist=pd.DataFrame.to_dict(joinlist2, orient='records')   

            selectitems=[]
            for i in detailofinclude:
                selectitems.append(i['name'])
            
            ##################################################################################################
            #proc sql 
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
                if detailoffilter!=[]:
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
                # we filter the table first before we join them together
                sg.cprint("DATA work.PolicyMaster;",key='ML_KEY')
                sg.cprint("SET PolicyMaster;",key='ML_KEY')
                sg.cprint("RUN;",key='ML_KEY')
                sg.cprint("",key='ML_KEY')

                finalstring2="SET work.PolicyMaster"+ "(keep="+ " ".join(str(elem) for elem in columninclude) +"); RUN;"  
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

                #reverse order of list so it can join from the subset table first then to the main table
                joinlist=joinlist[::-1]
                for i in joinlist:
                    #if we filter data before then need 'work.' else take it from the original table
                    if next((x for x in detailoffilter if x["table"] == i["table"]),False) and next((x for x in detailoffilter if x["table"] == i["on"]),False):
                        string1="PROC SORT data=work." + i["on"] + " out= work." + i["on"] + ";"
                        string2="BY " + i["by.l"] + ";"
                        string3="RUN;"
                        string4=""
                        string5="PROC SORT data=work." + i["table"] + " out= work.S" + i["table"] + ";"
                        string6="BY " + i["by.r"] + ";"
                        string7="RUN;"
                        string8=""
                    elif next((x for x in detailoffilter if x["table"] == i["table"]),True) or next((x for x in detailoffilter if x["table"] == i["on"]),False):
                        string1="PROC SORT data=work." + i["on"] + " out= work." + i["on"] + ";"
                        string2="BY " + i["by.l"] + ";"
                        string3="RUN;"
                        string4=""
                        string5="PROC SORT data=" + i["table"] + " out= work." + i["table"] + ";"
                        string6="BY " + i["by.r"] + ";"
                        string7="RUN;"
                        string8=""
                    elif next((x for x in detailoffilter if x["table"] == i["table"]),False) or next((x for x in detailoffilter if x["table"] == i["on"]),True):
                        string1="PROC SORT data=" + i["on"] + " out= work." + i["on"] + ";"
                        string2="BY " + i["by.l"] + ";"
                        string3="RUN;"
                        string4=""
                        string5="PROC SORT data=work." + i["table"] + " out= work." + i["table"] + ";"
                        string6="BY " + i["by.r"] + ";"
                        string7="RUN;"
                        string8=""
                    elif next((x for x in detailoffilter if x["table"] == i["table"]),True) or next((x for x in detailoffilter if x["table"] == i["on"]),True):
                        string1="PROC SORT data=" + i["on"] + " out= work." + i["on"] + ";"
                        string2="BY " + i["by.l"] + ";"
                        string3="RUN;"
                        string4=""
                        string5="PROC SORT data=" + i["table"] + " out= work." + i["table"] + ";"
                        string6="BY " + i["by.r"] + ";"
                        string7="RUN;"
                        string8=""
                    
                    string9="DATA work." + i["on"] + ";"
                    string10= "MERGE work."+ i["on"]  + "(in=a)"
                    string11= "work." + i["table"] + "(in=b);"
                    string12= "BY " + i["by.l"] +";"
                    string13="IF a THEN output; RUN;"
                    string14=""
                    for i in [string1,string2,string3,string4,string5,string6,string7,string8,string9,string10,string11,string12,string13,string14]:
                        sg.cprint (i,key='ML_KEY')
                    

                finalstring1="DATA work." + values['-TABLE-'] + ";"
                finalstring2="SET work.PolicyMaster"+ "(keep="+ " ".join(str(elem) for elem in columninclude) +"); RUN;"  
                for i in [finalstring1,finalstring2]:
                    sg.cprint (i,key='ML_KEY')
        except:
            sg.Popup('Please Fill in the Selected Filter Field', keep_on_top=True,title="Warning")
#Close Window
window.close()    
