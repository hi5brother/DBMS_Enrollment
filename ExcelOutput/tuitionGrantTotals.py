#-------------------------------------------------------------------------------
# Name:        tuitionGrantTotals

# Purpose:		will output the revenues from tuition and grants
#				changes column width
#				freezes panes
#
# Author:      DBMS
#
# Created:     30/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
from formatting import columnWidth, freezePanes

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data
import calcGrant as grant
import calcTuition as tuition

def write(c,book):
	'''	Outputs the sheet with all the revenue values.
	'''
	sheet = book.add_sheet("CourseTotals")

	freezePanes(sheet, 1)

	twoDecimalStyle = xlwt.XFStyle()		#styling for using two decimals
	twoDecimalStyle.num_format_str = '0.00'

	columnWidth(sheet, 14)

	courseNameStr = 'Course Name'		#hard coded values
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
		sheet.write(0, colNum, heading)

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
		sheet.write(count, columns[courseNameStr], courseName)

		term = data.grabCourseTerm(c, course)
		sheet.write(count, columns[termNameStr], term)

		credits = data.grabCourseCredits(c,course)
		sheet.write(count, columns[creditsNameStr] , credits, twoDecimalStyle)

		enrollment = data.grabEnrollmentNumber(c, course)
		enrollTot = enrollTot + enrollment
		sheet.write(count, columns[enrollmentNameStr] , enrollment)

		grantVal = grant.runAppCourse(course)
		grantTot = grantTot + grantVal
		sheet.write(count, columns[grantValNameStr], grantVal, twoDecimalStyle)

		tuitionVal = tuition.runAppCourse(course)
		tuitionTot = tuitionTot + tuitionVal
		sheet.write(count, columns[tuitValNameStr], tuitionVal, twoDecimalStyle)

		total = grantVal + tuitionVal
		totalTot = totalTot + total
		sheet.write(count, columns[totRevNameStr], total, twoDecimalStyle)

		grantPerStud = grantVal / enrollment
		sheet.write(count, columns[grantStudNameStr], grantPerStud, twoDecimalStyle)

		tuitionPerStud = tuitionVal / enrollment
		sheet.write(count, columns[tuitStudNameStr], tuitionPerStud, twoDecimalStyle)

		revenuePerStud = total / enrollment
		sheet.write(count, columns[revStudNameStr], revenuePerStud, twoDecimalStyle)

		count = count + 1 	#used to icnrement row number

	sheet.write(count,columns[courseNameStr], "Totals")
	sheet.write(count,columns[enrollmentNameStr], enrollTot)		#HARDCODE FOR THE TOTALS OF CERTAIN METRICS
	sheet.write(count, columns[grantValNameStr], grantTot, twoDecimalStyle)
	sheet.write(count,columns[tuitValNameStr], tuitionTot, twoDecimalStyle)
	sheet.write(count,columns[totRevNameStr], totalTot, twoDecimalStyle)

	return True
