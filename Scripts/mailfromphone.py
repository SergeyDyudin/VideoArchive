""" Скрипт на выходе получает csv-файлы с адресами электронной почты сотрудников(@grain.ru, @yugrusi.ru,
@yugrusiagro.ru), работающих на Заречной 5. Данные берутся из корпоративного телефонного справочника в директории
скрипта. Справочник должен быть xlsx.
"""

import openpyxl
import csv

FILE = 'Телефоны.xlsx'
GRAIN_MAIL = 'grain_mail.csv'
YUGRUSI_MAIL = 'yugrusi_mail.csv'
YUGRUSIAGRO_MAIL = 'yugrusiagro_mail.csv'


def split_mail(cell):
	"""Сделано через рекурсию и split(), т.к. справочник заполнен так, что в одной ячейке может 
	быть несколько электронных адресов.
	"""
	if '@grain.ru' in cell:
		if len(cell.split('\n')) > 1:
			for s in cell.split(): 
				split_mail(s)
		else:
			list_grain.append(cell)
	elif '@yugrusiagro.ru' in cell:
		if len(cell.split('\n')) > 1:
			for s in cell.split(): 
				split_mail(s)
		else:
			list_yugrusiagro.append(cell)
	elif '@yugrusi.ru' in cell:
		if len(cell.split('\n')) > 1:
			for s in cell.split(): 
				split_mail(s)
		else:
			list_yugrusi.append(cell)


wb = openpyxl.load_workbook(filename=FILE)
with open(GRAIN_MAIL, 'w', newline="") as grain, open(YUGRUSIAGRO_MAIL, 'w', newline="") as yugrusiagro, \
		open(YUGRUSI_MAIL, 'w', newline="") as yugrusi:
	list_grain = []
	list_yugrusi = []
	list_yugrusiagro = []
	for ws in wb.worksheets:
		for row in ws.rows:
			for cell in row:
				if (cell.value is not None) and ('Заречная, 5' in str(cell.value).strip()):
					for c in row:
						split_mail(str(c.value).strip())
	# Перегоняем в set() и обратно в list(), чтобы убрать повторы
	# [[..],[..],[..]] делаем, т.к. так csv-модуль корректно записывает данные
	list_grain = [[mail] for mail in set(list_grain)]
	list_yugrusiagro = [[mail] for mail in set(list_yugrusiagro)]
	list_yugrusi = [[mail] for mail in set(list_yugrusi)]
	print(len(list_grain), len(list_yugrusiagro), len(list_yugrusi), sep='\n')
	csv.writer(grain).writerows(list_grain)
	csv.writer(yugrusiagro).writerows(list_yugrusiagro)
	csv.writer(yugrusi).writerows(list_yugrusi)
wb.close()



