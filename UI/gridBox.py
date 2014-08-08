#-------------------------------------------------------------------------------
# Name:        gridbox output box

# Purpose:		will output a two dimensional list in the form of a grid
#
# Author:      DBMS
#
# Created:     06/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt

from Tkinter import *
data = [['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 215 - Fall 2013.xls', u'ANAT', u' 215', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 216 - Winter 2014.xls', u'ANAT', u' 216', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 315 - Fall 2013.xls', u'ANAT', u' 315', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 316 - Winter 2014.xls', u'ANAT', u' 316', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 218 - Winter 2014.xls', u'BCHM', u' 218', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 310 - Winter 2014.xls', u'BCHM', u' 310B', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 313 - Winter 2014.xls', u'BCHM', u' 313', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 315 - Fall 2013.xls', u'BCHM', u' 315', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 316 - Winter 2014.xls', u'BCHM', u' 316', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\MICR 221 - Winter 2014.xls', u'MICR', u' 221', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 (ONLINE) - Summer 2013.xls', u'PHAR', u' 100', 2135], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 (ONLINE) - Winter 2014.xls', u'PHAR', u' 100', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 - Fall 2013.xls', u'PHAR', u' 100', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 340 - Winter 2014.xls', u'PHAR', u' 340', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 450 - Fall 2013.xls', u'PHAR', u' 450', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 210 (ONLINE) - Summer 2013.xls', u'PHGY', u' 210', 2135], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 210 (ONLINE) - Winter 2014.xls', u'PHGY', u' 210', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 214 - Winter 2014.xls', u'PHGY', u' 214B', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 350 - Fall 2013.xls', u'PHGY', u' 350', 2139]]

class GridBoxApp:
	def __init__(self,parent,data):		#it accepts two dimensional lists
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize(data)
		self.status = False


	def initialize(self,data):
		rows = len(data)
		cols = len(data[0])

		for i in range(rows):
			for j in range(cols):

				if j == 0:		#this is the width of the box for subject e.g. ANAT
					width = 90
				elif j == 1:	#width of box for catalog number e.g. 215
					width = 5
				elif j == 2:	#width of box for term number e.g. 2139
					width = 5  	
				elif j == 3:	#width of box for the location of the spreadsheet e.g. C:\Users\DBMS...
					width = 5

				self.box = Label(self.container, text = data[i][j], relief = RIDGE, width = width)
				self.box.grid(row = i,column = j)

		self.subButton = Button(self.container)
		self.subButton['text'] = "OK"
		self.subButton.grid(row = rows + 1, column = 2)
		self.subButton['command'] = self.submit

		self.backButton = Button(self.container)
		self.backButton['text'] = "Back"
		self.backButton.grid(row = rows + 1, column = 3)
		self.backButton['command'] = self.back

	def submit(self):
		self.status = True
		self.parent.destroy()

	def back(self):
		self.status = False
		self.parent.destroy()


def runApp(data):
	root = Tk()
	root.title("List of Excel Spreadsheets")
	app = GridBoxApp(root, data)
	root.mainloop()

	return app.status

if __name__ == '__main__':
	runApp(data)

