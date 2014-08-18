#-------------------------------------------------------------------------------
# Name:       	Update Constants
# Purpose:      access the database and pull the constants data
#				
#
# Author:      DBMS
#
# Created:     01/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import extractData as data
import UI
import dateTimeOutput
import sqlite3

def checkError(funcOutput):     #returns false is there is an error, returns true if no error exists
    '''Checks the output of the function to see if an error message was returned
    '''

    if 'Error' in funcOutput:       #sees if the output returns an error
        return False
    else:                       #output does not return an error
        return True

def checkBack(funcOutput):
	'''Checks if the BACK button was selected
	'''

	if 'BACK' in funcOutput:		#Checks if the output shows "QUIT"
		return True 				#this will mean 
	else:
		return False


def inputCredits(c, inputStage):
    '''Implements the creditsInputScrolling tk app and will update the database
    '''
        
    c.execute("SELECT course_code, term FROM courses;") #grabs names of all the courses
    allCourses = c.fetchall()

    courseDisplayName = []

    for i in range(len(allCourses)):
        #first element [i][0] is the course code, the second [i][1] is the term that the course is in
        courseDisplayName.append(allCourses[i][0] + " - Term: " + str(allCourses[i][1]))  
    
    creditsList = UI.creditsInputScrolling.runApp(courseDisplayName)    #initializes the entry widget to input credits data
    while not checkError(creditsList):                  #do while loop that repeats until there is no more error
        UI.errorMessageBox.runApp(creditsList)
        creditsList = UI.creditsInputScrolling.runApp(courseDisplayName)
    
    if checkBack(creditsList):
    	return inputStage - 1

    for credit in creditsList:
        c.execute('''UPDATE courses SET credits = ?;''',(credit,))      #adds to each course record the number of credits

    return inputStage + 1

def inputUnitFees(c, inputStage):
	''' Uses the feeUnitsInput tk app and will update the database
	'''
	c.execute("SELECT DISTINCT program FROM students;")
	programList = c.fetchall()

	unitFeesList = UI.feeUnitsInput.runApp(programList)
	while not checkError(unitFeesList) and not len(programList) == len(unitFeesList):
		UI.errorMessageBox.runApp(unitFeesList)
		unitFeesList = UI.feeUnitsInput.runApp(programList)

	if checkBack(unitFeesList):
		return inputStage - 1

	if len(programList) == len(unitFeesList):
		for i in range(len(unitFeesList)):

			c.execute("UPDATE program_info SET unit_fees = ? WHERE program_name = ?;",(unitFeesList[i], programList[i][0],))
	return inputStage + 1

def inputBIU(c, inputStage):
	''' Uses the BIUInput tk app and will update the database
	'''

	BIUList = UI.BIUInput.runApp()
	while not checkError(BIUList) and not len(BIUList) == 1:
		UI.errorMessageBox.runApp(BIUList)
		BIUList = UI.BIUInput.runApp()
		
	if checkBack(BIUList):
		return inputStage - 1

	if len(BIUList) == 1:

		c.execute("SELECT COUNT (*) FROM constants WHERE id = 1")
		checkExists = c.fetchone()

		if checkExists == (1,):		#if a BIU value exists in the database

			c.execute("UPDATE constants SET value = ? WHERE id = 1;", (BIUList))	#update that existing value

		elif checkExists == (0,):	#if no BIU value exists

			c.execute("INSERT INTO constants (name,value) VALUES (?,?);",("BIU Value", BIUList[0]))		#insert a new record

	return inputStage + 1

def inputFormulaFees(c, inputStage):
	''' Uses the formulaFeesInput tk app and will update the database
	'''

	c.execute("SELECT DISTINCT program FROM students;")
	programList = c.fetchall()

	formulaFeeList = UI.formulaFeesInput.runApp(programList)
	while not checkError(formulaFeeList) and not len(programList) == len(formulaFeeList):
		UI.errorMessageBox.runApp(formulaFeeList)
		formulaFeeList = UI.formulaFeesInput.runApp(programList)

	if checkBack(formulaFeeList):
		return inputStage - 1 

	if len(programList) == len(formulaFeeList):
		for i in range(len(formulaFeeList)):

			c.execute("UPDATE program_info SET formula_fees = ? WHERE program_name = ?;",(formulaFeeList[i],programList[i][0]))

	return inputStage + 1

def inputNormalUnits(c, inputStage):
	c.execute("SELECT DISTINCT program FROM students;")
	programList = c.fetchall()

	normalUnitsList = UI.normalUnitsInput.runApp(programList)
	while not checkError(normalUnitsList) and not len(programList) == len(normalUnitsList):
		UI.errorMessageBox.runApp(normalUnitsList)
		normalUnitsList = UI.normalUnitsInput.runApp(programList)

	if checkBack(normalUnitsList):
		return inputStage - 1 

	if len(programList) == len(normalUnitsList):
		for i in range(len(normalUnitsList)):
			c.execute("UPDATE program_info SET normal_units = ? WHERE program_name = ?;", (normalUnitsList[i],programList[i][0],))

	return inputStage + 1

def inputProgWeights(c, inputStage):
	c.execute("SELECT DISTINCT program FROM students;")
	programList = c.fetchall()

	programList.append("1st Year Arts")
	programList.append("1st Year Science")

	progWeightsList = UI.programWeightsInput.runApp(programList)
	
	while not checkError(progWeightsList) and not len(programList) == len(progWeightsList):
		UI.errorMessageBox.runApp(progWeightsList)
		progWeightsList = UI.programWeightsInput.runApp(programList)

	if checkBack(progWeightsList):
		return inputStage - 1 

	if len(programList) == len(progWeightsList):
		for i in range(len(progWeightsList[:-2])):		#SQL updates for all programs "BSCH", "BAH" but NOT 1st year arts and science

			c.execute("UPDATE program_info SET program_weight = ? WHERE program_name = ?;",(progWeightsList[i],programList[i][0]))
			
		for i in range(len(progWeightsList)-2,len(progWeightsList)):

			c.execute("SELECT COUNT (*) FROM program_info WHERE program_name = ?", (programList[i],))
			checkExists = c.fetchone()

			if checkExists == (0,):		#happens when 1st year Arts and Science records DO NOT exist
				
				c.execute("INSERT INTO program_info(program_name, program_weight) VALUES (?,?);",(programList[i],progWeightsList[i]))
			
			elif checkExists == (1,):	#happens when 1st year Arts and Science records DO exist
				
				c.execute("UPDATE program_info SET program_weight = ? WHERE program_name = ?;", (progWeightsList[i],programList[i]))

	return inputStage + 1


def runApp():
	''' Runs all the functions in a loop
		If the submit button is pressed for each app, the next app will shows
		If the back button is pressed, the previous app will show up (data will be reentered entirely)
	'''
	conn = data.connectDB()

	c = conn.cursor()

	numOfFrames = 3

	inputStage = 2 		#initialize
	
	while inputStage != numOfFrames:

		if inputStage == 0:

			inputStage = inputCredits(c,inputStage)

		elif inputStage == 1:

			inputStage = inputUnitFees(c,inputStage)

		elif inputStage == 2:

			inputStage = inputBIU(c,inputStage)

		elif inputStage == 3:

			inputStage = inputFormulaFees(c,inputStage)

		elif inputStage == 4:

			inputStage = inputNormalUnits(c,inputStage)

		elif inputStage == 5:

			inputStage = inputProgWeights(c,inputStage)

		elif inputStage == -1:	#when it is equal to -1 (go back on inputCredits)

			inputStage = 0  #makes them input credits again

		else:
			break 		

	# c.execute('''UPDATE timeRecord
	# 				SET timeStam = ?
	# 				WHERE time_id = 2;''',(dateTimeOutput.pythonTime(),))
	try:
		c.execute('''INSERT INTO timeRecord(time_id,timeStam) 
					VALUES (2,?);''',(dateTimeOutput.pythonTime(),))
	except sqlite3.IntegrityError:
		c.execute('''UPDATE timeRecord
				SET timeStam = ?
				WHERE time_id = 2;''',(dateTimeOutput.pythonTime(),))
	conn.commit()

	conn.close()

if __name__ == '__main__':
	runApp()
	