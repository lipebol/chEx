import PySimpleGUI as sg
from files_app.plans_dataFrame import dataFramePlans
from files_app.new_plan import newPlan

def plans():
     
    sg.theme('DarkGrey2')

    chEx = sg.Image(filename='files_app/images/chEx.png')

    layout_plans = [
        [sg.Text('')],
        [sg.Column([[chEx]])],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button("Novo Plano", font='Courier 12')],
        [sg.Text('')],
        [sg.Button("Ver Planos", font='Courier 12')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text("v 0.1", font='Courier 8')]
    ]

    window_plans = sg.Window("chEx", icon='files_app/images/chEx-icon.png',
    layout = layout_plans, size=(400, 420), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_plans.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "Novo Plano":
            window_plans.Hide()
            newPlan()
            window_plans.UnHide()
        if event == "Ver Planos":
            window_plans.Hide()
            dataFramePlans()
            window_plans.UnHide()