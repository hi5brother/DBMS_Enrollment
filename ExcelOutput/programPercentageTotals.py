#-------------------------------------------------------------------------------
# Name:        percentage breakdowns

# Purpose:		will display the breakdown of each course by faculty using percentages
#				programs are labeled as DBMS, ArtSci, Nurs, etc. rather than BA1, BAH, 
#
# Author:      DBMS
#
# Created:     14/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
from formatting import columnWidth, freezePanes

from collections import defaultdict

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, parentdir)
import extractData as data

def write(c, book):
	'''
	Tried to imitate what Dan Adams had for his "Enrollment by Program" Sheet
	For each program, it will have a column for # of weighted enrollments, and also percentage of total enrollments
	'''

	sheet = book.add_sheet("Weighted Program Enroll")
	
	twoDecimalStyle = xlwt.XFStyle()
	twoDecimalStyle.num_format_str = '0.00'

	freezePanes(sheet,1)
	informationStartRow = 1
	columnWidth(sheet, 9)
	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	c.execute("SELECT DISTINCT program FROM students;")
	programsList = c.fetchall()

	courseNameStr = 'Course Name'
	termNameStr = 'Term'
	enrollmentNameStr = 'W. Enrollments'

	DBMSNameStr = "W. DBMS"
	DBMSPerNameStr = "% DBMS"

	#List of all the DBMS plans. This excludes the minors. 

	DBMSPlans = ['LISC-G-BSC',
					'LISC-M-BSH',
					'LISC-P-BSH',
					'LISC-Z-3',
					'BCHM-G-BSC',
					'BCHM-M-BSH',
					'BCHM-P-BSH',
					'BCHM-Z-3',
					]

	ArtSciNameStr = "W. ArtSci"		#all other plans with degree program BA, BAH, BSC...
	ArtSciPerNameStr = "% ArtSci"

	NursNameStr = "W. NURS"		#all those with  BNURS 
	NursPerNameStr = "% NURS"

	EngNameStr = "W. ENG"		#all those with BSCE, , etc
	EngPerNameStr = "% ENG"	

	CommNameStr = "W. COMM"
	CommPerNameStr = "% COMM"

	columns = {
				courseNameStr : 0,
				termNameStr : 1,
				enrollmentNameStr : 2,
				DBMSNameStr : 3,
				DBMSPerNameStr: 4,
				ArtSciNameStr : 5,
				ArtSciPerNameStr : 6,
				NursNameStr : 7,
				NursPerNameStr : 8,
				EngNameStr : 9,
				EngPerNameStr : 10,
				CommNameStr : 11,
				CommPerNameStr : 12,
				}

	for columnName in columns:
		sheet.write(0, columns[columnName], columnName)

	count = informationStartRow
	courseWeightedTotal = 0


	for course in courseList:

		course = course[0]

		courseWeight = data.grabCourseCredits(c, course)		
		weighting = courseWeight / 3.0 		#the weighting adjusts the number of Full Time Enrollments (FTE)

		courseName = data.grabCourseName(c, course)
		sheet.write(count, columns[courseNameStr], courseName)

		term = data.grabCourseTerm(c, course)
		sheet.write(count, columns[termNameStr], term)
		
		enrollments = data.grabEnrollmentNumber(c, course)
		enrollments = enrollments * weighting			#total weighted
		sheet.write(count, columns[enrollmentNameStr], enrollments)

		courseWeightedTotal = courseWeightedTotal + enrollments

		DBMSEnrollments = 0
		for plan in DBMSPlans:
			DBMSEnrollments = DBMSEnrollments + data.grabStudentPlanEnroll(c,plan,course)

		#DBMS Columns
		DBMSEnrollments = DBMSEnrollments * weighting		#number of all those in DBMS majors
		sheet.write(count,columns[DBMSNameStr],DBMSEnrollments)

		DBMSPerEnrollments = DBMSEnrollments / enrollments 			#Percentage of all those in DBMS majors
		sheet.write(count, columns[DBMSPerNameStr], DBMSPerEnrollments * 100, twoDecimalStyle)
		
		#Nursing Columns
		NursEnrollments = data.grabStudentEnrollment(c, "BNSC", course)
		sheet.write(count, columns[NursNameStr], NursEnrollments)

		NursPerEnrollments = NursEnrollments / enrollments
		sheet.write(count, columns[NursPerNameStr], NursPerEnrollments * 100, twoDecimalStyle)

		#Engineering Columns
		EngEnrollments = data.grabStudentEnrollment(c, "BSCE", course)
		EngEnrollments = EngEnrollments + data.grabStudentEnrollment(c, "UENG", course)
		sheet.write(count, columns[EngNameStr], EngEnrollments)

		EngPerEnrollments = EngEnrollments / enrollments
		sheet.write(count, columns[EngPerNameStr], EngPerEnrollments * 100, twoDecimalStyle)

		#Commerce Columns
		CommEnrollments = data.grabStudentEnrollment(c, "BCOM", course)
		sheet.write(count, columns[CommNameStr], CommEnrollments)

		CommPerEnrollments = CommEnrollments / enrollments
		sheet.write(count, columns[CommPerNameStr], CommPerEnrollments * 100, twoDecimalStyle)

		#ArtSci Columns 
		ArtSciEnrollments = enrollments - DBMSEnrollments - NursEnrollments - EngEnrollments - CommEnrollments
		sheet.write(count, columns[ArtSciNameStr], ArtSciEnrollments)

		ArtSciPerEnrollments = ArtSciEnrollments / enrollments
		sheet.write(count, columns[ArtSciPerNameStr], ArtSciPerEnrollments * 100, twoDecimalStyle)

		count = count + 1

	return True