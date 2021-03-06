#-------------------------------------------------------------------------------
# Name:        extract Data
# Purpose:		functions that will extract the data in either a single tuple, or a list
#				can output values/lists such as:
#					- time stamp )from timeRecord
#					- list of distinct programs, courses, student plans, student years
#					- specific unit fees, based on program and other info to calculate grants (from program_info)
#					- grabs enrollment number in a particular course/year/program based on 
#						o program, 
#
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

#meta data RELATED FUNCTIONS

def connectDB():		#connects to the database and returns the connection object, still requires the cursor
	cdLocation = os.getcwd()
	dbLocation = cdLocation + "/enrolldata.db"

	conn = sqlite3.connect(dbLocation)
	return conn

def closeDB(conn):		#closes the connection object and saves the database
	conn.commit()
	conn.close

#Grab metadata
def grabTimeStamp(connDB,value):
	if value == "Student Data":		#time stamp for excel imported 
		timeID = 1
	elif value == "BIU Data":
		timeID = 2

	connDB.execute("SELECT timeStam FROM timeRecord WHERE time_id = ?;", str(timeID))
	data = connDB.fetchone()
	data = data[0]

	return data

class timeStam:
	def __init__(self, timeStamString):
		self.year = int(timeStamString[:4])
		self.month = int(timeStamString[6:7])
		self.day = int(timeStamString[9:10])

	def printTimeStam():
		print self.year

def compareTimeStamp(timeStamStud, timeStamBIU):
	stud = timeStam(timeStamStud)
	BIU = timeStam(timeStamBIU)

	pass

#STUDENT SPECIFIC
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

#PROGRAM SPECIFIC
def grabProgName(connDB,prog_id):
	connDB.execute("SELECT program_name FROM program_info WHERE program_id = ?;",(prog_id,))
	data = connDB.fetchone()
	data = data[0]
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

def grabFullPlanList(connDB):
	'''Grabs the full list of plans, including majors, minors, generals, 
		from the columns plan, plan2, and plan3.
		Outputs a single list with all distinct plans from all three columns
		This considers plans that are in plan2 or plan3 but NOT the plan column and will add them to the list
	'''
	connDB.execute("SELECT DISTINCT plan FROM students;")		
	planList = connDB.fetchall()
	
	connDB.execute("SELECT DISTINCT plan2 FROM students;")
	plan2List = connDB.fetchall()
	
	connDB.execute("SELECT DISTINCT plan3 FROM students;")
	plan3List = connDB.fetchall()

	for plan in plan2List:		#MERGING plan2 values with plan 

		try: 
			temp = planList.index(plan)		#check if it is in the original plan list already
		
		except ValueError:
			if plan[0] != '':			#make sure the plan isn't NULL or "" (which means there is no second plan)
		 		planList.append(plan) 		#if error arises, the plan is not in the original plan

	for plan in plan3List:		#MERGING plan3 values with plan + plan2

		try: 
			temp = planList.index(plan)	

		except ValueError:
			if plan[0] != '':
				planList.append(plan)

	return planList

# def grabDBMSEnrollNumber(connDB, course_id):
# 	'''Grabs the number of all those in a LISC or BCHM plan for a particular course.
# 	'''
# 	connDB.execute('''SELECT COUNT (*)
# 						FROM students
# 						WHERE (plan LIKE 'LISC%'
# 							OR plan2 LIKE 'LISC%'
# 							OR plan3 LIKE 'LISC%'
# 							OR plan LIKE 'BCHM%'
# 							OR plan2 LIKE 'BCHM%'
# 							OR plan3 LIKE 'BCHM%')
# 							AND (course1 = ? or 
# 							course2 = ? or
# 							course3 = ? or
# 							course4 = ? or
# 							course5 = ? or
# 							course6 = ? or
# 							course7 = ? or
# 							course8 = ? or
# 							course9 = ? or
# 							course10 = ?);''',(course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
# 	data = connDB.fetchone()
# 	data = data[0]
# 	return data

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

def grabProgEnrollment(connDB, program_name):
	connDB.execute("SELECT COUNT (*) FROM students WHERE program = ?", program_name)
	data = connDB.fetchone()
	data = data[0]
	if data == 0:		#this works for 1st year Arts and Science (it returns blank)
		data = None
	return data

#GRAB COUNTS DYNAMICALLY

def grabStudentEnrollment(connDB, program_name,course_id):		#grabs total enrollment of the course
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

def grabStudentProgYearEnroll(connDB, program_name, year, course_id):		#grabs based on program AND year
	connDB.execute('''SELECT COUNT (*)
						FROM students
						WHERE program = ? and
							proj_level = ? and 
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

def grabStudentPlanEnroll(connDB, plan, course_id):
	connDB.execute('''SELECT COUNT(*)
						FROM students
						WHERE (plan = ? or
							plan2 = ? or
							plan3 = ?) and
							(course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?);''',(plan,plan,plan,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabStudentPlanYearEnroll(connDB,plan,year,course_id):
	connDB.execute('''SELECT COUNT(*)
						FROM students
						WHERE (plan = ? or
							plan2 = ? or
							plan3 = ?) and
							proj_level = ? and
							(course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?);''',(plan,plan,plan,year,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabStudentYearEnroll(connDB, year, course_id):		#grabs count based on YEAR
	connDB.execute('''SELECT COUNT(*)
						FROM students
						WHERE proj_level = ? and
							(course1 = ? or 
							course2 = ? or
							course3 = ? or
							course4 = ? or
							course5 = ? or
							course6 = ? or
							course7 = ? or
							course8 = ? or
							course9 = ? or
							course10 = ?);''',(str(year),course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id,course_id))
	data = connDB.fetchone()
	data = data[0]
	return data

def grabProgInfo(connDB,field,course_id):
	connDB.execute('''SELECT ? 
						FROM program_info
						WHERE course_id = ?;''',field, course_id)
	data = connDB.fetchone()
	data = data[0]
	return data

#FOR SHEETS THAT DIFFERENTIATE BASED ON PROGRAM
def grabProgramYearEnroll(connDB, program, year):
	connDB.execute('''SELECT COUNT(*)
						FROM students 
						WHERE program = ? and
							proj_level = ?;
					''', (program, str(year)))
	data = connDB.fetchone()
	data = data[0]
	return data

#SHOW TYPES OF OUTPUT
def main():
	conn = connectDB()
	c = conn.cursor()

	timeStamStud = grabTimeStamp(c, "Student Data")
	timeStamBIU = grabTimeStamp(c, "BIU Data")
	print compare

	# time = grabTimeStamp(c)
	# print "TIME STAMP"
	# print time
	# print type(time)
	# print "\n"

	# program = grabStudentProgram(c, 1)
	# print "PROGRAM"
	# print program 
	# print type(program)
	# print "\n"

	# plan = grabStudentPlan(c, 1)
	# print "PLAN"
	# print plan
	# print type(plan)
	# print "\n"

	# year= grabStudentYear(c, 1)
	# print "YEAR"
	# print year
	# print type(year)
	# print "\n"

	# courses = grabStudentCourses(c,1)
	# print "COURSES"
	# print courses
	# print type(courses)
	# print "\n"

	# credits = grabCourseCredits(c, 1)
	# print "CREDITS"
	# print credits
	# print type(credits)
	# print "\n"

	# term = grabCourseTerm(c, 1)
	# print "TERM"
	# print term
	# print type(term)
	# print "\n"

	# unitFee = grabUnitFees(c, program)
	# print "UNIT FEES"
	# print unitFee
	# print type(unitFee)
	# print "\n"

	# progWeight = grabProgramWeight (c, program)
	# print "PROGRAM WEIGHT"
	# print progWeight
	# print type(progWeight)
	# print "\n"

	# formulaFee = grabFormulaFee(c,program)
	# print "FORMULA FEE"
	# print formulaFee
	# print type(formulaFee)
	# print "\n"

	# BIU = grabBIU(c)
	# print "BIU"
	# print BIU
	# print type(BIU)
	# print "\n"

	# normalUnits = grabNormalUnits(c, program)
	# print "Normal Units"
	# print normalUnits
	# print type(BIU)
	# print "\n"

if __name__ == '__main__':
	main()
