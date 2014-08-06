#-------------------------------------------------------------------------------
# Name:        plan breakdown enrollments

# Purpose:		will output enrollments in each plan and year
#				will take the plan e.g. "BCHM" or "MECH" and find all the major/minor/spec with that
#				
#							BCHM M 	BCHM S 		BCHM G...
#				course... Year 1... Year 2... Year 3... Year 4...
#
# Author:      DBMS
#
# Created:     31/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
from formatting import columnWidth, freezePanes


from collections import defaultdict

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data

def write (c,book,plan):
	'''Grabs only plans specified in the function call. If plan is 'BCHM',
		it will find BCHM-G_BSC, BCHM-M-BSH, BCHM-P-BSH
	'''
	sheet = book.add_sheet(str(plan) + " Breakdown")
	planRow = 0
	yearRow = 1
	informationStartRow = 2

	courseNameStr = 'Course Name'
	termStr = 'Term'
	sheet.write(planRow,0, courseNameStr)
	
	columnWidth(sheet,10)

	c.execute("SELECT DISTINCT course_id FROM courses;")		
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT proj_level FROM students;")
	yearList = c.fetchall()

	c.execute("SELECT DISTINCT plan FROM students WHERE plan LIKE \'" + str(plan) + "%\';")
	planList = c.fetchall()		#will find all the plans that begin with BCHM
	c.execute("SELECT DISTINCT plan2 FROM students WHERE plan2 LIKE \'" + str(plan) + "%\';")
	plan2List = c.fetchall()		#will find all the plans in plan2 that begin with BCHM
	c.execute("SELECT DISTINCT plan3 FROM students WHERE plan3 LIKE \'" + str(plan) + "%\';")
	plan3List = c.fetchall()		#will find all the plans in plan3 that begin with BCHM

	for plan in plan2List:					#MERGING plan2 values with plan 

		try: 
			temp = planList.index(plan)		#check if it is in the original plan list already
		
		except ValueError:
			if plan[0] != '':				#make sure the plan isn't NULL or "" (which means there is no second plan)
		 		planList.append(plan) 		#if error arises, the plan is not in the original plan

	for plan in plan3List:					#MERGING plan3 values with plan + plan2

		try: 
			temp = planList.index(plan)	

		except ValueError:
			if plan[0] != '':
				planList.append(plan)

	columnsExp = defaultdict(dict)

	count = yearRow 	
	for plan in planList:
		for year in yearList:
			columnsExp[plan][year] = count 			#setting up the columns
			count = count + 1
			sheet.write(planRow,columnsExp[plan][year], str(plan[0]))		#outputs the Plan heading
			sheet.write(yearRow,columnsExp[plan][year], "Year: " + str(year[0]))	#outputs the year heading 

	count = informationStartRow
	for course in courseList:						#iterate throught courses
		course = course[0]

		courseName = data.grabCourseName(c, course)
		sheet.write(count, 0, courseName)

		for plan in planList:						#iterate through the plans
			for year in yearList:					#iterate through all the years

				enroll = data.grabStudentPlanYearEnroll(c,plan[0],year[0],course)	#output the enrollment based on year/plan
				sheet.write(count, columnsExp[plan][year], enroll)

		count = count + 1

	freezePanes(sheet,2)

	return True
	