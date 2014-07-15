#-------------------------------------------------------------------------------
# Name:        extract Data
# Purpose:		uses the user interface to interact with the database to pull relevant and requested data
#
#
#
# Author:      DBMS
#
# Created:     21/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sqlite3
import sys

sys.path.append(os.getcwd() + '/testing/UI')    #adding the UI modules to the path

import radioBoxInput

def connectDB():		#connects to the database and returns the connection object, still requires the cursor
	cdLocation = os.getcwd()
	dbLocation = cdLocation + "/testv2.db"

	conn = sqlite3.connect(dbLocation)
	return conn

def closeDB(conn):		#closes the connection object and saves the database
	conn.commit()
	conn.close

def grabStudentProgram(connDB,stude_id):		#
	connDB.execute("SELECT program FROM students WHERE stud_id = ?;",(stude_id,))
	data = connDB.fetchone()
	return data

def grabStudentCourses(connDB,stude_id):
	connDB.execute("SELECT course1, course2, course3, course4, course5, course6, course7, course8, course9, course10 FROM students WHERE stud_id = ?;",(stude_id,))
	data = connDB.fetchone()	#grabs the data in a list, which each thing being an element
	return data

def grabCourseCredits(connDB,course_code):
	connDB.execute("SELECT credits FROM courses WHERE course_code = ?;",(course_code,))
	data = connDB.fetchone()
	return data

def main():
	conn = connectDB()
	c = conn.cursor()


	data = grabStudentCourses(c,1)
	print data
	radioBoxInput.runAppStr(data)

if __name__ == '__main__':
	main()








