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
import tkFont
text = range(1,10)


class CheckBoxScrollingApp():
	'''Adds a scrolling bar to the window. The scrollbar is a part of the textbox frame, since
		checkbox frames can't have a scrollbar
	'''
	def __init__(self,parent,optionsList):
		self.parent = parent
		self.makeFonts()
		self.initialize(optionsList)

	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)

	def initialize(self,optionsList):

		self.vsb = Scrollbar(orient = "vertical")

		tempHeight = (lambda x: 60 if x > 60 else x) (len(optionsList))	#make the length of the box dynamic
		defaultbg = self.parent.cget('bg')	#set default colour
		self.text = Text(self.parent, width = 30, height = tempHeight, bg = defaultbg,
							yscrollcommand = self.vsb.set, font = self.font)

		self.vsb.config(command = self.text.yview)		#scrollbar configuration
		self.vsb.pack(side = "right", fill = "y")
		self.text.pack(side = "top", fill = "both", expand = True)

		self.optionsList = optionsList
		self.var = {}
		for option in optionsList:
			self.var[option] = StringVar()
			self.checkButton = Checkbutton(text = option, variable = self.var[option], 
										onvalue = option, offvalue = '', justify = RIGHT, font = self.optionFont)
			self.text.window_create("end", window = self.checkButton)
			self.text.insert("end", "\n")

		self.infoBox = Label(self.parent, text = "Please select all the required Excel spreadsheet queries.", font = self.font)
		self.infoBox.config(width = 50, height = 2)
		self.infoBox.pack(side = "top")

		self.subButton = Button(self.parent, font = self.buttonFont)
		self.subButton['text'] = 'View Data'
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


def runScrollingApp(text):
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("Excel Sheet Query")
	app = CheckBoxScrollingApp(root,text)
	root.mainloop()

	try:
		if app.data == []:		#if submit was hit with nothing chosen
				return "User Error: No data was input"
		return app.data 		#returns all the data if it is correct
	
	except AttributeError:		#if the window was closed 
		return "Data Error: No data was input"


if __name__ == '__main__':
	print runScrollingApp(text)