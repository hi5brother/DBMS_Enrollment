#-------------------------------------------------------------------------------
# Name:        
#				grabs the relevant data and determines grant money for each student
#
#				grabs data for grant money of a course				
#			
# Purpose:
#
# Author:      DBMS
#
# Created:     21/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import extractData as data

import sqlite3
import sys
import os

def studentGrant(connDB,stude_id):

	program = data.grabStudentProgram(connDB, stude_id)		#tuple

	year = data.grabStudentYear(connDB,stude_id)

	plan = data.grabStudentPlan(connDB,stude_id)	

	formulaFee = data.grabFormulaFee(connDB, program)

	coursesRaw = data.grabStudentCourses(connDB, stude_id)

	normalUnits = data.grabNormalUnits(connDB, program)


	if year == 1 and "BA" in program: 		#accounts for first year students, since
		program = [("1st Year Arts"),]
	elif year == 1 and "BSC" in program:
		program = [("1st Year Science"),]

	programWeight = data.grabProgramWeight(connDB, program)


	BIU = data.grabBIU(connDB)

	for i in reversed(range(len(coursesRaw))):
		if coursesRaw[i] == None:
			courses = coursesRaw[:i]		#removes the None courses 

	creditsList = []
	for course_id in courses:
		creditsList.append(data.grabCourseCredits(connDB, course_id))			#tuple

	creditSum = 0.0
	for credit in creditsList:		#sum up all the credits that the student was enrolled 
		temp = credit[0]
		creditSum = creditSum + temp	#used to unpack the tuple


	if BIU == 0 or programWeight == 0:	#prevents totalBIU from being negative
		totalBIU = 0
	else:
		totalBIU = (BIU * programWeight) - formulaFee		

	proportion = creditSum / normalUnits

	grantGenerated = proportion * totalBIU

	return grantGenerated

def courseGrant(connDB,course_id):
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
	
	studentsList = connDB.fetchall()		#list of all students

	courseGrantTotal = 0  		#cumulative total of the grants award to the course

	for student in studentsList:		#iterates through all the students

		stude_id = student[0]

		program = data.grabStudentProgram(connDB, stude_id)

		year = data.grabStudentYear(connDB, stude_id)

		formulaFee = data.grabFormulaFee(connDB, program)

		normalUnits = data.grabNormalUnits(connDB,program)

		if year == 1 and "BA" in program: 		#accounts for first year students, since
			program = [("1st Year Arts"),]
		elif year == 1 and "BSC" in program:
			program = [("1st Year Science"),]

		programWeight = data.grabProgramWeight (connDB, program)

		BIU = data.grabBIU(connDB)

		if BIU == 0 or programWeight == 0:		#prevents total BIU to go below zero
			totalBIU = 0
		else:
			totalBIU = (BIU * programWeight) - formulaFee

		courseCredits = data.grabCourseCredits(connDB, course_id)	


		proportion = courseCredits / normalUnits
		grantGenerated = proportion * totalBIU

		courseGrantTotal = courseGrantTotal + grantGenerated


	return courseGrantTotal
	


def runApp():
	conn = data.connectDB()
	c = conn.cursor()
	c.execute("SELECT COUNT (*) FROM students")

	val = c.fetchone()
	numOfStudents = int(val[0])


	grantGeneratedTotal = 0
	for i in range(numOfStudents):
		grantGeneratedTotal = grantGeneratedTotal + studentGrant(c, i + 1)

	#print grantGeneratedTotal
	return grantGeneratedTotal

def runAppCourse(course):
	conn = data.connectDB()
	c = conn.cursor()
	#print courseGrant(c, course)
	return courseGrant(c, course)

if __name__ == '__main__':

	total1 = 0
	total1 = total1 + runAppCourse(1)
	total1 = total1 + runAppCourse(2)
	total1 = total1 + runAppCourse(3)

	total2 = runApp()

	print total2

	print total1

