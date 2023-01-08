import PySimpleGUI as sg
from files_app.new_customer import newCustomer
from files_app.customers_dataFrame import dataFrameCustomers

def customers():
     
    sg.theme('DarkGrey2')

    chEx = sg.Image(filename='files_app/images/chEx.png')

    layout_customers = [
        [sg.Text('')],
        [sg.Column([[chEx]])],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button("Novo Aluno", font='Courier 12')],
        [sg.Text('')],
        [sg.Button("Ver Alunos", font='Courier 12')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text("v 0.1", font='Courier 8')]
    ]

    window_customers = sg.Window("chEx", icon='files_app/images/chEx-icon.png',
    layout = layout_customers, size=(400, 420), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_customers.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Novo Aluno":
            window_customers.Hide()
            newCustomer()
            window_customers.UnHide()
        if event == "Ver Alunos":
            window_customers.Hide()
            dataFrameCustomers()
            window_customers.UnHide()