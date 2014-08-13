#-------------------------------------------------------------------------------
# Name:        
#
#			tests using Tk to go through directory
#			tkFileDialog: http://tkinter.unpythonic.net/wiki/tkFileDialog
#			
# Purpose:
#
# Author:      DBMS
#
# Created:     22/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import Tk
from tkFileDialog import asksaveasfilename

def main():
	Tk().withdraw()

	filename = asksaveasfilename(defaultextension='.xls',initialfile = 'DBMS Enrollment Data')	
	#default extension will be .xls


	if filename == '':
		print "User Error: File was not saved."
	else:
		print (filename)

def runApp():
	main()

if __name__ == '__main__':
	runApp()