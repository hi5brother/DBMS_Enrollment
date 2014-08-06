#-------------------------------------------------------------------------------
# Name:        excelFormatting

# Purpose:		formats some excel output stuff
#				changes column width
#				freezes panes
#
# Author:      DBMS
#
# Created:     30/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import itertools
import xlwt

def columnWidth(sheet, width):	
	'''Pass in the number of characters each column width will be and set it for the sheet
		First 3 columns: COURSE...TERM...ENROLLMENTS
	'''
	colWidth = 256 * width
	try: 
		for i in itertools.count():

			sheet.col(i).width = colWidth

			if i == 0:			#reset the FIRST column's width to fit all the course names
				sheet.col(i).width = 256 * 20
			elif i == 1:				#the SECOND column's width fits the "TERM" numbers
				sheet.col(i).width = 256 * 10
			elif i == 2:				#the THIRD column's wdith fits the "ENROLLMENTS" numbers
				sheet.col(i).width = 256 * 10

	except ValueError:
		pass
	return True

def columnWidthProg(sheet, width):
	'''Same as previous function, but used for breakdowns based on program
	'''
	colWidth = 256 * width
	try:
		for i in itertools.count():
			sheet.col(i).width = colWidth

			if i == 0:
				sheet.col(i).width = 256 * 12
	except ValueError:
		pass
	return True


def freezePanes(sheet, rows):
	'''Sets the number of rows to freeze in the sheet
	'''
	sheet.set_panes_frozen(True)
	sheet.set_horz_split_pos(rows)
	return True

