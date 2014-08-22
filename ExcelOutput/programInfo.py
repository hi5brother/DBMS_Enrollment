#-------------------------------------------------------------------------------
# Name:        program Information

# Purpose:		writes all the program info onto the sheet
#				includes program name, enrollment numbers, unit fees formula fees, BIU, etc
#
# Author:      DBMS
#
# Created:     31/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
from formatting import columnWidth, freezePanes

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data


def write(c, book):
	sheet = book.add_sheet("Program Info")

	twoDecimalStyle = xlwt.XFStyle()		#styling for using two decimals
	twoDecimalStyle.num_format_str = '0.00'

	columnWidth(sheet,14)
	c.execute("SELECT DISTINCT program_id FROM program_info;")
	programList = c.fetchall()

	programNameStr = 'Program Name'
	enrollmentNameStr = 'Enrollment'
	unitFeeNameStr = 'Unit Fees'
	formulaFeeNameStr = 'Formula Fees'
	progWeightNameStr = 'Program Weight'
	normUnitsNameStr = 'Normal Units'
	BIUNameStr = 'BIU Value'

	columns = {programNameStr : 0,
				enrollmentNameStr : 1,
				unitFeeNameStr : 2,
				formulaFeeNameStr : 3,
				progWeightNameStr : 4,
				normUnitsNameStr : 5,
				BIUNameStr : 6,
				}

	for columnName in columns:
		sheet.write(0,columns[columnName],columnName)

	count = 1
	for program in programList:
	
		program = program[0]

		programName = data.grabProgName(c,program)
		sheet.write(count,columns[programNameStr], programName)

		programName = [programName]	#make into tuple 

		enrollment = data.grabProgEnrollment(c,programName)
		sheet.write(count, columns[enrollmentNameStr],enrollment)

		unitFee = data.grabUnitFees(c,programName)
		sheet.write(count, columns[unitFeeNameStr], unitFee, twoDecimalStyle)

		formulaFee = data.grabFormulaFee(c,programName)
		sheet.write(count,columns[formulaFeeNameStr], formulaFee, twoDecimalStyle)

		progWeight = data.grabProgramWeight(c, programName)
		sheet.write(count, columns[progWeightNameStr], progWeight, twoDecimalStyle)

		normUnits = data.grabNormalUnits(c,programName)
		sheet.write(count, columns[normUnitsNameStr], normUnits)

		count = count + 1

	BIUVal = data.grabBIU(c)
	sheet.write(1,columns[BIUNameStr],BIUVal)


	freezePanes(sheet,1)

	return True