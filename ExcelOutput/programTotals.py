#-------------------------------------------------------------------------------
# Name:        program enrollments

# Purpose:		will output enrollments in each course based on program (e.g. "BSCH" or "BA")
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
	sheet = book.add_sheet("ProgramTotals")

	freezePanes(sheet,1)
	informationStartRow = 1
	columnWidth(sheet, 6)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT program FROM students;")
	programsList = c.fetchall()

	courseNameStr = 'Course Name'
	termNameStr = 'Term'
	enrollmentNameStr = 'Enrollments'

	fYrArtsStr = 'Arts (1st)'		#these help differentiate between 1st year artsci HONOURS and upper year artsci HONOURS
	fYrSciStr = 'Science (1st)'
	upYrArtsStr = 'Arts Hon (2-4)'
	upYrSciStr = 'Science Hon (2-4)'

	columns = {
				courseNameStr : 0,
				termNameStr : 1,
				enrollmentNameStr : 2,
				fYrArtsStr : 3,
				fYrSciStr : 4,
				upYrArtsStr : 5,
				upYrSciStr : 6,
				}		#Creating all the headings (Course Name, BA, BAH, BSCH...) and hard code 1st year arts and sci
	
	for columnName in columns:		#write hardcoded column headings (Name, total enrollment, etc)
		sheet.write(0, columns[columnName], columnName)

	hardColumns = len(columns)
	
	for program in programsList:			#Writing all the column headings to the excel sheet
		columns[program] = programsList.index(program) + hardColumns
		sheet.write(0, columns[program], program)

	count = informationStartRow
	for course in courseList:			#Outputs the course codes in column 0 (ANAT 215, 216)
		
		course = course[0]		#unpack the tuple

		courseName = data.grabCourseName(c, course)		
		sheet.write(count, columns[courseNameStr], courseName)

		term = data.grabCourseTerm(c,course)
		sheet.write(count, columns[termNameStr], term)

		enrollments = data.grabEnrollmentNumber(c,course)
		sheet.write(count, columns[enrollmentNameStr], enrollments)

		for program in programsList:			#Outputs enrollments for all programs (except 1st year Arts Sci)

			studCount = data.grabStudentEnrollment(c, program[0], course)
			sheet.write(count, columns[program], studCount)

		#Breaking down between 1st year and upper year Arts and Sci HONOURS
		firstYrArts = data.grabStudentProgYearEnroll(c, "BAH", 1, course)
		firstYrSci = data.grabStudentProgYearEnroll(c, "BSCH",1, course)

		upYrArts = data.grabStudentEnrollment(c, "BAH", course) - firstYrArts
		upYrSci = data.grabStudentEnrollment(c, "BSCH", course) - firstYrSci

		sheet.write(count, columns[fYrArtsStr], firstYrArts)
		sheet.write(count, columns[fYrSciStr], firstYrSci)

		sheet.write(count, columns[upYrArtsStr], upYrArts)
		sheet.write(count, columns[upYrSciStr], upYrSci)

		count = count + 1


	return True