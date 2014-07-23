#-------------------------------------------------------------------------------
# Name:        
#
#			testing ways to output to Excel
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

from collections import defaultdict

import extractData as data
import calcGrant as grant
import calcTuition as tuition



def main():

	conn = data.connectDB()
	c = conn.cursor()

	cdLocation = os.getcwd()
	excelLocation = cdLocation + "\\lol.xls"

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
		print heading
		print colNum
		courseTotals.write(0, colNum, heading)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	count = 1 		#used to increment the row number
	for course in courseList:
		course = course[0]		#unpack the tuple

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

	#CALCULATING ENROLLMENTS BASED ON PROGRAM~~~~~~~~~~~~~~~~~~~~~~~
	programBreakdown = book.add_sheet("programBreakdown")

	c.execute("SELECT DISTINCT program FROM students;")
	programsList = c.fetchall()

	columns = {'Course Name' : 0}
	for program in programsList:
		columns[program] = programsList.index(program) + 1

	print columns
	count = 1
	for course in courseList:
		course = course[0]
		programBreakdown.write(count,columns['Course Name'], course)
		for program in programsList:
			studCount = data.grabStudentEnrollment(c, program[0], course)
			programBreakdown.write(count, columns[program], studCount)

		count = count + 1
	# columns = {'Course Name' : 0,
	# 			''}

	book.save("lol.xls")


if __name__ == '__main__':
	main()