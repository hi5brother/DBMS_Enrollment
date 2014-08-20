#-------------------------------------------------------------------------------
# Name:        find directory
#
# Purpose:      has input box for directory of the raw data
#
# Author:      DBMS
#
# Created:     05/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
import tkFont

class DirectoryInputApp:
	''' Has a field that asks for the location of the file directory with the raw data.
	'''
	def __init__(self,parent):
		self.parent = parent

		self.container = Frame(parent)
		self.container.pack()

		self.makeFonts()
		self.initialize()

	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)


	def initialize(self):
		self.textBox = Label(self.container, text = "Please enter the file directory of the course list spreadsheets.\n\n e.g.  'C:\users\DBMS\enrollmentDataDirectory\'\n ", justify = LEFT, font = self.font)
		self.textBox.config (width = 50, height = 5)
		self.textBox.pack(side = TOP)

		self.entry = Entry(self.container)
		self.entry.config(width = 70)
		self.entry.pack(side = TOP)

		self.subButton = Button(self.container, font = self.buttonFont)       #the submit button will process data then quit
		self.subButton['text'] = "Submit"
		self.subButton.pack(side = BOTTOM)
		self.subButton['command'] = self.submit

	def submit(self):
		self.data = self.entry.get()  #the data is stored in the object's .data
		self.parent.destroy()

	def quit(self):
		self.data = "QUIT"
		self.parent.destroy()

def runApp():
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("File Location")
	app = DirectoryInputApp(root)
	root.mainloop()

	try:
		return app.data
	except AttributeError:
		return 'Data Error: No directory location was entered.'

if __name__ == '__main__':
	print runApp()

