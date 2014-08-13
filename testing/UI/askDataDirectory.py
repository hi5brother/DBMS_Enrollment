#-------------------------------------------------------------------------------
# Name:        find directory
#
# Purpose:      has input box for directory of the raw data
#
# Author:      DBMS
#
# Created:     31/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *

class DirectoryInputApp:
	def __init__(self,parent):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize()

	def initialize(self):
		self.textBox = Label(self.container, text = "Please enter the file location of the raw data.", justify = LEFT)
		self.textBox.config (width = 50, height = 3)
		self.textBox.pack(side = TOP)

		self.entry = Entry(self.container)
		self.entry.config(width = 70)
		self.entry.pack(side = TOP)

		self.subButton = Button(self.container)       #the submit button will process data then quit
		self.subButton['text'] = "Submit"
		self.subButton.pack(side = LEFT)
		self.subButton['command'] = self.submit

		self.quitButton = Button(self.container)      #the quit button will just quit
		self.quitButton['text'] = "Quit"
		self.quitButton.pack(side = RIGHT)
		self.quitButton['command'] = self.quit

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
