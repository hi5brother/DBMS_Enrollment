#-------------------------------------------------------------------------------
# Name:        main_menu
# Purpose:      shows the menu options (main functions of the progrm)
#				if one is pressed, this module passes the pressed button to whatever
#
# Author:      DBMS
#
# Created:     17/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *

class menuScreen:
	def __init__(self, parent):
		self.parent = parent

		self.container = Frame(parent)
		self.container.pack()
		self.initialize()
		self.quitStatus = True

	def initialize(self):
		#Menu bar stuff
		menubar = Menu(self.parent)
		self.parent.config(menu = menubar)

		filemenu = Menu(self.parent, tearoff=0)

		menubar.add_cascade(label = "Options", menu = filemenu)

		filemenu.add_command(label = "Help")
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = self.quit)

		#Windows content stuff
		self.infoBox = Label (self.container, text = "Please select an option.")
		self.infoBox.config (width = 20, height = 2)
		self.infoBox.grid(row = 0, column = 0)

		options = ["Update Data", "Update Constants","View Data"]

		self.optionBox = Button(self.container)
		self.optionBox['text'] = options[0]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = 1, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[0])

		self.optionBox = Button(self.container)
		self.optionBox['text'] = options[1]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = 2, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[1])

		self.optionBox = Button(self.container)
		self.optionBox['text'] = options[2]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = 3, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[2])

	def submit(self, option):
		self.data = option
		self.quitStatus = False
		self.parent.destroy()

	def help(self,option):
		pass 	#

	def quit(self):
		self.quitStatus = True
		self.parent.destroy()


def runApp():
	root = Tk()
	root.title("DBMS Enrollment Analysis")
	app = menuScreen(root)
	root.mainloop()

	if app.quitStatus is True:		#if the quit option is selected
		return "QUIT APPLICATION"

	try:
		return app.data
	
	except AttributeError:		#if close button is clicked, program just closes
		return "QUIT APPLICATION"

if __name__ == '__main__':
	runApp()