#-------------------------------------------------------------------------------
# Name:        updates the database by adding the credits (asked through the UI entry widget)
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

import extractData
import sqlite3
import sys
import os

sys.path.append(os.getcwd() + '/testing/UI')    #adding the UI modules to the path

import creditsInput

def main():
	conn = extractData.connectDB()
	c = conn.cursor()

	c.execute("SELECT course_code FROM courses;")	#grabs names of all the courses
	allCourses = c.fetchall()
	creditsList = creditsInput.runApp(allCourses) 	#initializes the entry widget to input credits data
	
	for credit in creditsList:
		c.execute("UPDATE courses SET credits = ?;",(credit,))		#adds to each course record the number of credits

	extractData.closeDB(conn) 

if __name__ == '__main__':
	main()



