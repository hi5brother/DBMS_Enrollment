#-------------------------------------------------------------------------------
# Name:        plan enrollments

# Purpose:		will output enrollments in each course based on plan (e.g. "BCHM-M-BSH" or "LISC-M-BSH")
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

def write(c,book):
	sheet = book.add_sheet("PlanTotalsExpanded")		#new sheet 

	freezePanes(sheet, 1)
	
	columnWidth(sheet, 10)

	courseNameStr = 'Course Name'
	termNameStr = 'Term'
	enrollmentsNameStr = 'Enrollments'

	columns = {courseNameStr : 0,
				termNameStr : 1,
				enrollmentsNameStr : 2}		#hardcoded columns

	for columnName in columns:				#write hardcoded columns 
		sheet.write(0, columns[columnName], columnName)

	hardColumns = len(columns)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()


	planList = data.grabFullPlanList(c)

	for plan in planList:		#writing all column headings for each plan
		columns[plan] = planList.index(plan) + hardColumns
		sheet.write(0, columns[plan], plan)

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c, course)		#write down the courses in the first row
		sheet.write(count,columns[courseNameStr],courseName)

		term = data.grabCourseTerm(c, course)
		sheet.write(count, columns[termNameStr], term)

		totEnrollments = data.grabEnrollmentNumber(c,course)
		sheet.write(count,columns[enrollmentsNameStr], totEnrollments)

		for plan in planList:		#interate through all the plans

			studCount = data.grabStudentPlanEnroll(c, plan[0], course)	#gotta unpack that plan
			sheet.write(count, columns[plan], studCount)

		count = count + 1



	return True