import PySimpleGUI as sg
import sqlite3

def connectionDB():
    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    foreign_keys = db.execute("PRAGMA foreign_keys = ON;")

    return conn, db, foreign_keys

def alertPlan():

    sg.theme('DarkGrey2')

    message = sg.Text("Preencha todos os campos.", font='Courier 12')
   
    layout_alertPlan = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_alertPlan = sg.Window("chEx",icon='files_app/images/chEx-icon.ico', 
    layout = layout_alertPlan, size=(320, 100), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_alertPlan.read()
        if event == sg.WIN_CLOSED:
            break

def numberAlert():

    sg.theme('DarkGrey2')

    message = sg.Text("Preencha o campo 'Valor'\n apenas com número(s).", font='Courier 12')
   
    layout_numberAlert = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_numberAlert = sg.Window("chEx",icon='files_app/images/chEx-icon.ico', 
    layout = layout_numberAlert, size=(320, 100), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_numberAlert.read()
        if event == sg.WIN_CLOSED:
            break

def confirmInsertPlan():

    sg.theme('DarkGrey2')

    message = sg.Text("Cadastrado!", font='Courier 12')
   
    layout_confirmInsertPlan = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_confirmInsertPlan = sg.Window("chEx",icon='files_app/images/chEx-icon.ico', 
    layout = layout_confirmInsertPlan, size=(250, 100), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_confirmInsertPlan.read()
        if event == sg.WIN_CLOSED:
            break

def newPlan():
     
    sg.theme('DarkGrey2')
    conn, db, foreign_keys = connectionDB()

    chEx = sg.Image(filename='files_app/images/chEx.png')
    type_pĺans = sg.Text("Mensal, Semestral ou Anual?", font='Courier 12')
    input_type_plans = sg.InputText("", key="type_plans", size=(40), font='Courier 12')
    modality = sg.Text("Personal 1x, 2x, 3x, 4x ou 5x?", font='Courier 12')
    input_modality = sg.InputText("Personal ", key="modality", size=(40), font='Courier 12')
    value = sg.Text("Valor:", font='Courier 12')
    input_value = sg.InputText("", key="value", size=(40), font='Courier 12')
    buttonCadaster = sg.Button("Cadastrar", font='Courier 12')
    version = sg.Text("v 0.1", font='Courier 8')

    layout_newPlan = [
        [sg.Text('')],
        [sg.Column([[chEx]], justification='center')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Column([[type_pĺans]])],
        [sg.Column([[input_type_plans]])],
        [sg.Text('')],
        [sg.Column([[modality]])],
        [sg.Column([[input_modality]])],
        [sg.Text('')],
        [sg.Column([[value]])],
        [sg.Column([[input_value]])],
        [sg.Text('')],
        [sg.Column([[buttonCadaster]], justification='center')],
        [sg.Text('')],
        [sg.Column([[version]], justification='center')]
    ]

    window_newPlan = sg.Window("chEx", icon='files_app/images/chEx-icon.ico',
    layout = layout_newPlan, size=(400, 586), resizable = True, finalize=True)

    while True:
        event, values = window_newPlan.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Cadastrar":
            type_plans = values["type_plans"]
            modality = values["modality"]
            value = values["value"]
            comma = ","
            if type_plans and value != "" and modality != "Personal ":
                if comma in value:
                    numberAlert()
                else:
                    if value.isdigit():
                        plans = [
                            (type_plans, modality, value)
                        ]
                
                        for item in plans:
                            db.executemany(
                            """INSERT INTO Planos 
                            (Tipo, Modalidade, Valor) 
                            VALUES (?,?,?)""", [item]
                        )
                        conn.commit()
                        window_newPlan["value"].Update("")
                        window_newPlan["modality"].Update("Personal ")
                        window_newPlan["type_plans"].Update("")
                        confirmInsertPlan()
                    else:
                        numberAlert()
            else:
                alertPlan()