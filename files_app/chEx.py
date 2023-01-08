import PySimpleGUI as sg
import sqlite3
import os
from datetime import date
import pandas as pd

def connectionDB():
    conn = sqlite3.connect("files_app/app.db")
    db = conn.cursor()
    foreign_keys = db.execute("PRAGMA foreign_keys = ON;")

    return conn, db, foreign_keys

def alertEmpty():

    sg.theme('DarkGrey2')

    message = sg.Text(""" A pasta 'Extrato_CSV' está vazia.\n\n(Coloque o extrato no formato .csv)
    """, font='Courier 12')
   
    layout_alertEmpty = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_alertEmpty = sg.Window("chEx",icon='files_app/images/chEx-icon.png', 
    layout = layout_alertEmpty, size=(388,110), resizable = True, element_justification='c', 
    finalize=True)

    while True:
        event, values = window_alertEmpty.read()
        if event == sg.WIN_CLOSED:
            break

def confirmGenerateCSVAndExcel():

    sg.theme('DarkGrey2')

    message = sg.Text(""" Excel gerado com sucesso!\n\n(Pegue-o na pasta 'Excel_chEx')
    """, font='Courier 12')
   
    layout_confirmGenerateCSVAndExcel = [
        [sg.Text("")],
        [sg.Column([[message]])],
        [sg.Text("")],
    ]

    window_confirmGenerateCSVAndExcel = sg.Window("chEx",icon='files_app/images/chEx-icon.png', 
    layout = layout_confirmGenerateCSVAndExcel, size=(388,110), resizable = True, 
    element_justification='c', finalize=True)

    while True:
        event, values = window_confirmGenerateCSVAndExcel.read()
        if event == sg.WIN_CLOSED:
            break


def convertCSV(file_extract_path, file_extract):
    new_csv = pd.read_csv(
        file_extract_path,
        usecols=["DATA", "TIPO", "DESCRICAO", "VALOR"]
        )
    new_csv = new_csv[new_csv["TIPO"].str.contains("Pix Recebido")]
    new_csv.to_csv("Extrato_CSV/{}".format(file_extract), index=False, header=True)
    new_csv = pd.read_csv(file_extract_path, usecols=["DATA", "DESCRICAO", "VALOR"])
    new_csv = new_csv.rename(columns=({"DESCRICAO":"NOME"}))
    new_csv = new_csv.rename(columns=({"VALOR":"VALOR_PAGO"}))
    new_csv["DATA"] = pd.to_datetime(new_csv.DATA)
    new_csv["DATA"] = new_csv["DATA"].dt.strftime("%d/%m/%Y")
    new_csv = new_csv.rename(columns=({"DATA":"DATA_PAGAMENTO"}))
    new_csv.to_csv(
        "Extrato_CSV/{}".format(file_extract),
        columns=["NOME", "DATA_PAGAMENTO", "VALOR_PAGO"], 
        index=False,
        header=True
        )

def insertPayments(file_extract_path):

    conn, db, foreign_keys = connectionDB()

    payments = pd.read_csv(file_extract_path)
    payments.to_sql("Pagamentos", conn, if_exists="append", index=False)
    

def generateCSVAndExcel(file_extract_path):

    conn, db, foreign_keys = connectionDB()

    directoryPath = "Extrato_CSV"
    directory = os.listdir(directoryPath)
    if directory != []:
        file_extract = "".join(directory)
        file_extract = file_extract[:21]

    new_csv = pd.read_sql_query("""
        SELECT c.Nome, d.Data_Pagamento, 'PAGO'
        FROM Clientes AS c, Pagamentos AS d, Planos AS e
        WHERE c.Nome = d.Nome AND c.Id_Planos = e.Id AND d.Valor_Pago >= e.Valor
        UNION
        SELECT c.Nome, d.Data_Pagamento, 'NÃO PAGO'
        FROM Clientes AS c, Pagamentos AS d, Planos AS e
        WHERE c.Nome = d.Nome AND c.Id_Planos = e.Id AND d.Valor_Pago < e.Valor
    """, conn)
    new_csv.to_csv("Export.csv", index=False, header=True)
    new_csv = new_csv.rename(columns=({"'PAGO'":"Status"}))
    new_csv.to_excel(
        "Excel_chEx/{}.xlsx".format(file_extract),
        index=False,
        header=True
        )
    with open(file_extract_path,'w') as cnt:
        pass
    with open('Export.csv','w') as cnt:
        pass
    os.remove(file_extract_path)
    os.remove('Export.csv')
    os.rmdir('./Extrato_CSV')
    

def dropPayments():

    conn, db, foreign_keys = connectionDB()

    db.execute("""
    DROP TABLE Pagamentos;
    """)

    conn.commit()
    conn.close()
