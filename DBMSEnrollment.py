#-------------------------------------------------------------------------------
# Name:        main, imports all the modules and runs them
# Purpose:      shows the main menu
#				
#
# Author:      DBMS
#
# Created:     05/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys

import preprocess
import writeToExcel

import updateConstants

import excelPreprocess

import UI

import extractData as data

import sqlite3

import dateTimeOutput

class Instance:
	def __init__(self):

		self.menu = True
		self.output = False
		self.constants = False
		self.dataDirectory = False
		self.dataLocation = False
		
		self.MainLoop()

	def MainLoop(self):	
		''' Main loop of program. The menu tk app returns strings based on the button pressed.
		'''
		self.DatabaseSetup()
		
		while self.menu != "QUIT APPLICATION":

			self.DatabaseSetup()
			self.Instructions()		

			self.menu = UI.mainMenu.runApp(self.instructionList)

			if self.menu == "Import Student and Course Data":

				self.dataLocation = False

				while self.dataLocation is False:	

					self.SetDataLocation()		#keeps on asking for the data location 

				if self.dataLocation != False :	#as long as the dataLocation is valid, the database will be updated

					self.UpdateData(self.dataLocation)
					UI.messageOutputBox.runApp(["Student and course data have been succesfully imported."])

			elif self.menu == "Update Program Data":

				self.UpdateConstants()
				UI.messageOutputBox.runApp(["Program and BIU data have been successfully imported."])

			elif self.menu == "View Data":

				self.OutputExcel()
				UI.messageOutputBox.runApp(["Sheet was saved successfully."])

			elif self.menu == "DELETE DATABASE":
				'''	This option is shown under the menu bar
				'''
				self.DeleteDatabase()

		sys.exit()	

	def SetDataLocation(self):
		'''See if the directory with spreadsheets exists
			Then check the contents of the sheets. If they cannot be processed (does not have appropriate headings),
			TypeError is returned and the dataLocation is False
		'''
		userApproved = False
		while not userApproved: 
			self.dataLocation = UI.askDataDirectory.runApp()		#asks user for the data location
			self.excelExtension = "xls"
			self.dirExist = preprocess.checkDirectory(self.dataLocation, self.excelExtension)		#checks if the data is valid (True or False)
		
			if self.dirExist:

				self.filesList = excelPreprocess.findFiles(self.dataLocation, self.excelExtension)
				self.sheetAddressList = excelPreprocess.findSheetAddresses(self.dataLocation)

				try:
					self.courseCodes = excelPreprocess.checkCourseCode(self.filesList, self.sheetAddressList)
					userApproved = UI.gridBox.runApp(self.courseCodes) 	#user can submit (userApproved = True) or go back (userApproved = False)

				except TypeError:
					UI.errorMessageBox.runApp("The spreadsheets in the directory are not valid.")
					self.dataLocation = False
			else:
				self.dataLocation = False
				UI.errorMessageBox.runApp("The directory does not have spreadsheets.")

	def Instructions(self):
		''' This method generates the instructions used to direct the user. 
			Checks the database for timestamp records to see if data exists.
			If all the data is present, it will ask the user to just 'View Data'
		'''
		self.instructionList = []

		''' Checks for a time stamp on the students and courses tables (imported from Excel)
		'''
		self.noStudData = False
		try:
			self.timeStam = data.grabTimeStamp(self.c,"Student Data")
		except TypeError:			#if there is no time stamp value, it means no data has been imported
			self.noStudData = True	
		except sqlite3.OperationalError: 	#if there is no db available
			self.noStudData = True

		if self.noStudData:				#IF THERE IS NO STUDENT DATA
			self.instructionList.append("No student or course data has been imported.\n    Please 'Import Data' first.")

		elif not self.noStudData:		#IF THERE IS STUDENT DATA
			self.instructionList.append("Student and course data was imported at " + str(self.timeStam) + "\n    You do not need to import student and course data.")

		''' Checks for a time stamp on the program data tables 	(inputted by user)
		'''
		self.noBIUData = False
		try:
			self.timeStam = data.grabTimeStamp(self.c,"BIU Data")
		except TypeError:
			self.noBIUData = True
		except sqlite3.OperationalError:
			self.noBIUData = True

		if self.noBIUData: 			#IF THERE IS NO BIU DATA
			self.instructionList.append("No program or BIU data has been imported. \n    Please 'Update Constants'")

		elif not self.noBIUData: 	#IF THERE IS BIU DATA
			self.instructionList.append("Program and BIU data was imported at " + str(self.timeStam) + "\n    You do not need to update program data, unless the student \n     and course data was updated after the program data.")

		self.instructionList.append("Please select 'View Data' to access the data. A spreadsheet will be\n    output with the requested data.")

	def DatabaseSetup(self):
		'''	Used every loop in the main menu loop
		'''
		self.conn = data.connectDB()
		self.c = self.conn.cursor()

	def OutputExcel(self):
		writeToExcel.runApp()

	def UpdateData(self,dataLocation):
		preprocess.main(dataLocation)

	def UpdateConstants(self):
		updateConstants.runApp()

	def DeleteDatabase(self):
		''' Needs to close the DB. Then it will delete the DB
		'''
		self.conn.close()
		cdLocation = os.getcwd()
		dbName = "\\enrolldata.db"
		dbLocation = cdLocation + dbName

		try:
			os.remove(dbLocation)
		except WindowsError:        #WindowsError appreas when there is no database file
			pass

def main():
	
	program = Instance() 

	del program 	#kill the object

		
if __name__ == '__main__':
	main()


#make sure all excel files are closed
	