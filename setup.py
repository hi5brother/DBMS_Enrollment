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
from cx_Freeze import setup, Executable

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
					"include_files" : ["excelMacro\intToFloat.xlsm"]}

#pywin is the same as win32api

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(	name = "DBMS_Enrollment",
		version = "0.4",
		description = "cx_freeze application",
		options = {"build_exe": build_exe_options},
		executables = [Executable("main.py", base=base)])

'''

To execute and build on CMD,use

python setup.py bdist_msi 

'''