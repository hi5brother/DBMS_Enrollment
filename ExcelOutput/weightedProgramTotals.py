#-------------------------------------------------------------------------------
# Name:        weighted program breakdown

# Purpose:		will output enrollments in each plan and year
#				will take the plan e.g. "BCHM" or "MECH" and find all the major/minor/spec with that
#				
#							BCHM M 	BCHM S 		BCHM G...
#				course... Year 1... Year 2... Year 3... Year 4...
#
# Author:      DBMS
#
# Created:     06/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt

from formatting import columnWidth, freezePanes

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import extractData as data

def write(c,book):

	sheet = book.add_sheet("WeightedProgramTotals")

	freezePanes(sheet, 1)

	columnWidth(sheet, 10)

	c.execute("SELECT DISTINCT course_id FROM courses;")
	courseList = c.fetchall()

	planList = data.grabFullPlanList(c)

	for plan in planList:
		

