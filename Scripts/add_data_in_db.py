import openpyxl
from db import DataBase

wb = openpyxl.load_workbook(filename='C:/install/Films.xlsx')
ws = wb.active
connect_file = r'C:\Users\video\Documents\Projects\VideoArchive\dbauth.txt'
db = DataBase(connect_file)

for row in range(2, 2376):  # max_row=ws.max_row):
    db.query(row)
    # print(row)
wb.close()