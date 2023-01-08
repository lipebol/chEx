import PySimpleGUI as sg
import pandas as pd
import sqlite3


def connectionDB():
    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    foreign_keys = db.execute("PRAGMA foreign_keys = ON;")

    return conn, db, foreign_keys


def dataFramePaymentMethods():

    sg.theme('DarkGrey2')
    conn, db, foreign_keys = connectionDB()

    dataFrame = pd.read_sql_query("SELECT Id, Tipo FROM Forma_Pagamento", conn)
    headings = list(dataFrame.columns)
    values = dataFrame.values.tolist()

    layout_dataFramePlans = [
        [sg.Text('')],
        [sg.Table(values = values, headings = headings, auto_size_columns=True)],
        [sg.Text('')],
        [sg.Text("v 0.1", font='Courier 8')]
    ]

    window_dataFramePlans = sg.Window("chEx", icon='files_app/images/chEx-icon.ico', 
    layout = layout_dataFramePlans, size=(400, 260), resizable=True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_dataFramePlans.read()
        if event == sg.WIN_CLOSED:
            break

