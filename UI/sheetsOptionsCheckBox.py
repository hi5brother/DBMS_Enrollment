#-------------------------------------------------------------------------------
# Name:        checkbox that allows user to select multiple options
#				returns a list of all the selected checkboxes 
#				e.g. [plan sheet, blah blah]
#				
#				includes an app with a scroll bar too
#
# Purpose:		
#
# Author:      DBMS
#
# Created:     05/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
text = range(1,10)

class CheckBoxApp:
	def __init__(self,parent,optionsList):
		self.parent = parent
		self.container = Frame(parent)
		self.container.grid(sticky=(N,S,E,W))

		self.initialize(optionsList)

	def initialize(self,optionsList):

		self.txtBox = Label(self.container, text = "Please select the required plan breakdowns.")
		self.txtBox.config(width = 40, height = 2)
		self.txtBox.grid(row = 0, column = 0)

		self.yScroll = Scrollbar(self.container, orient = VERTICAL)
		self.yScroll.grid(row = 0, column = 1, sticky = N + S)

		self.optionsList = optionsList
		self.var = {}

		for option in optionsList:
			self.var[option] = StringVar()
			self.checkbutton = Checkbutton(self.container, text = option, variable = self.var[option], 
												onvalue = option, offvalue = '', justify = LEFT)
			self.checkbutton.grid(row = len(self.var), column = 0)

		self.subButton = Button(self.container)
		self.subButton['text'] = 'Submit'
		self.subButton.grid(row = len(self.var) + 1, column = 0)
		self.subButton['command'] = self.submit

	def submit(self):
		self.data = []
		for option in self.optionsList:
			if self.var[option].get() != '':		#make sure the option is not a blank
				self.data.append(self.var[option].get())

		self.parent.destroy()

	def quit(self):
		self.parent.destroy()

class CheckBoxScrollingApp():
	'''Adds a scrolling bar to the window. The scrollbar is a part of the textbox frame, since
		checkbox frames can't have a scrollbar
	'''
	def __init__(self,parent,optionsList):
		self.parent = parent
		self.initialize(optionsList)

	def initialize(self,optionsList):

		self.vsb = Scrollbar(orient = "vertical")

		tempHeight = (lambda x: 40 if x > 40 else x) (len(optionsList))	#make the length of the box dynamic
		defaultbg = self.parent.cget('bg')	#set default colour
		self.text = Text(self.parent, width = 30, height = tempHeight, bg = defaultbg,
							yscrollcommand = self.vsb.set)

		self.vsb.config(command = self.text.yview)		#scrollbar configuration
		self.vsb.pack(side = "right", fill = "y")
		self.text.pack(side = "top", fill = "both", expand = True)

		self.optionsList = optionsList
		self.var = {}
		for option in optionsList:
			self.var[option] = StringVar()
			self.checkButton = Checkbutton(text = option, variable = self.var[option], 
										onvalue = option, offvalue = '', justify = RIGHT)
			self.text.window_create("end", window = self.checkButton)
			self.text.insert("end", "\n")

		self.infoBox = Label(self.parent, text = "Please select all the required plan breakdowns.")
		self.infoBox.config(width = 60, height = 2)
		self.infoBox.pack(side = "top")

		self.subButton = Button(self.parent)
		self.subButton['text'] = 'Submit'
		self.subButton.pack(side = "bottom")
		self.subButton['command'] = self.submit

	def submit(self):
		self.data = []
		for option in self.optionsList:
			if self.var[option].get() != '':		#make sure the option is not a blank
				self.data.append(self.var[option].get())

		self.parent.destroy()

	def quit(self):
		self.parent.destroy()

def runApp(text):
	root = Tk()
	root.title("DBMS Enrollment Excel Sheet Select")
	app = CheckBoxScrollingApp(root,text)
	root.mainloop()

	try:
		if app.data == []:		#if submit was hit with nothing chosen
				return "User Error: No data was input"
		return app.data 		#returns all the data if it is correct
	
	except AttributeError:		#if the window was closed 
		return "Data Error: No data was input"

def runScrollingApp(text):
	root = Tk()
	root.title("DBMS Enrollment Excel Sheet Select")
	app = CheckBoxScrollingApp(root,text)
	root.mainloop()

	try:
		if app.data == []:		#if submit was hit with nothing chosen
				return "User Error: No data was input"
		return app.data 		#returns all the data if it is correct
	
	except AttributeError:		#if the window was closed 
		return "Data Error: No data was input"


if __name__ == '__main__':
	print runApp(text)