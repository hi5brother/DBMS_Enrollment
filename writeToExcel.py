#-------------------------------------------------------------------------------
# Name:        
#
#			testing ways to output to Excel
#			sheets that are output
#				- tuition/grant totals for all courses
#				- breakdown of courses based on program
#				- breakdown of courses based on plan (DBMS LISC, BCHM...)
#				- breakdown of courses based on year (1,2,3,4)
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

	columns = {'Course Name' : 0, 
				'Term' : 1, 
				'Credits' : 2, 
				'Enrollment' : 3, 
				'Grant Value' : 4, 
				'Tuition Value' : 5,
				'Total Revenue' : 6,
				'Grant per Student' : 7,
				'Tuition per Student' : 8,
				'Revenue per Student' : 9
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
		courseTotals.write(count, columns['Course Name'], courseName)

		term = data.grabCourseTerm(c, course)
		courseTotals.write(count, columns['Term'], term)

		credits = data.grabCourseCredits(c,course)
		courseTotals.write(count, columns['Credits'] , credits, twoDecimalStyle)

		enrollment = data.grabEnrollmentNumber(c, course)
		enrollTot = enrollTot + enrollment
		courseTotals.write(count, columns['Enrollment'] , enrollment)

		grantVal = grant.runAppCourse(course)
		grantTot = grantTot + grantVal
		courseTotals.write(count, columns['Grant Value'], grantVal, twoDecimalStyle)

		tuitionVal = tuition.runAppCourse(course)
		tuitionTot = tuitionTot + tuitionVal
		courseTotals.write(count, columns['Tuition Value'], tuitionVal, twoDecimalStyle)

		total = grantVal + tuitionVal
		totalTot = totalTot + total
		courseTotals.write(count, columns['Total Revenue'], total, twoDecimalStyle)

		grantPerStud = grantVal / enrollment
		courseTotals.write(count, columns['Grant per Student'], grantPerStud, twoDecimalStyle)

		tuitionPerStud = tuitionVal / enrollment
		courseTotals.write(count, columns['Tuition per Student'], tuitionPerStud, twoDecimalStyle)

		revenuePerStud = total / enrollment
		courseTotals.write(count, columns['Revenue per Student'], revenuePerStud, twoDecimalStyle)

		count = count + 1 	#used to icnrement row number

	courseTotals.write(count,columns['Enrollment'], enrollTot)		#HARDCODE FOR THE TOTALS OF CERTAIN METRICS
	courseTotals.write(count, columns['Grant Value'], grantTot)
	courseTotals.write(count,columns['Tuition Value'], tuitionTot)
	courseTotals.write(count,columns['Total Revenue'], totalTot)

	courseTotals.set_panes_frozen(True)
	courseTotals.set_horz_split_pos(1)		#Freeze panes for the first row

	#CALCULATING ENROLLMENTS BASED ON PROGRAM~~~~~~~~~~~~~~~~~~~~~~~
def programEnrollments(c,book):
	programBreakdown = book.add_sheet("ProgramBreakdown")

	columnWidth(programBreakdown, 6)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT program FROM students;")
	programsList = c.fetchall()

	courseNameStr = 'Course Name'
	fYrArtsStr = '1st Year Arts'		#these help differentiate between 1st year artsci HONOURS and upper year artsci HONOURS
	fYrSciStr = '1st Year Science'
	upYrArtsStr = 'Upper Year Science'
	upYrSciStr = 'Upper Year Arts'
	totEnrollmentsStr = 'Total Enrollments'

	columns = {courseNameStr : 0,
				fYrArtsStr : len(programsList) + 1,
				fYrSciStr : len(programsList) + 2,
				upYrArtsStr : len(programsList) + 3,
				upYrSciStr : len(programsList) + 4,

				totEnrollmentsStr : len(programsList) + 5,

				}		#Creating all the headings (Course Name, BA, BAH, BSCH...) and hard code 1st year arts and sci
	
	for columnName in columns:		#write hardcoded column headings (Name, total enrollment, etc)
		programBreakdown.write(0, columns[columnName], columnName)
	
	for program in programsList:			#Writing all the column headings to the excel sheet
		columns[program] = programsList.index(program) + 1
		programBreakdown.write(0, columns[program], program)

	count = 1
	for course in courseList:			#Outputs the course codes in column 0 (ANAT 215, 216)
		
		course = course[0]		#unpack the tuple

		courseName = data.grabCourseName(c, course)		
		programBreakdown.write(count, columns[courseNameStr], courseName)

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


	#CALCULATING PERCENTAGE ENROLLMENTS BASED ON PLAN
def planEnrollments(c,book):
	planBreakdown = book.add_sheet("PlanBreakdown")		#new sheet 

	columnWidth(planBreakdown, 10)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	courseNameStr = 'Course Name'

	c.execute("SELECT DISTINCT plan FROM students;")		
	planList = c.fetchall()

	columns = {courseNameStr : 0,}		#hardcoded column

	for columnName in columns:				#write hardcoded columns 
		planBreakdown.write(0, columns[columnName], columnName)

	for plan in planList:		#writing all column headings for each plan
		columns[plan] = planList.index(plan) + 1
		planBreakdown.write(0, columns[plan], plan)

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c, course)		#write down the courses in the first row
		planBreakdown.write(count,columns[courseNameStr],courseName)

		for plan in planList:		#interate through all the plans

			studCount = data.grabStudentPlanEnroll(c, plan[0], course)	#gotta unpack that plan
			planBreakdown.write(count, columns[plan], studCount)

		count = count + 1

	planBreakdown.set_panes_frozen(True)
	planBreakdown.set_horz_split_pos(1)		#Freeze panes for the first row

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

		for year in yearList:

			yearCount = data.grabStudentYearEnroll(c, year[0], course)
			yearBreakdown.write(count, columns[year], yearCount)

		count = count + 1

	yearBreakdown.set_panes_frozen(True)
	yearBreakdown.set_horz_split_pos(1)

def programInfo(c, book):
	progInfo = book.add_sheet("ProgramInfo")

	columnWidth(progInfo,14)
	c.execute("SELECT DISTINCT program_id FROM program_info;")
	programList = c.fetchall()

	programNameStr = 'Program Name'
	unitFeeNameStr = 'Unit Fees'
	formulaFeeNameStr = 'Formula Fees'
	progWeightNameStr = 'Program Weight'
	normUnitsNameStr = 'Normal Units'


	columns = {programNameStr : 0,
				unitFeeNameStr : 1,
				formulaFeeNameStr : 2,
				progWeightNameStr : 3,
				normUnitsNameStr : 4,
				}

	for columnName in columns:
		progInfo.write(0,columns[columnName],columnName)

	count = 1
	for program in programList:
	
		program = program[0]

		programName = data.grabProgName(c,program)
		progInfo.write(count,columns[programNameStr], programName)

		programName = [programName]	#make into tuple 
		unitFee = data.grabUnitFees(c,programName)
		progInfo.write(count, columns[unitFeeNameStr], unitFee)

		formulaFee = data.grabFormulaFee(c,programName)
		progInfo.write(count,columns[formulaFeeNameStr], formulaFee)

		progWeight = data.grabProgramWeight(c, programName)
		progInfo.write(count, columns[progWeightNameStr], progWeight)

		normUnits = data.grabNormalUnits(c,programName)
		progInfo.write(count, columns[normUnitsNameStr], normUnits)

		count = count + 1

	progInfo.set_panes_frozen(True)
	progInfo.set_horz_split_pos(1)


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

	tuitionGrantTotals(c,book)

	programEnrollments(c,book)

	planEnrollments(c,book)

	yearBreakdown(c,book)

	programInfo(c, book)

	try:
		book.save(sheetName)
	except IndexError:
		pass
	except IOError:
		print "Error: Please close all Excel workbooks."

	readBook = xlrd.open_workbook(excelLocation)


if __name__ == '__main__':
	runApp()
