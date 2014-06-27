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
    ("PHAR 340",7),
    ("PHAR 450",8),]

class RadioBoxApp:
	def __init__(self,parent,optionsList):
		self.parent=parent
		self.container=Frame(parent)
		self.container.pack()
		self.initialize(optionsList)

	def initialize(self,optionsList):
		self.txtBox=Label(self.container, text = "Please select your option")
		self.txtBox.config(width = 30, height = 5)
		self.txtBox.pack(side = TOP)

        self.var = IntVar()

        for option, val in optionsList:
		self.button = Radiobutton(self.container, text = option, variable = self.var, value = val, command = self.submit)
		self.button.pack(anchor = W)

        self.exitButton = Button (self.container)
        self.exitButton['text'] = "Exit"
        self.exitButton.pack(side = LEFT)
        self.exitButton['command'] = self.quit		#this button will quit the box

    def submit(self):
        self.data = self.var.get()
        self.parent.destroy()

    def quit(self):
        self.parent.destroy()

def runApp(optionsList):
	root = Tk()
	root.title("DBMS Enrollment")

	app = RadioBoxApp(root, optionsList)
	root.mainloop()

    try:
	print app.data
	return app.data
		
    except AttributeError:
	print "No data"
	return None
		
if __name__ == '__main__':
    runApp(optionsList)
