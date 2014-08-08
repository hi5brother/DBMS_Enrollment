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

from collections import OrderedDict 

from updateConstants import checkError

import ExcelOutput

import xlwt

import extractData as data
import calcGrant as grant
import calcTuition as tuition

import UI

from Tkinter import Tk 			#used to find directory to save in 
from tkFileDialog import asksaveasfilename

def runApp():

	conn = data.connectDB()
	c = conn.cursor()

	sheetName = "DBMS Enrollment Data.xls"		#name of the excel spreadsheet

	tuitionGrantSheetName = "Course Tuition and Grant Revenue Totals"
	programTotalsSheetName = "Course Breakdown Based on Program"
	planTotalsSheetName = "Course Breakdown Based on All Plans"
	sigPlanTotalsSheetName = "Course Breakdown Based on Plans (with >10 enrollments)"
	yearTotalsSheetName = "Course Breakdown Based on Year"
	planBreakdownSheetName = "Course Breakdown Based on Selected Plans"
	programYearSheetName = "Program Breakdown Based on Year"
	programInfoSheetName = "Program Info"

	sheetsOrderedDict = OrderedDict([
									(tuitionGrantSheetName, 0),
									(programTotalsSheetName, 1),
									(planTotalsSheetName, 2),
									(sigPlanTotalsSheetName, 3),
									(yearTotalsSheetName, 4),
									(planBreakdownSheetName, 5),
									(programYearSheetName, 6),
									(programInfoSheetName, 7),
									])

	cdLocation = os.getcwd()
	excelLocation = cdLocation + "\\" + sheetName

	try:
		os.remove(excelLocation)		#TESTING PURPOSES, REMOVES THE OLD SPREADSHEET EVERY TIME@@@@@@@@@@@@
	except WindowsError:
		pass

	'''	Asks user for information that needs to be shown
	'''

	selectedSheets = UI.sheetsOptionsCheckBox.runScrollingApp(sheetsOrderedDict)		#UI module asks for sheets
	while not checkError(selectedSheets):
		UI.errorMessageBox.runApp(selectedSheets)
		selectedSheets = UI.sheetsOptionsCheckBox.runScrollingApp(sheetsOrderedDict)
	
	selectedSheetsKey = []			#used to store the keys of the selected sheets

	for name in selectedSheets:

		selectedSheetsKey.append(sheetsOrderedDict[name])

	book = xlwt.Workbook()

	if sheetsOrderedDict[tuitionGrantSheetName] in selectedSheetsKey:

		ExcelOutput.tuitionGrantTotals.write(c,book)

	if sheetsOrderedDict[programTotalsSheetName] in selectedSheetsKey:	

		ExcelOutput.programTotals.write(c,book)

	if sheetsOrderedDict[planTotalsSheetName] in selectedSheetsKey:

		ExcelOutput.planExpandedTotals.write(c,book)

	if sheetsOrderedDict[sigPlanTotalsSheetName] in selectedSheetsKey:

		ExcelOutput.planSignificantTotals.write(c,book)

	if sheetsOrderedDict[yearTotalsSheetName] in selectedSheetsKey:

		ExcelOutput.yearTotals.write(c,book)

	if sheetsOrderedDict[planBreakdownSheetName] in selectedSheetsKey:
		#Make list of plans with only the plan code e.g. "BCHM"
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
		while not checkError(selectedPlans):			#ensure plans are chosen to be output
			UI.errorMessageBox(selectedPlans)
			selectedPlans = UI.planOptionsCheckBox.runScrollingApp(checkPlanList)

		for plan in selectedPlans:

			ExcelOutput.planBreakdown.write(c,book,plan)

	if sheetsOrderedDict[programYearSheetName] in selectedSheetsKey:

		ExcelOutput.programYearTotals.write(c,book)

	if sheetsOrderedDict[programInfoSheetName] in selectedSheetsKey:

		ExcelOutput.programInfo.write(c,book)
	

	'''Save the file into a specific location. This uses the tkfiledialog module
		to select the save location.
		The default save name is "DBMS Enrollment Data " and the timestamp date.
		A location must be chosen for save location.
	'''

	timeStam = data.grabTimeStamp(c)		#only the date of the timestamp will be printed

	Tk().withdraw()

	filename = asksaveasfilename(defaultextension = '.xls', initialfile = 'DBMS Enrollment Data ' + timeStam[:10])

	while filename == '':		#a location must be saved
		#UI.errorMessageBox.runApp("File was not saved. Please enter valid name.")
		filename = asksaveasfilename(defaultextension = '.xls', initialfile = 'DBMS Enrollment Data ' + timeStam[:10])

	try:
		book.save(filename)
	except IndexError:		#exists if no sheets are printed (empty file)
		pass
	except IOError:
		UI.errorMessageBox.runApp("Error: Please close all Excel workbooks.")

if __name__ == '__main__':
	runApp()


