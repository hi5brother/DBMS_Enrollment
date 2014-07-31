#-------------------------------------------------------------------------------
# Name:        
#
#			testing ways to output to Excel
#			sheets that are output
#				- tuition/grant totals for all courses
#				- breakdown of courses based on program
#				- breakdown of courses based on plan (DBMS LISC, BCHM...)
#				- breakdown of courses based on year (1,2,3,4)
#				- breakdown of courses based on plan and year (e.g. BCHM Y1, BCHM Y2, BCHM Y3, BCHM Y4)
#				- a sheet with all the unit fees/progam infos, etc.
#
#			saves the new excel workbook into user specified location
#			
# Purpose:
#
# Author:      DBMS
#
# Created:     22/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys

import sqlite3

import xlrd
import xlwt

import ExcelOutput

import extractData as data
import calcGrant as grant
import calcTuition as tuition

import UI

from Tkinter import Tk 			#used to find directory to save in 
from tkFileDialog import asksaveasfilename

def totals(readBook):

	totalsRows = {'Totals' : len(courseList) + 2}

	for column in [columns['Enrollment'], columns['Grant Value'], columns['Tuition Value'], columns['Total Revenue']]:
		print column

def runApp():

	conn = data.connectDB()
	c = conn.cursor()

	sheetName = "DBMS Enrollment Data.xls"		#name of the excel spreadsheet

	cdLocation = os.getcwd()
	excelLocation = cdLocation + "\\" + sheetName

	try:
		os.remove(excelLocation)		#TESTING PURPOSES, REMOVES THE OLD SPREADSHEET EVERY TIME@@@@@@@@@@@@
	except WindowsError:
		pass

	book = xlwt.Workbook()

	ExcelOutput.tuitionGrantTotals.write(c,book)

	ExcelOutput.programTotals.write(c,book)

	ExcelOutput.planExpandedTotals.write(c,book)

	ExcelOutput.planSignificantTotals.write(c,book)

	ExcelOutput.yearTotals.write(c,book)

	rawPlanList = data.grabFullPlanList(c)
	checkPlanList = []

	for plan in rawPlanList:
		plan = plan[0]			#unpack the tuple
		
		breakPoint = plan.index('-')	#find the first occurence of "-" that separates BCHM-M-BSH
		plan = plan[0:breakPoint]		#splice the string to get just BCHM
		
		try: 
			temp = checkPlanList.index(plan)		#check if the course code BCHM exists in the list

		except ValueError:
			checkPlanList.append(plan)			#if not, it is added to the list

	selectedPlans = UI.planOptionsCheckBox.runScrollingApp(checkPlanList)
	for plan in selectedPlans:
		ExcelOutput.planBreakdown.write(c,book,plan)

	ExcelOutput.programInfo.write(c,book)

	#saving the file into a direcotry~~~~~~~~~~~~~~~~~
	timeStam = data.grabTimeStamp(c)		#only the date of the timestamp will be printed

	Tk().withdraw()

	filename = asksaveasfilename(defaultextension = '.xls', initialfile = 'DBMS Enrollment Data ' + timeStam[:10])

	while filename == '':		#a location must be saved
		print "User Error: File was not saved."
		filename = asksaveasfilename(defaultextension = '.xls', initialfile = 'DBMS Enrollment Data ' + timeStam[:10])

	try:
		book.save(filename)
	except IndexError:		#exists if no sheets are printed (empty file)
		pass
	except IOError:
		print "Error: Please close all Excel workbooks."

if __name__ == '__main__':
	runApp()
