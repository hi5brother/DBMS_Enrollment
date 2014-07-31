#-------------------------------------------------------------------------------
# Name:        year enrollments

# Purpose:		will output enrollments in each year
#				does not discriminate on plan or program
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

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data

def write(c,book):
	sheet = book.add_sheet("YearTotals")

	columnWidth(sheet, 7)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	courseNameStr = 'Course Name'
	columns = {courseNameStr : 0,}

	for columnName in columns:
		sheet.write(0, columns[columnName], columnName)

	c.execute("SELECT DISTINCT proj_level FROM students;")
	yearList = c.fetchall()

	for year in yearList:
		columns[year] = yearList.index(year) + 1
		sheet.write(0, columns[year],"Year " + str(year[0]))

	count = 1
	for course in courseList:		#iterate through all the courses

		course = course[0]

		courseName = data.grabCourseName(c, course)		#write down the courses in the first row
		sheet.write(count, columns[courseNameStr], courseName)

		for year in yearList:		#iterate through years 1,2,3,4

			yearCount = data.grabStudentYearEnroll(c, year[0], course)	
			sheet.write(count, columns[year], yearCount)		#write to the sheet enrollment(course,year)

		count = count + 1

	freezePanes(sheet,1)

	return True