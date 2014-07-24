#-------------------------------------------------------------------------------
# Name:        
#
#			testing ways to output to Excel
#			sheets that are output
#				- tuition/grant totals for all courses
#				- breakdown of courses based on program
#				- breakdown of courses based on plan (DBMS LISC, BCHM...)
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
import xlwt

import extractData as data
import calcGrant as grant
import calcTuition as tuition

def main():

	conn = data.connectDB()
	c = conn.cursor()

	sheetName = "DBMS Enrollment Data.xls"

	cdLocation = os.getcwd()
	excelLocation = cdLocation + "\\" + sheetName

	try:
		os.remove(excelLocation)
	except WindowsError:
		pass

	book = xlwt.Workbook()

	#CALCULATING TUITION AND GRANT TOTALS~~~~~~~~~~~~~~~~~~~~~~~~~~~
	courseTotals = book.add_sheet("CourseTotals")

	columns = {'Course Name' : 0, 
				'Term' : 1, 
				'Credits' : 2, 
				'Enrollment' : 3, 
				'Grant Value' : 4, 
				'Tuition Value' : 5,
				'Total Revenue' : 6,
				}

	for heading, colNum in columns.iteritems():
		courseTotals.write(0, colNum, heading)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	count = 1 		#used to increment the row number
	for course in courseList:
		course = course[0]		#unpack the tuple

		print course

		courseName = data.grabCourseName(c,course)
		courseTotals.write(count, columns['Course Name'], courseName)

		term = data.grabCourseTerm(c, course)
		courseTotals.write(count, columns['Term'], term)

		credits = data.grabCourseCredits(c,course)
		courseTotals.write(count, columns['Credits'] , credits)

		enrollment = data.grabEnrollmentNumber(c,course)
		courseTotals.write(count, columns['Enrollment'] , enrollment)

		grantVal = grant.runAppCourse(course)
		courseTotals.write(count,columns['Grant Value'],grantVal)

		tuitionVal = tuition.runAppCourse(course)
		courseTotals.write(count, columns['Tuition Value'], tuitionVal)

		total = grantVal + tuitionVal
		courseTotals.write(count, columns['Total Revenue'], total)

		count = count + 1 	#used to icnrement row number

	courseTotals.set_panes_frozen(True)
	courseTotals.set_horz_split_pos(1)		#Freeze panes for the first row

	#CALCULATING ENROLLMENTS BASED ON PROGRAM~~~~~~~~~~~~~~~~~~~~~~~
	programBreakdown = book.add_sheet("programBreakdown")

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
		programBreakdown.write(0,columns[columnName], columnName)
	
	for program in programsList:			#Writing all the column headings to the excel sheet
		columns[program] = programsList.index(program) + 1
		programBreakdown.write(0,columns[program],program)

	count = 1
	for course in courseList:			#Outputs the course codes in column 0 (ANAT 215, 216)
		
		course = course[0]		#unpack the tuple

		courseName = data.grabCourseName(c,course)		
		programBreakdown.write(count,columns[courseNameStr], courseName)

		for program in programsList:			#Outputs enrollments for all programs (except 1st year Arts Sci)
			
			studCount = data.grabStudentEnrollment(c, program[0], course)
			programBreakdown.write(count, columns[program], studCount)

		#Breaking down between 1st year and upper year Arts and Sci HONOURS
		firstYrArts = data.grabStudentYearCourse(c, "BAH", 1, course)
		firstYrSci = data.grabStudentYearCourse(c,"BSCH",1,course)

		upYrArts = data.grabStudentEnrollment(c, "BAH",course) - firstYrArts
		upYrSci = data.grabStudentEnrollment(c, "BSCH",course) - firstYrSci

		programBreakdown.write(count, columns[fYrArtsStr], firstYrArts)
		programBreakdown.write(count, columns[fYrSciStr], firstYrSci)

		programBreakdown.write(count, columns[upYrArtsStr], upYrArts)
		programBreakdown.write(count,columns[upYrSciStr], upYrSci)

		count = count + 1


	#CALCULATING PERCENTAGE ENROLLMENTS BASED ON PLAN
	planBreakdown = book.add_sheet("planBreakdown")		#new sheet 

	c.execute("SELECT DISTINCT plan FROM students;")		
	planList = c.fetchall()

	columns = {courseNameStr : 0,}		#hardcoded column

	for columnName in columns:				#write hardcoded columns 
		planBreakdown.write(0,columns[columnName],columnName)

	for plan in planList:		#writing all column headings for each plan
		columns[plan] = planList.index(plan) + 1
		planBreakdown.write(0,columns[plan],plan)

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c,course)		#write down the courses in the first row
		planBreakdown.write(count,columns[courseNameStr],courseName)

		for plan in planList:		#interate through all the plans

			studCount = data.grabStudentPlanCourse(c,plan[0],course)	#gotta unpack that plan
			planBreakdown.write(count,columns[plan], studCount)

		count = count + 1
	print planList
	print len(planList)



	book.save(sheetName)


if __name__ == '__main__':
	main()
