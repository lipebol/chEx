import PySimpleGUI as sg
import pandas as pd
import sqlite3


def connectionDB():
    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    foreign_keys = db.execute("PRAGMA foreign_keys = ON;")

    return conn, db, foreign_keys


def dataFrameCustomers():

    sg.theme('DarkGrey2')
    conn, db, foreign_keys = connectionDB()


    dataFrame = pd.read_sql_query("""
    SELECT c.Nome, e.Tipo, e.Modalidade, e.Valor
    FROM Clientes AS c, Forma_Pagamento AS d, Planos AS e
    WHERE c.Id_Forma_Pagamento = d.Id AND c.Id_Planos = e.Id
    """, conn)
    headings = list(dataFrame.columns)
    values = dataFrame.values.tolist()

    layout_dataFrameCustomers = [
        [sg.Text('')],
        [sg.Table(values = values, headings = headings, auto_size_columns=True)],
        [sg.Text('')],
        [sg.Text("v 0.1", font='Courier 8')]
    ]

    window_dataFrameCustomers = sg.Window("chEx", icon='files_app/images/chEx-icon.png', 
    layout = layout_dataFrameCustomers, size=(400, 240), resizable=True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_dataFrameCustomers.read()
        if event == sg.WIN_CLOSED:
            break

