#-------------------------------------------------------------------------------
# Name:        plan enrollments (only using the significant numbers) IN PERCENTAGES

# Purpose:		will output enrollments in each course based on plan (e.g. "BCHM-M-BSH" or "LISC-M-BSH")
#				will only output plans with a certain number of enrollments. It means we can exclude the
#				very obscure plans from the spreadsheet
# Author:      DBMS
#
# Created:     22/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
from formatting import columnWidth, freezePanes

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data

def write(c, book):
	cutoff = 10		#cutoff range for number of plan enrollments

	twoDecimalStyle = xlwt.XFStyle()
	twoDecimalStyle.num_format_str = '0.00'

	planBreakdown = book.add_sheet("Plan Breakdown Percentage")
	columnWidth(planBreakdown, 10)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	courseNameStr = 'Course Name'
	termNameStr = 'Term'
	enrollmentsNameStr = 'Enrollments'

	planList = data.grabFullPlanList(c)

	columns = {courseNameStr : 0,
				termNameStr : 1,
				enrollmentsNameStr : 2}

	hardCodedColumns = len(columns)

	sigPlanList = []		#filter out plans with very little enrollments in DBMS courses (eg ENG or COMM plans)
	
	for plan in planList:
		'''Iterates through each plan. With a particular plan, iterate through all the courses.
			If the number of people in that plan cannot exceed 10 people for any of the courses, 
			they will not be included in this sheet.
			
			The second for loop FILTERS
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
		columns[plan] = sigPlanList.index(plan) + hardCodedColumns
		planBreakdown.write(0, columns[plan], plan)

	count = 1
	for course in courseList:
		'''This for loop WRITES
		'''
		course = course[0]

		courseName = data.grabCourseName(c, course)
		planBreakdown.write(count,columns[courseNameStr],courseName)

		term = data.grabCourseTerm(c, course)
		planBreakdown.write(count, columns[termNameStr], term)

		enrollments = data.grabEnrollmentNumber(c, course)
		planBreakdown.write(count, columns[enrollmentsNameStr],enrollments)

		for plan in sigPlanList:
			studCount = data.grabStudentPlanEnroll(c, plan[0], course)	#gotta unpack that plan

			studCountPercent = float(studCount) / enrollments

			if studCountPercent != 0.0:
				planBreakdown.write(count, columns[plan], studCountPercent * 100, twoDecimalStyle)
			else:
				planBreakdown.write(count, columns[plan], None)

		count = count + 1

	planBreakdown.set_panes_frozen(True)
	planBreakdown.set_horz_split_pos(1)		#Freeze panes for the first row
	
	return True