#-------------------------------------------------------------------------------
# Name:        plan enrollments (only using the significant numbers)

# Purpose:		will output enrollments in each course based on plan (e.g. "BCHM-M-BSH" or "LISC-M-BSH")
#				will only output plans with a certain number of enrollments. It means we can exclude the
#				very obscure plans from the spreadsheet
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

def write(c, book):
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