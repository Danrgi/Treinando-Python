import pyodbc
import openpyxl
# conexão com banco de dados
dbo_data = (
    "Driver={SQL SERVER};"
    "Server={DESKTOP-DAN\SQLEXPRESS};"
    "Database={Learn_Python};"
)
try:
    dbo_connect = pyodbc.connect(dbo_data)
    print('Conexão bem sucedida')
    # dbo_connect.close()
except pyodbc.Error as e:
    print('Erro de conexão com o banco de dados')


def dboselect(colum_name=None, row_value=None):
    if colum_name or row_value != None:
        condition = f"WHERE {colum_name}='{row_value}'"
    else:
        condition = ''
    try:
        cursor = dbo_connect.cursor()
        command = f"""SELECT f FROM xlspython {condition}"""
        cursor.execute(command)
        rows = []
        for row in cursor.fetchall():
            rows.append(row)
        return rows
    except pyodbc.Error as e:
        print(e.args[1])
        return False


def xlsexport(colum_name=None, row_value=None):
    book = openpyxl.Workbook()
    book.create_sheet('Computadores')
    book.remove_sheet(book.get_sheet_by_name('Sheet'))
    pc_page = book['Computadores']
    pc_page.append(['ID', 'Tipo', 'IP', 'Local', 'Usuário', 'Senha'])
    result = dboselect(colum_name, row_value)
    if result != False:
        for row in result:
            pc_page.append([row[0], row[1], row[2], row[3], row[4], row[5]])

        book.save('Planilha Computadores.xlsx')
        print('Blz')
