#-------------------------------------------------------------------------------
# Name:        calculates the money from tuition proportional to number of courses taken 
#               income per student = DBMS credits taken x unit fee (varies by program)
#
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

sys.path.append(os.getcwd() + '/UI')    #adding the UI modules to the path

import creditsInput

def studentTuition(connDB, stude_id):			#pass in the student and calculate tuition of the student

	program = extractData.grabStudentProgram(connDB, stude_id)	

	coursesRaw = extractData.grabStudentCourses(connDB, stude_id)

	unitFee = extractData.grabUnitFees(connDB,program)
	unitFee = unitFee[0]	#make from tuple into float

	for i in reversed(range(len(coursesRaw))):
		if coursesRaw[i] == None:			#eliminates the none courses
			courses = coursesRaw[:i]	
	
	creditsList = []
	for course_id in courses:		#finds the credits of each course that the student took
		creditsList.append(extractData.grabCourseCredits(connDB, course_id))
	
	creditSum = 0
	for credit in creditsList:		#sum up all the credits that the student was enrolled in
		creditSum = creditSum + (credit[0])

	revenueGenerated = creditSum * unitFee		#formula to calculate revenue from each student

	return revenueGenerated

def runApp():
	conn = extractData.connectDB()
	c = conn.cursor()
	c.execute("SELECT COUNT (*) FROM students")		#find how many students are in the data base

	val = c.fetchone()
	numOfStudents = int(val[0])

	revenueGeneratedTotal = 0
	for i in range(numOfStudents):		#loops through all the students and calculates money from each student
		print studentTuition(c, i+1)
		revenueGeneratedTotal = revenueGeneratedTotal + studentTuition(c, i + 1)

	print numOfStudents
	print revenueGeneratedTotal

if __name__ == '__main__':
	runApp()