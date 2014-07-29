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

import itertools
import xlrd
import xlwt

import extractData as data
import calcGrant as grant
import calcTuition as tuition

from collections import defaultdict

import UI.planOptionsCheckBox

from Tkinter import Tk 			#used to find directory to save in 
from tkFileDialog import asksaveasfilename

def columnWidth(sheet, width):	
	'''Pass in the number of characters each column width will be and set it for the sheet
	'''
	colWidth = 256 * width
	try: 
		for i in itertools.count():

			sheet.col(i).width = colWidth

			if i == 0:			#reset the FIRST column's width to fit all the course names
				sheet.col(i).width = 256 * 20

	except ValueError:
		pass
	return True

	#CALCULATING TUITION AND GRANT TOTALS~~~~~~~~~~~~~~~~~~~~~~~~~~~
def tuitionGrantTotals(c,book):
	courseTotals = book.add_sheet("CourseTotals")

	twoDecimalStyle = xlwt.XFStyle()		#styling for using two decimals
	twoDecimalStyle.num_format_str = '0.00'

	columnWidth(courseTotals,14)

	courseNameStr = 'Course Name'
	termNameStr = 'Term'
	creditsNameStr = 'Credits'
	enrollmentNameStr = 'Enrollments'
	grantValNameStr = 'Grant Value ($)'
	tuitValNameStr = 'Tuition Value ($)'
	totRevNameStr = 'Total Revenue ($)'
	grantStudNameStr = 'Grant per Student'
	tuitStudNameStr = 'Tuition per Student'
	revStudNameStr = 'Revenue per Student'


	columns = {courseNameStr : 0, 
				termNameStr : 1, 
				creditsNameStr : 2, 
				enrollmentNameStr : 3, 
				grantValNameStr : 4, 
				tuitValNameStr : 5,
				totRevNameStr : 6,
				grantStudNameStr : 7,
				tuitStudNameStr : 8,
				revStudNameStr : 9
				}

	for heading, colNum in columns.iteritems():
		courseTotals.write(0, colNum, heading)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	enrollTot = 0  #HARDCODE FOR THE TOTALS OF CERTAIN METRICS
	grantTot = 0
	tuitionTot = 0
	totalTot = 0

	count = 1 		#used to increment the row number
	for course in courseList:
		course = course[0]		#unpack the tuple

		courseName = data.grabCourseName(c, course)
		courseTotals.write(count, columns[courseNameStr], courseName)

		term = data.grabCourseTerm(c, course)
		courseTotals.write(count, columns[termNameStr], term)

		credits = data.grabCourseCredits(c,course)
		courseTotals.write(count, columns[creditsNameStr] , credits, twoDecimalStyle)

		enrollment = data.grabEnrollmentNumber(c, course)
		enrollTot = enrollTot + enrollment
		courseTotals.write(count, columns[enrollmentNameStr] , enrollment)

		grantVal = grant.runAppCourse(course)
		grantTot = grantTot + grantVal
		courseTotals.write(count, columns[grantValNameStr], grantVal, twoDecimalStyle)

		tuitionVal = tuition.runAppCourse(course)
		tuitionTot = tuitionTot + tuitionVal
		courseTotals.write(count, columns[tuitValNameStr], tuitionVal, twoDecimalStyle)

		total = grantVal + tuitionVal
		totalTot = totalTot + total
		courseTotals.write(count, columns[totRevNameStr], total, twoDecimalStyle)

		grantPerStud = grantVal / enrollment
		courseTotals.write(count, columns[grantStudNameStr], grantPerStud, twoDecimalStyle)

		tuitionPerStud = tuitionVal / enrollment
		courseTotals.write(count, columns[tuitStudNameStr], tuitionPerStud, twoDecimalStyle)

		revenuePerStud = total / enrollment
		courseTotals.write(count, columns[revStudNameStr], revenuePerStud, twoDecimalStyle)

		count = count + 1 	#used to icnrement row number

	courseTotals.write(count,columns[courseNameStr], "Totals")
	courseTotals.write(count,columns[enrollmentNameStr], enrollTot)		#HARDCODE FOR THE TOTALS OF CERTAIN METRICS
	courseTotals.write(count, columns[grantValNameStr], grantTot, twoDecimalStyle)
	courseTotals.write(count,columns[tuitValNameStr], tuitionTot, twoDecimalStyle)
	courseTotals.write(count,columns[totRevNameStr], totalTot, twoDecimalStyle)

	courseTotals.set_panes_frozen(True)
	courseTotals.set_horz_split_pos(1)		#Freeze panes for the first row
	return True

	#CALCULATING ENROLLMENTS BASED ON PROGRAM~~~~~~~~~~~~~~~~~~~~~~~
def programEnrollments(c,book):
	programBreakdown = book.add_sheet("ProgramBreakdown")
	informationStartRow = 1
	columnWidth(programBreakdown, 6)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT program FROM students;")
	programsList = c.fetchall()

	courseNameStr = 'Course Name'
	enrollmentNameStr = 'Enrollments'

	fYrArtsStr = 'Arts (1st)'		#these help differentiate between 1st year artsci HONOURS and upper year artsci HONOURS
	fYrSciStr = 'Science (1st)'
	upYrArtsStr = 'Arts Hon (2-4)'
	upYrSciStr = 'Science Hon (2-4)'

	columns = {courseNameStr : 0,
				enrollmentNameStr : 1,
				fYrArtsStr : 2,
				fYrSciStr : 3,
				upYrArtsStr : 4,
				upYrSciStr : 5,
				}		#Creating all the headings (Course Name, BA, BAH, BSCH...) and hard code 1st year arts and sci
	
	for columnName in columns:		#write hardcoded column headings (Name, total enrollment, etc)
		programBreakdown.write(0, columns[columnName], columnName)

	hardColumns = len(columns)
	
	for program in programsList:			#Writing all the column headings to the excel sheet
		columns[program] = programsList.index(program) + hardColumns
		programBreakdown.write(0, columns[program], program)

	count = informationStartRow
	for course in courseList:			#Outputs the course codes in column 0 (ANAT 215, 216)
		
		course = course[0]		#unpack the tuple

		courseName = data.grabCourseName(c, course)		
		programBreakdown.write(count, columns[courseNameStr], courseName)

		enrollments = data.grabEnrollmentNumber(c,course)
		programBreakdown.write(count, columns[enrollmentNameStr], enrollments)

		for program in programsList:			#Outputs enrollments for all programs (except 1st year Arts Sci)
			
			studCount = data.grabStudentEnrollment(c, program[0], course)
			programBreakdown.write(count, columns[program], studCount)

		#Breaking down between 1st year and upper year Arts and Sci HONOURS
		firstYrArts = data.grabStudentProgYearEnroll(c, "BAH", 1, course)
		firstYrSci = data.grabStudentProgYearEnroll(c, "BSCH",1, course)

		upYrArts = data.grabStudentEnrollment(c, "BAH", course) - firstYrArts
		upYrSci = data.grabStudentEnrollment(c, "BSCH", course) - firstYrSci

		programBreakdown.write(count, columns[fYrArtsStr], firstYrArts)
		programBreakdown.write(count, columns[fYrSciStr], firstYrSci)

		programBreakdown.write(count, columns[upYrArtsStr], upYrArts)
		programBreakdown.write(count, columns[upYrSciStr], upYrSci)

		count = count + 1

	programBreakdown.set_panes_frozen(True)
	programBreakdown.set_horz_split_pos(1)		#Freeze panes for the first row
	return True

	#CALCULATING PERCENTAGE ENROLLMENTS BASED ON PLAN
def planEnrollments(c,book):
	planBreakdown = book.add_sheet("PlanBreakdownExpanded")		#new sheet 

	columnWidth(planBreakdown, 10)

	courseNameStr = 'Course Name'
	enrollmentsNameStr = 'Enrollments'

	columns = {courseNameStr : 0,
				enrollmentsNameStr : 1}		#hardcoded columns

	for columnName in columns:				#write hardcoded columns 
		planBreakdown.write(0, columns[columnName], columnName)

	hardColumns = len(columns)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()


	planList = data.grabFullPlanList(c)


	# c.execute("SELECT DISTINCT plan FROM students;")		
	# planList = c.fetchall()
	# c.execute("SELECT DISTINCT plan2 FROM students;")
	# plan2List = c.fetchall()
	# c.execute("SELECT DISTINCT plan3 FROM students;")
	# plan3List = c.fetchall()

	# for plan in plan2List:		#MERGING plan2 values with plan 
	# 	try: 
	# 		temp = planList.index(plan)		#check if it is in the original plan list already
	# 	except ValueError:
	# 		if plan[0] != '':			#make sure the plan isn't NULL or "" (which means there is no second plan)
	# 	 		planList.append(plan) 		#if error arises, the plan is not in the original plan

	# for plan in plan3List:		#MERGING plan3 values with plan + plan2
	# 	try: 
	# 		temp = planList.index(plan)	
	# 	except ValueError:
	# 		if plan[0] != '':
	# 			planList.append(plan)

	for plan in planList:		#writing all column headings for each plan
		columns[plan] = planList.index(plan) + hardColumns
		planBreakdown.write(0, columns[plan], plan)

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c, course)		#write down the courses in the first row
		planBreakdown.write(count,columns[courseNameStr],courseName)

		totEnrollments = data.grabEnrollmentNumber(c,course)
		planBreakdown.write(count,columns[enrollmentsNameStr], totEnrollments)

		for plan in planList:		#interate through all the plans

			studCount = data.grabStudentPlanEnroll(c, plan[0], course)	#gotta unpack that plan
			planBreakdown.write(count, columns[plan], studCount)

		count = count + 1

	planBreakdown.set_panes_frozen(True)
	planBreakdown.set_horz_split_pos(1)		#Freeze panes for the first row

	return True

def planSignificantEnrollments(c,book):

	cutoff = 10		#cutoff range for number of plan enrollments

	planBreakdown = book.add_sheet("PlanBreakdown")
	columnWidth(planBreakdown, 10)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	courseNameStr = 'Course Name'

	planList = data.grabFullPlanList(c)

	columns = {courseNameStr : 0,}

	sigPlanList = []		#filter out plans with very little enrollments in DBMS courses (eg ENG or COMM plans)
	
	for plan in planList:
		'''Iterates through each plan. With a particular plan, iterate through all the courses.
			If the number of people in that plan cannot exceed 10 people for any of the courses, 
			they will not be included in this sheet.
			This for loop FILTERS
		'''
		studCount = []		
		addToList = False		

		for course in courseList:		

			course = course[0]
			studCount.append(data.grabStudentPlanEnroll(c, plan[0], course))

		for count in studCount:
			if count > cutoff:	
				addToList = True
				break

		if addToList:		#only add to the new list if there are enough enrollments
			sigPlanList.append(plan)

	for columnName in columns:
		planBreakdown.write(0, columns[columnName], columnName)

	for plan in sigPlanList:		#only write the relevant plans into each column
		columns[plan] = sigPlanList.index(plan) + 1
		planBreakdown.write(0, columns[plan], plan)

	count = 1
	for course in courseList:
		'''This for loop WRITES
		'''
		course = course[0]

		courseName = data.grabCourseName(c, course)
		planBreakdown.write(count,columns[courseNameStr],courseName)

		for plan in sigPlanList:
			studCount = data.grabStudentPlanEnroll(c, plan[0], course)	#gotta unpack that plan
			planBreakdown.write(count, columns[plan], studCount)

		count = count + 1

	planBreakdown.set_panes_frozen(True)
	planBreakdown.set_horz_split_pos(1)		#Freeze panes for the first row
	
	return True

def yearBreakdown(c, book):
	yearBreakdown = book.add_sheet("YearBreakdown")

	columnWidth(yearBreakdown, 7)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	courseNameStr = 'Course Name'
	columns = {courseNameStr : 0,}

	for columnName in columns:
		yearBreakdown.write(0, columns[columnName], columnName)

	c.execute("SELECT DISTINCT proj_level FROM students;")
	yearList = c.fetchall()

	for year in yearList:
		columns[year] = yearList.index(year) + 1
		yearBreakdown.write(0, columns[year],"Year " + str(year[0]))

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c, course)		#write down the courses in the first row
		yearBreakdown.write(count, columns[courseNameStr], courseName)

		for year in yearList:		#iterate through years 1,2,3,4

			yearCount = data.grabStudentYearEnroll(c, year[0], course)	
			yearBreakdown.write(count, columns[year], yearCount)		#write to the sheet enrollment(course,year)

		count = count + 1

	yearBreakdown.set_panes_frozen(True)
	yearBreakdown.set_horz_split_pos(1)

	return True

def planBreakdown(c,book,plan):
	'''Grabs only plans specified in the function call. If plan is 'BCHM',
		it will find BCHM-G_BSC, BCHM-M-BSH, BCHM-P-BSH
	'''
	planBreakdown = book.add_sheet(str(plan) + " Breakdown")
	planRow = 0
	yearRow = 1
	informationStartRow = 2

	courseNameStr = 'Course Name'
	planBreakdown.write(planRow,0, courseNameStr)

	columnWidth(planBreakdown,10)

	c.execute("SELECT DISTINCT course_id FROM courses;")		
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT proj_level FROM students;")
	yearList = c.fetchall()

	c.execute("SELECT DISTINCT plan FROM students WHERE plan LIKE \'" + str(plan) + "%\';")
	planList = c.fetchall()		#will find all the plans that begin with BCHM
	c.execute("SELECT DISTINCT plan2 FROM students WHERE plan LIKE \'" + str(plan) + "%\';")
	plan2List = c.fetchall()		#will find all the plans in plan2 that begin with BCHM
	c.execute("SELECT DISTINCT plan3 FROM students WHERE plan LIKE \'" + str(plan) + "%\';")
	plan3List = c.fetchall()		#will find all the plans in plan3 that begin with BCHM

	# for plan in plan2List:
	# 	print plan[0]
	# 	try: 
	# 		temp = planList.index(plan[0])
	# 		print "hi"
	# 	except ValueError:
	# 		#print "Do Nothing"
	# 		pass
	# 	# Else:
	# 	# 	print "Hi"

	columnsExp = defaultdict(dict)

	count = yearRow
	for plan in planList:
		for year in yearList:
			columnsExp[plan][year] = count
			count = count + 1
			planBreakdown.write(planRow,columnsExp[plan][year], str(plan[0]))
			planBreakdown.write(yearRow,columnsExp[plan][year], "Year: " + str(year[0]))


	count = informationStartRow
	for course in courseList:		#iterate throught courses
		course = course[0]

		courseName = data.grabCourseName(c, course)
		planBreakdown.write(count, 0, courseName)

		for plan in planList:			#iterate through the plans
			for year in yearList:		#iterate through all the years

				enroll = data.grabStudentPlanYearEnroll(c,plan[0],year[0],course)
				planBreakdown.write(count, columnsExp[plan][year], enroll)

		count = count + 1

	planBreakdown.set_panes_frozen(True)
	planBreakdown.set_horz_split_pos(2)

	return True


def programInfo(c, book):
	progInfo = book.add_sheet("ProgramInfo")

	twoDecimalStyle = xlwt.XFStyle()		#styling for using two decimals
	twoDecimalStyle.num_format_str = '0.00'

	columnWidth(progInfo,14)
	c.execute("SELECT DISTINCT program_id FROM program_info;")
	programList = c.fetchall()

	programNameStr = 'Program Name'
	enrollmentNameStr = 'Enrollment'
	unitFeeNameStr = 'Unit Fees'
	formulaFeeNameStr = 'Formula Fees'
	progWeightNameStr = 'Program Weight'
	normUnitsNameStr = 'Normal Units'
	BIUNameStr = 'BIU Value'

	columns = {programNameStr : 0,
				enrollmentNameStr : 1,
				unitFeeNameStr : 2,
				formulaFeeNameStr : 3,
				progWeightNameStr : 4,
				normUnitsNameStr : 5,
				BIUNameStr : 6,
				}

	for columnName in columns:
		progInfo.write(0,columns[columnName],columnName)

	count = 1
	for program in programList:
	
		program = program[0]

		programName = data.grabProgName(c,program)
		progInfo.write(count,columns[programNameStr], programName)

		programName = [programName]	#make into tuple 

		enrollment = data.grabProgEnrollment(c,programName)
		progInfo.write(count, columns[enrollmentNameStr],enrollment)

		unitFee = data.grabUnitFees(c,programName)
		progInfo.write(count, columns[unitFeeNameStr], unitFee, twoDecimalStyle)

		formulaFee = data.grabFormulaFee(c,programName)
		progInfo.write(count,columns[formulaFeeNameStr], formulaFee, twoDecimalStyle)

		progWeight = data.grabProgramWeight(c, programName)
		progInfo.write(count, columns[progWeightNameStr], progWeight, twoDecimalStyle)

		normUnits = data.grabNormalUnits(c,programName)
		progInfo.write(count, columns[normUnitsNameStr], normUnits)

		count = count + 1

	BIUVal = data.grabBIU(c)
	progInfo.write(1,columns[BIUNameStr],BIUVal)


	progInfo.set_panes_frozen(True)
	progInfo.set_horz_split_pos(1)

	return True


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

	# tuitionGrantTotals(c,book)

	# programEnrollments(c,book)

	planSignificantEnrollments(c,book)

	# yearBreakdown(c,book)

	rawPlanList = data.grabFullPlanList(c)

	checkPlanList = []
	for plan in rawPlanList:
		try: 
			temp = checkPlanList.index(plan)

		except ValueError:
			if plan[0] != 

	print checkPlanList

	planBreakdown(c,book,"BCHM")
	
	planBreakdown(c,book,"LISC")

	programInfo(c, book)


	#saving the file into a direcotry
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
