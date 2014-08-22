#-------------------------------------------------------------------------------
# Name:        
#
#			setup with cxFreeze 
#			
# Purpose:
#
# Author:      DBMS
#
# Created:     11/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sys
import os
from cx_Freeze import setup, Executable

path = os.getcwd()

build_exe_options = {"packages" : [	"UI",
									"ExcelOutput",
									"xlwt",
									"xlrd",
									"win32com",
									"Tkinter",
									"sqlite3",
									"calcGrant",
									"calcTuition",
									"dateTimeOutput",
									"dbFormat",
									"excelPreprocess",
									"extractData",
									"preprocess",
									"studentProcessing",
									"updateConstants",
									"writeToExcel",
									"xlutils",
									"pywin"],
					"include_files" : ["excelMacro\intToFloat.xlsm",
										"icon_table.ico",
										"README.md"]}

#pywin is the same as win32api

base = None
if sys.platform == "win32":		#used to remove the console window
    base = "Win32GUI"

setup(	name = "DBMS_Enrollment Calculator",
		version = "0.61",
		description = "DBMS Enrollment Calculator",
		options = {"build_exe": build_exe_options},
		executables = [Executable("dbmsEnrollCalc.py", icon = "icon_table.ico", base=base)])


'''

To execute and build on CMD,use

python setup.py bdist_msi 


'''