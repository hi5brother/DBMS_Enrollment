#-------------------------------------------------------------------------------
# Name:        initial setup
# Purpose:		pops up for user and has instructions about use of program
#				
# Author:      DBMS
#
# Created:     12/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

import os
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0,parentdir) 
import dateTimeOutput
import extractData as data
import sqlite3

text = ["1.","2.","3."]


class InitialSetupInfoApp:
	def __init__(self,parent,text):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize(text)

	def initialize(self,text):
		introText = "Welcome. To retrieve enrollment numbers,\n please follow the instructions."
		self.textBox = Label(self.container, text = introText)
		self.textBox.config(width = 50, height = 3)
		self.textBox.pack(side = TOP)

		for i in range(len(text)):
			self.txtBox = Label(self.container,text = str(i + 1) + ". " + text[i], anchor = 'w')
			self.txtBox.config(anchor = W, justify = LEFT)
			self.txtBox.pack(side = TOP)

		self.okButton = Button(self.container)
		self.okButton['text'] = "OK"
		self.okButton.pack(side = BOTTOM)
		self.okButton['command'] = self.quit

	def quit(self):
		self.parent.destroy()

def runApp(text):


	root = Tk()
	root.title("Instructions")
	app = InitialSetupInfoApp(root,text)
	root.mainloop()

if __name__ == "__main__":

	runApp(text)