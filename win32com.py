#-------------------------------------------------------------------------------
# Name:        win32com TEST
# Purpose:      test out the excel macro found in intToFloat.xlsm
#				test out win32com.client module
#
#
# Author:      DBMS
#
# Created:     21/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import win32com.client

def main():

	#hard coded directory paths
	dataLocation = "C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\QU_RG_CLASS_LIST_GRADE_476707713 (4).xls"
	macroLocation = "C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\excelMacro\\intToFloat.xlsm"
	

	xl = win32com.client.Dispatch("Excel.Application")
	xl.Visible = 1

	wbPre = xl.Workbooks.Open(macroLocation)		#open the macro workbook

	wbPre.Application.Run("makeTexttoFloat", 7, dataLocation)		#run the macro

	#the macro take in the column that is converted from text to float
	#also opens the target workbook itself

	xl.Application.Quit()
	del (xl)

if __name__ == '__main__':
	print main()