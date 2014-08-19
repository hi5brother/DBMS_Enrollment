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
import tkFont

import webbrowser


instructions = ["HI","PLEASE UPDATE THIS","THEN VIEW DAT DATA"]

class helpScreen:
	'''Help screen tk widget that shows up when help is demanded
	'''
	def __init__(self,parent):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize()

	def initialize(self):

		self.scroll = Scrollbar(self.container)


		helpInfo = '''DBMS Enrollment Calculator
						Version 0.61

						More detailed instructions regarding the 
						use of the program can be found in the 
						documentation files.

						To immediately quit the application,
						use task manager and end the process.

						If more help is needed, please contact
						daniel.kao.95@gmail.com OR
						daniel.kao@queensu.ca

						The source code can be found at
						https://github.com/hi5brother/DBMS_Enrollment

					'''
		self.textBox = Text(self.container, height = 22, width = 42, font = ("Helvetica"))
		self.textBox.pack(side = LEFT)
		self.textBox.insert(END,helpInfo)

		self.scroll.pack(side = RIGHT, fill = Y)
		self.scroll.config(command = self.textBox.yview)
		self.textBox.config(yscrollcommand = self.scroll.set)

		self.okButton = Button(self.container)
		self.okButton['text'] = "OK"
		self.okButton.config(width = 10)
		self.okButton.pack(side = BOTTOM, anchor = S)
		self.okButton['command'] = self.quit

	def quit(self):
		self.parent.destroy()


class menuScreen:
	'''Main menu screen with the options for processing the information
	'''
	def __init__(self, parent,instructions):
		self.parent = parent

		self.container = Frame(parent)
		self.container.pack()
		self.makeFonts()

		self.initialize(instructions)
		
		self.quitStatus = True
		self.helpStatus = False
		self.deleteDBStatus = False


	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)

	def initialize(self,instructions):

		#Menu bar stuff
		menubar = Menu(self.parent)
		self.parent.config(menu = menubar)

		filemenu = Menu(self.parent, tearoff=0)

		menubar.add_cascade(label = "Options", menu = filemenu)

		filemenu.add_command(label = "Help", command = self.help)
		filemenu.add_separator()
		filemenu.add_command(label = "Delete Data", command = self.deleteData)
		filemenu.add_separator()
		filemenu.add_command(label = "Exit", command = self.quit)


		#Window content stuff
		#Instructions
		introText = "Welcome. To retrieve enrollment numbers,\n please follow the instructions. \n\n Please close all Excel spreadsheets. \n_______________________"
		self.textBox = Label(self.container, text = introText, font = self.font)
		self.textBox.config(width = 60, height = 5)
		self.textBox.grid(row = 0, column = 0)

		for i in range(len(instructions)):
			instructText = "                 " + str(i + 1) + ". " + instructions[i]
			self.txtBox = Label(self.container,text = instructText,font = self.font)
			self.txtBox.config(anchor = 'w', justify = LEFT)
			self.txtBox.grid(row = i + 1, column = 0, sticky = W)

		#Buttons

		self.infoBox = Label (self.container, text = "_______________________\nPlease select an option.\n",font = self.font)
		self.infoBox.config (width = 20, height = 3)
		self.infoBox.grid(row = i + 2, column = 0)

		options = ["Import Student and Course Data", "Update Program Data","View Data"]

		self.optionBox = Button(self.container,font = self.optionFont)
		self.optionBox['text'] = "1. " + options[0]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = i + 3, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[0])

		self.optionBox = Button(self.container,font = self.optionFont)
		self.optionBox['text'] = "2. " +options[1]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = i + 4, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[1])

		self.optionBox = Button(self.container,font = self.optionFont)
		self.optionBox['text'] = "3. " +options[2]
		self.optionBox.config(width = 60, height = 2)
		self.optionBox.grid (row = i + 5, column = 0)
		self.optionBox['command'] = lambda: self.submit(options[2])

	def submit(self, option):
		self.data = option
		self.quitStatus = False
		self.parent.destroy()

	def deleteData(self):
		self.deleteDBStatus = True
		self.quitStatus = False
		self.parent.destroy()

	def help(self):
		self.helpStatus = True
		root = Tk()
		root.title("Help Information")
		help = helpScreen(root)

	def quit(self):
		self.quitStatus = True
		self.parent.destroy()


def runApp(instructions):
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("DBMS Enrollment Analysis")
	app = menuScreen(root,instructions)
	root.mainloop()

	if app.deleteDBStatus is True:
		return "DELETE DATABASE"
	elif app.quitStatus is True:		#if the quit option is selected
		return "QUIT APPLICATION"

	try:
		return app.data
	
	except AttributeError:		#if close button is clicked, program just closes
		return "QUIT APPLICATION"

if __name__ == '__main__':
	print runApp(instructions)