#-------------------------------------------------------------------------------
# Name:        main, imports all the modules and runs them
# Purpose:      shows the main menu
#				asks for what the user wants
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

class Instance:
	def __init__(self):

		self.menu = True
		self.output = False
		self.constants = False
		self.dataDirectory = False
		self.dataLocation = False
		self.progStatus = {
							"MainMenu" : 0
							}
		
		self.DatabaseSetup()
		self.Instructions()
		self.Start()

	def test(self):
		self.DatabaseSetup()
		self.Instructions()

	def Start(self):	
		''' Main loop of program. The menu tk app returns strings based on the button pressed.
		'''

		while self.menu != "QUIT APPLICATION":

			self.menu = UI.mainMenu.runApp()


			if self.menu == "View Data":

				self.OutputExcel()

			elif self.menu == "Import Data":

				self.dataLocation = False

				while self.dataLocation is False:

					self.SetDataLocation()		#keeps on asking for the data location 

				if self.dataLocation != False :	#as long as the dataLocation is valid, the database will be updated

					self.UpdateData(self.dataLocation)

			elif self.menu == "Update Constants":

				self.UpdateConstants()

		sys.exit()	

	def SetDataLocation(self):
		'''See if the directory with spreadsheets exists
			Then check the contents of the sheets. If they cannot be processed (does not have appropriate headings),
			TypeError is returned and the dataLocation is False
		'''
		self.dataLocation = UI.askDataDirectory.runApp()
		self.excelExtension = "xls"
		self.dirExist = preprocess.checkDirectory(self.dataLocation, self.excelExtension)

		if self.dataLocation == "QUIT":
			pass

		elif self.dirExist:

			self.filesList = excelPreprocess.findFiles(self.dataLocation, self.excelExtension)
			self.sheetAddressList = excelPreprocess.findSheetAddresses(self.dataLocation)

			try:
				self.courseCodes = excelPreprocess.checkCourseCode(self.filesList, self.sheetAddressList)
				UI.gridBox.runApp(self.courseCodes)

			except TypeError:
				UI.errorMessageBox.runApp("The spreadsheets in the directory are not valid.")
				self.dataLocation = False
		else:
			self.dataLocation = False
			UI.errorMessageBox.runApp("The directory does not exist.")

	def Instructions(self):
		instructionList = []
		self.noStudData = False
		try:
			self.timeStam = data.grabTimeStamp(self.c,"Student Data")
		except TypeError:			#if there is no time stamp value, it means no data has been imported
			self.noStudData = True	
		except sqlite3.OperationalError: 	#if there is no db available
			self.noStudData = True

		if self.noStudData:				#IF THERE IS NO STUDENT DATA
			instructionList.append("No student/course data has been imported.\n    Please 'Import Data' first.")

		elif not self.noStudData:		#IF THERE IS STUDENT DATA
			instructionList.append("Student/course data was imported at " + str(self.timeStam) + "\n    You do not need to import data.")

		self.noBIUData = False
		try:
			self.timeStam = data.grabTimeStamp(self.c,"BIU Data")
		except TypeError:
			self.noBIUData = True
		except sqlite3.OperationalError:
			self.noBIUData = True

		if self.noBIUData: 			#IF THERE IS NO BIU DATA
			instructionList.append("No program or BIU data has been imported. \n    Please 'Update Constants'")

		elif not self.noBIUData: 	#IF THERE IS BIU DATA
			instructionList.append("Program and BIU data was imported at " + str(self.timeStam) + "\n    You do not need to update constants.")

		instructionList.append("Please select 'View Data' to access the data. \n    A spreadsheet will be output with the requested data.")

		UI.instructionsBox.runApp(instructionList)


	def DatabaseSetup(self):
		self.conn = data.connectDB()
		self.c = self.conn.cursor()

	def OutputExcel(self):
		writeToExcel.runApp()

	def UpdateData(self,dataLocation):
		preprocess.main(dataLocation)

	def UpdateConstants(self):
		updateConstants.runApp()

def main():
	
	program = Instance() 

	del program 	#kill the object

		
if __name__ == '__main__':
	main()


#make sure all excel files are closed
	