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
		
		self.Start()

	def MainLoop(self):

		pass

	def Start(self):
		while self.menu != "QUIT APPLICATION":

			self.menu = UI.mainMenu.runApp()

			print self.menu  	#@@@@@@@@@@@@@@@@@@@@@@@@@@@ TAKE OUT LATER

			if self.menu == "View Data":

				self.OutputExcel()

			elif self.menu == "Update Data":

				self.dataLocation = False

				while self.dataLocation is False:

					self.SetDataLocation()		#keeps on asking for the data location 

				if self.dataLocation != False :	#as long as the dataLocation is valid, the database will be updated

					self.UpdateData(self.dataLocation)

			elif self.menu == "Update Constants":

				self.UpdateConstants()

			#self.UpdateData()

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

	def OutputExcel(self):
		writeToExcel.runApp()
		self.output = True

	def UpdateData(self,dataLocation):
		preprocess.main(dataLocation)

	def UpdateConstants(self):
		updateConstants.runApp()
		self.constants = True


def main():
	program = Instance()

#pass in the datalocation + option chosen into the preprocess function
		
if __name__ == '__main__':
	main()


#make sure all excel files are closed
	