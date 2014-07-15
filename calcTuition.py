#-------------------------------------------------------------------------------
# Name:        calculates the money from tuition proportional to number of courses taken 
#               
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

sys.path.append(os.getcwd() + '/testing/UI')    #adding the UI modules to the path

import creditsInput

def studentTuition(connDB, stude_id):			#pass in the student and calculate tuition of the student

	program = extractData.grabStudentProgram(connDB, stude_id)		
	coursesRaw = extractData.grabStudentCourses(connDB, stude_id)

	for i in reversed(range(len(coursesRaw))):
		if coursesRaw[i] == None:			#eliminates the none courses
			courses = coursesRaw[:i]	

	return len(courses)


def main():
	conn = extractData.connectDB()
	c = conn.cursor()
	c.execute("SELECT COUNT (*) FROM students")

	val = c.fetchone()
	numOfStudents = int(val[0])

	numOfStudents = 10
	for i in range(numOfStudents):
		print studentTuition(c, i+1)

	#for i in range(numOfStudents)

if __name__ == '__main__':
    main()