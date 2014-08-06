#-------------------------------------------------------------------------------
# Name:        program breakdown based on year

# Purpose:		
#							
#				program... Year 1... Year 2... Year 3... Year 4...
#
# Author:      DBMS
#
# Created:     06/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt

from formatting import columnWidthProg, freezePanes

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data

def write(c, book):
	'''Setup of the sheet 
	'''
	sheet = book.add_sheet("ProgramYearTotals")		#name the sheet

	freezePanes(sheet, 1)

	columnWidthProg(sheet, 8)

	c.execute("SELECT DISTINCT program FROM students;")		#find all the program names
	programList = c.fetchall()

	c.execute("SELECT DISTINCT proj_level FROM students;")		#find all the years (1,2,3,4)
	yearList = c.fetchall()		

	programNameStr = 'Program Name'
	totalEnrollNameStr = 'Total Enrollments'
	columns = {programNameStr : 0,
				totalEnrollNameStr : 1}

	hardCodedColumns = len(columns)

	for heading, colNum in columns.iteritems():			#write the headings
		sheet.write(0,colNum,heading)
		
	for year in yearList:			
		columns[year] = yearList.index(year) + hardCodedColumns
		sheet.write(0, columns[year], "Year " + str(year[0]))

	yearTotal = [0] * (len(yearList) + 1)	#initialize the list to store totals 

	'''	Writing the data into each cell based on program and year
	'''
	count = 1
	for program in programList:
		program = program[0]

		sheet.write(count, columns[programNameStr], program)

		progTotal = 0

		for year in yearList:		

			yearCount = data.grabProgramYearEnroll(c, program, year[0])
			sheet.write(count, columns[year], yearCount)		

			yearTotal[year[0]] = yearTotal[year[0]] + yearCount		

			progTotal = progTotal + yearCount		#counting the total number in each program

		sheet.write(count, columns[totalEnrollNameStr], progTotal)

		count = count + 1

	'''Add the totals at the very bottom of the list
	'''

	sheet.write(count, columns[programNameStr], "Totals")		#outputting the totals of each year
	sheet.write(count, columns[totalEnrollNameStr], sum(yearTotal))

	for year in yearList:
		sheet.write(count, columns[year], yearTotal[year[0]])	

	return True
