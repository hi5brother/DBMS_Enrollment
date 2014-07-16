#-------------------------------------------------------------------------------
# Name:        testing of a radio button box
# Purpose:		can take a list of strings that will display for each option, and also returns a value related to the string
#
#				 self.button = Radiobutton(self.container, text = option, variable = self.var, value = val, command = self.submit)
#											container		text shown		output variable						command
# Author:      DBMS
#
# Created:     26/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

optionsList = [             #options for radio buttons can be passed into the function
    ("ANAT 315", 1),
    ("ANAT 316", 2),
    ("BIOL 205", 3),
    ("CHEM 281", 4),
    ("MBIO 218", 5),
    ("PHAR 100", 6),
    ("PHAR 340", 7),
    ("PHAR 450", 8),]

optionsList2 = [             #options for radio buttons can be passed into the function
    ("ANAT 315"),
    ("ANAT 316"),
    ("BIOL 205"),
    ("CHEM 281"),
    ("MBIO 218"),
    ("PHAR 100"),
    ("PHAR 340"),
    ("PHAR 450"),]

class RadioBoxAppInt:		#this button returns an integer that corresponds with the options
	def __init__(self,parent,optionsList):	
		self.parent=parent
		self.container=Frame(parent)
		self.container.pack()
		self.initialize(optionsList)

	def initialize(self,optionsList):	#initialize the box and characteristics/features
		self.txtBox=Label(self.container, text = "Please select your option")
		self.txtBox.config(width = 30, height = 5)
		self.txtBox.pack(side = TOP)

		self.var = IntVar()

		for option, val in optionsList:		#add all the buttons for each option
			self.button = Radiobutton(self.container, 
										text = option, 
										variable = self.var, 
										value = val, 
										command = self.submit)
			self.button.pack(anchor = W)

		self.exitButton = Button (self.container)	#exit button
		self.exitButton['text'] = "Exit"
		self.exitButton.pack(side = LEFT)
		self.exitButton['command'] = self.quit		#this button will quit the box

	def submit(self):		#used when an option is pressed
		self.data = self.var.get()
		self.parent.destroy()

	def quit(self):		#used when exit button is pressed
		self.parent.destroy()

class RadioBoxAppStr:		#this only returns the string of the option selected
	def __init__(self,parent,optionsList):	
		self.parent=parent
		self.container=Frame(parent)
		self.container.pack()
		self.initialize(optionsList)

	def initialize(self,optionsList):	#initialize the box and characteristics/features
		self.txtBox=Label(self.container, text = "Please select your option")
		self.txtBox.config(width = 20, height = 5)
		self.txtBox.pack(side = TOP)

		self.var = StringVar()

		for option in optionsList:		#add all the buttons for each option
			self.button = Radiobutton(self.container, 
										text = option,
										indicatoron=0, 	#makes it into indicators instead of radiobuttons
										width=20, 
										padx=20,
										variable = self.var, 
										value = option, 
										command = self.submit)
			self.button.pack(anchor = W)

		self.exitButton = Button (self.container)	#exit button
		self.exitButton['text'] = "Exit"
		self.exitButton.pack(side = LEFT)
		self.exitButton['command'] = self.quit		#this button will quit the box

	def submit(self):		#used when an option is pressed
		self.data = self.var.get()
		self.parent.destroy()

	def quit(self):		#used when exit button is pressed
		self.parent.destroy()

def runApp(optionsList):
	root = Tk()
	root.title("DBMS Enrollment")

	app = RadioBoxAppInt(root, optionsList)
	root.mainloop()

	try:
		print app.data
		return app.data

	except AttributeError:
		print "No data"		#error message if no option is selected
		return None

def runAppStr(optionsList):
	root = Tk()
	root.title("DBMS Enrollment")

	app = RadioBoxAppStr(root, optionsList)
	root.mainloop()

	try:
		print app.data
		return app.data

	except AttributeError:
		print "No data"		#error message if no option is selected
		return None

if __name__ == '__main__':

	#runApp(optionsList)
	runAppStr(optionsList2)