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

class DirectoryInputApp:
	''' Has a field that asks for the location of the file directory with the raw data.
	'''
	def __init__(self,parent):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize()

	def initialize(self):
		self.textBox = Label(self.container, text = "Please enter the file directory of the raw data.\n e.g.  'C:\users\DBMS\enrollmentDataDirectory\' ", justify = LEFT)
		self.textBox.config (width = 50, height = 3)
		self.textBox.pack(side = TOP)

		self.entry = Entry(self.container)
		self.entry.config(width = 70)
		self.entry.pack(side = TOP)

		self.subButton = Button(self.container)       #the submit button will process data then quit
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
	root.title("File Location")
	app = DirectoryInputApp(root)
	root.mainloop()

	try:
		return app.data
	except AttributeError:
		return 'Data Error: No directory location was entered.'

if __name__ == '__main__':
	print runApp()

