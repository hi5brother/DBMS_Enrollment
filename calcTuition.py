#-------------------------------------------------------------------------------
# Name:        calculates the money from tuition proportional to number of courses taken 
#               income per student = DBMS credits taken x unit fee (varies by program)
#	
#				calculates money from tuition for each course also
# Purpose:
#
# Author:      DBMS
#
# Created:     15/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import extractData	#module to extract all the data for a single record for each student

import sqlite3
import sys
import os

def studentTuition(connDB, stude_id):			#pass in the student and calculate tuition of the student

	program = extractData.grabStudentProgram(connDB, stude_id)	

	coursesRaw = extractData.grabStudentCourses(connDB, stude_id)

	unitFee = extractData.grabUnitFees(connDB,program)

	for i in reversed(range(len(coursesRaw))):
		if coursesRaw[i] == None:			#eliminates the none courses
			courses = coursesRaw[:i]	
	
	creditsList = []
	for course_id in courses:		#finds the credits of each course that the student took
		creditsList.append(extractData.grabCourseCredits(connDB, course_id))
	
	creditSum = 0
	for credit in creditsList:		#sum up all the credits that the student was enrolled in
		creditSum = creditSum + (credit)	#used to unpack the tuple

	revenueGenerated = creditSum * unitFee		#formula to calculate revenue from each student

	return revenueGenerated

def courseTuition(connDB, course_id):
	#grab all students who enrolled in that course
	connDB.execute('''SELECT stud_id 		
						FROM students 
						WHERE course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?;''',(course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))

	studentsList = connDB.fetchall()

	courseTuitionTotal = 0

	for student in studentsList:

		stude_id = student[0]

		program = extractData.grabStudentProgram(connDB, stude_id)

		unitFee = extractData.grabUnitFees(connDB, program)

		courseCredit = extractData.grabCourseCredits(connDB,course_id)

		tuitionGenerated = courseCredit * unitFee

		courseTuitionTotal = courseTuitionTotal + tuitionGenerated

	return courseTuitionTotal

def runApp():
	conn = extractData.connectDB()
	c = conn.cursor()
	c.execute("SELECT COUNT (*) FROM students")		#find how many students are in the data base

	val = c.fetchone()
	numOfStudents = int(val[0])

	revenueGeneratedTotal = 0
	for i in range(numOfStudents):		#loops through all the students and calculates money from each student
		revenueGeneratedTotal = revenueGeneratedTotal + studentTuition(c, i + 1)
	
	return revenueGeneratedTotal


def runAppCourse(course):
	conn = extractData.connectDB()
	c = conn.cursor()

	return courseTuition(c , course)


if __name__ == '__main__':
	total2 = runApp()
	total1 = 0
	total1 = total1 + runAppCourse(1)
	total1 = total1 + runAppCourse(2)
	total1 = total1 + runAppCourse(3)
	
	print total2

	print total1