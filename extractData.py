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

sys.path.append(os.getcwd() + '/UI')    #adding the UI modules to the path


#meta data RELATED FUNCTIONS

def connectDB():		#connects to the database and returns the connection object, still requires the cursor
	cdLocation = os.getcwd()
	dbLocation = cdLocation + "/testv2.db"

	conn = sqlite3.connect(dbLocation)
	return conn

def closeDB(conn):		#closes the connection object and saves the database
	conn.commit()
	conn.close

#STDUENT SPECIFIC

def grabStudentProgram(connDB,stude_id):		#
	connDB.execute("SELECT program FROM students WHERE stud_id = ?;",(stude_id,))
	data = connDB.fetchone()
	
	return data

def grabStudentPlan(connDB,stude_id):
	connDB.execute("SELECT plan, plan2, plan3 FROM students WHERE stud_id = ?;", (stude_id,))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabStudentYear(connDB, stude_id):
	connDB.execute("SELECT proj_level FROM students WHERE stud_id = ?;", (stude_id,))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabStudentCourses(connDB,stude_id):
	connDB.execute("SELECT course1, course2, course3, course4, course5, course6, course7, course8, course9, course10 FROM students WHERE stud_id = ?;",(stude_id,))
	data = connDB.fetchone()	#grabs the data in a list, with each thing being an element
	return data

#COURSE SPECIFIC

def grabCourseName(connDB,course_id):
	connDB.execute("SELECT course_code FROM courses WHERE course_id = ?;",(course_id,))
	data = connDB.fetchone()
	return data

def grabCourseCredits(connDB,course_id):
	connDB.execute("SELECT credits FROM courses WHERE course_id = ?;",(course_id,))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabCourseTerm(connDB,course_id):
	connDB.execute("SELECT term FROM courses WHERE course_id = ?;",(course_id,))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabEnrollmentNumber(connDB,course_id):
	connDB.execute('''SELECT COUNT(*)		
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

	data = connDB.fetchone()
	data = data[0]
	return data

#FOR CALCULATING GRANTS

def grabUnitFees(connDB,program_name):		#take the student's program name (str) and returns the appropriate unit fee
	connDB.execute("SELECT unit_fees FROM program_info WHERE program_name = ?;", program_name)
	data = connDB.fetchone()
	data = data[0]
	return data


def grabProgramWeight(connDB, program_name):	#pass in a string like ['program']

	connDB.execute("SELECT program_weight FROM program_info WHERE program_name = ?;", program_name)
	data = connDB.fetchone()
	data = data[0]
	return data

def grabFormulaFee(connDB,program_name):

	connDB.execute("SELECT formula_fees FROM program_info WHERE program_name = ?;", program_name)
	data = connDB.fetchone()
	data = data[0]
	return data

def grabBIU(connDB):
	connDB.execute("SELECT value FROM constants WHERE name = 'BIU Value';")
	data = connDB.fetchone()
	data = data[0]
	return data

def grabNormalUnits(connDB, program_name):
	connDB.execute("SELECT normal_units FROM program_info WHERE program_name = ?", program_name)
	data = connDB.fetchone()
	data = data[0]
	return data

#GRAB DYNAMICALLY

def grabStudentEnrollment(connDB, program_name,course_id):
	connDB.execute('''SELECT COUNT(*)		
						FROM students 
						WHERE program = ? and
							(course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?);''',(program_name,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabStudentYearCourse(connDB, program_name, year, course_id):
	connDB.execute('''SELECT COUNT (*)
						FROM students
						WHERE program = ? and
							year = ? and 
							(course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?);''',(program_name,year,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
	data = connDB.fetchone()
	data = data[0]
	return data

#SHOW TYPES OF OUTPUT
def main():
	conn = connectDB()
	c = conn.cursor()



	program = grabStudentProgram(c, 1)
	print "PROGRAM"
	print program 
	print type(program)
	print "\n"

	plan = grabStudentPlan(c, 1)
	print "PLAN"
	print plan
	print type(plan)
	print "\n"

	year= grabStudentYear(c, 1)
	print "YEAR"
	print year
	print type(year)
	print "\n"

	courses = grabStudentCourses(c,1)
	print "COURSES"
	print courses
	print type(courses)
	print "\n"

	credits = grabCourseCredits(c, 1)
	print "CREDITS"
	print credits
	print type(credits)
	print "\n"

	term = grabCourseTerm(c, 1)
	print "TERM"
	print term
	print type(term)
	print "\n"

	unitFee = grabUnitFees(c, program)
	print "UNIT FEES"
	print unitFee
	print type(unitFee)
	print "\n"

	progWeight = grabProgramWeight (c, program)
	print "PROGRAM WEIGHT"
	print progWeight
	print type(progWeight)
	print "\n"

	formulaFee = grabFormulaFee(c,program)
	print "FORMULA FEE"
	print formulaFee
	print type(formulaFee)
	print "\n"

	BIU = grabBIU(c)
	print "BIU"
	print BIU
	print type(BIU)
	print "\n"

	normalUnits = grabNormalUnits(c, program)
	print "Normal Units"
	print normalUnits
	print type(BIU)
	print "\n"

if __name__ == '__main__':
	main()
