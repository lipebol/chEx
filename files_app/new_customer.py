import PySimpleGUI as sg
import sqlite3
from files_app.paymentMethods_dataFrame import dataFramePaymentMethods
from files_app.plans_dataFrame import dataFramePlans

def connectionDB():
    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    foreign_keys = db.execute("PRAGMA foreign_keys = ON;")

    return conn, db, foreign_keys

def alertCustomer():

    sg.theme('DarkGrey2')

    message = sg.Text("Preencha todos os campos.", font='Courier 12')
   
    layout_alertCustomer = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_alertCustomer = sg.Window("chEx",icon='files_app/images/chEx-icon.png', 
    layout = layout_alertCustomer, size=(320,80), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_alertCustomer.read()
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

    window_numberAlert = sg.Window("chEx",icon='files_app/images/chEx-icon.png', 
    layout = layout_numberAlert, size=(320,80), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_numberAlert.read()
        if event == sg.WIN_CLOSED:
            break

def confirmInsertCustomer():

    sg.theme('DarkGrey2')

    message = sg.Text("Cadastrado!", font='Courier 12')
   
    layout_confirmInsertCustomer = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_confirmInsertCustomer = sg.Window("chEx",icon='files_app/images/chEx-icon.png', 
    layout = layout_confirmInsertCustomer, size=(250,80), resizable = True, 
    element_justification='c', finalize=True)

    while True:
        event, values = window_confirmInsertCustomer.read()
        if event == sg.WIN_CLOSED:
            break

def newCustomer():
     
    sg.theme('DarkGrey2')
    conn, db, foreign_keys = connectionDB()

    chEx = sg.Image(filename='files_app/images/chEx.png')
    client = sg.Text("Aluno(a):", font='Courier 12')
    input_client = sg.InputText('', key="client", size=(40), font='Courier 12')
    client_plan = sg.Text("Qual o 'Id' do Plano dele(a)?", font='Courier 12')
    input_client_plan = sg.InputText("", key="client_plan", size=(40), font='Courier 12')
    # button_plans = sg.Button("Ver Planos", font='Courier 9')
    form_payment = sg.Text("Qual o 'Id' da Form.Pag. que ele(a) usa?", font='Courier 12')
    input_form_payment = sg.InputText("", key="form_payment", size=(40), font='Courier 12')
    # button_form_payments = sg.Button("Ver Form.Pag.", font='Courier 9')
    buttonCadaster = sg.Button("Cadastrar", font='Courier 12')
    version = sg.Text("v 0.1", font='Courier 8')

    layout_newCustomer = [
        [sg.Text('')],
        [sg.Column([[chEx]], justification='center')],
        [sg.Text('')],
        [sg.Button("Ver Planos", font='Courier 9'), sg.Button("Ver Form.Pag.", font='Courier 9')],
        [sg.Text('')],
        [sg.Column([[client]])],
        [sg.Column([[input_client]])],
        [sg.Text('')],
        [sg.Column([[client_plan]])],
        [sg.Column([[input_client_plan]])],
        # [sg.Column([[button_plans]], justification='center')],
        [sg.Text('')],
        [sg.Column([[form_payment]])],
        [sg.Column([[input_form_payment]])],
        # [sg.Column([[button_form_payments]], justification='center')],
        [sg.Text('')],
        [sg.Column([[buttonCadaster]], justification='center')],
        [sg.Text('')],
        [sg.Column([[version]], justification='center')]
    ]

    window_newCustomer = sg.Window("chEx", icon='files_app/images/chEx-icon.png',
    layout = layout_newCustomer, size=(460, 600), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_newCustomer.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Ver Planos":
            window_newCustomer.Hide()
            dataFramePlans()
            window_newCustomer.UnHide()
        if event == "Ver Form.Pag.":
            window_newCustomer.Hide()
            dataFramePaymentMethods()
            window_newCustomer.UnHide()
        if event == "Cadastrar":
            client = values["client"]
            client_plan = values["client_plan"]
            form_payment = values["form_payment"]
            if client and client_plan and form_payment != "":
                if client_plan.isdigit() and form_payment.isdigit():

                    clients = [
                        (client, client_plan, form_payment)
                    ]

                    for item in clients:
                        db.executemany(
                            """INSERT INTO Clientes 
                            (Nome, Id_Planos, Id_Forma_Pagamento) 
                            VALUES (?,?,?)""", [item]
                        )

                    conn.commit()
                    window_newCustomer['client'].Update('')
                    window_newCustomer['client_plan'].Update('')
                    window_newCustomer['form_payment'].Update('')
                    confirmInsertCustomer()
                else:
                    numberAlert()
            else:
                alertCustomer()