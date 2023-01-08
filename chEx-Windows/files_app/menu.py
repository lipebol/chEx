import PySimpleGUI as sg
import sqlite3
import os
from files_app.chEx import alertEmpty, convertCSV, insertPayments
from files_app.chEx import generateCSVAndExcel, dropPayments, confirmGenerateCSVAndExcel
from files_app.plans import plans
from files_app.customers import customers


def menuApp():
     
    sg.theme('DarkGrey2')

    chEx = sg.Image(filename='files_app/images/chEx.png')

    layout_menuApp = [
        [sg.Text('')],
        [sg.Column([[chEx]])],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Text('')],
        [sg.Button("chEx", font='Courier 12')],
        [sg.Text('')],
        [sg.Button("Planos", font='Courier 12')],
        [sg.Text('')],
        [sg.Button("Clientes", font='Courier 12')],
        [sg.Text('')],
        [sg.Text("v 0.1", font='Courier 8')],
    ]

    dirExtrato_CSV = './Extrato_CSV'
    dirExcel_chEx = './Excel_chEx'
    if not os.path.isdir(dirExtrato_CSV):
        os.makedirs(dirExtrato_CSV)
    if not os.path.isdir(dirExcel_chEx):
        os.makedirs(dirExcel_chEx)

    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    db.execute("PRAGMA foreign_keys = ON;")

    db.execute("""
    CREATE TABLE IF NOT EXISTS Planos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Tipo TEXT NOT NULL,
        Modalidade TEXT NOT NULL,
        Valor REAL NOT NULL
        );
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS Forma_Pagamento (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Tipo TEXT NOT NULL
        );
    """)

    db.execute("""
    SELECT * FROM Forma_Pagamento;
    """)
    items = db.fetchall()
    if items == []:
        db.execute("INSERT INTO Forma_Pagamento (Tipo) VALUES ('Pix')")
        db.execute("INSERT INTO Forma_Pagamento (Tipo) VALUES ('Cartão de Crédito')")
        db.execute("INSERT INTO Forma_Pagamento (Tipo) VALUES ('Dinheiro')")

    db.execute("""
    CREATE TABLE IF NOT EXISTS Clientes (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Id_Planos INTEGER,
        Id_Forma_Pagamento INTEGER,
        FOREIGN KEY(Id_Planos) REFERENCES Planos(Id),
        FOREIGN KEY(Id_Forma_Pagamento) REFERENCES Forma_Pagamento(Id)
        );
    """)

    db.execute("""
    CREATE TABLE IF NOT EXISTS Pagamentos (
        Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Nome TEXT NOT NULL,
        Data_Pagamento TEXT NOT NULL,
        Valor_Pago REAL NOT NULL
        );
    """)

    conn.commit()
    conn.close()

    window_menuApp = sg.Window("chEx", icon='files_app/images/chEx-icon.ico',
    layout = layout_menuApp, size=(400, 455), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_menuApp.read()
        if event == sg.WIN_CLOSED:
            break
        if event == "chEx":
            dirExtrato_CSV = './Extrato_CSV'
            dirExcel_chEx = './Excel_chEx'
            if not os.path.isdir(dirExtrato_CSV):
                os.makedirs(dirExtrato_CSV)
            if not os.path.isdir(dirExcel_chEx):
                os.makedirs(dirExcel_chEx)
            directoryPath = "Extrato_CSV"
            directory = os.listdir(directoryPath)
            if directory == []:
                alertEmpty()
            else:
                file_extract = "".join(directory)
                file_extract_path = "".join(directoryPath + "/" + file_extract)
                convertCSV(file_extract_path, file_extract)
                insertPayments(file_extract_path)
                generateCSVAndExcel(file_extract_path)
                dropPayments()
                confirmGenerateCSVAndExcel()
        if event == "Planos":
            window_menuApp.Hide()
            plans()
            window_menuApp.UnHide()
        if event == "Clientes":
            window_menuApp.Hide()
            customers()
            window_menuApp.UnHide()