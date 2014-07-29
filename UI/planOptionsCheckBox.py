#-------------------------------------------------------------------------------
# Name:        checkbox that allows user to select multiple options
#				returns a list of all the selected checkboxes 
#				e.g. ['BCHM','BIOL']
#
# Purpose:		
#
# Author:      DBMS
#
# Created:     28/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
text = ["BCHM", "LISC","NURS"]

class CheckBoxApp:
	def __init__(self,parent,optionsList):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize(optionsList)

	def initialize(self,optionsList):

		self.txtBox = Label(self.container, text = "Please select the required plan breakdowns.")
		self.txtBox.config(width = 40, height = 2)
		self.txtBox.grid(row = 0, column = 0)

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

def runApp(text):
	root = Tk()
	root.title("DBMS Enrollment Plan Select")
	app = CheckBoxApp(root,text)
	root.mainloop()

	try:
		if app.data == []:		#if submit was hit with nothing chosen
				return "User Error: No data was input"
		return app.data 		#returns all the data if it is correct
	
	except AttributeError:		#if the window was closed 
		return "Data Error: No data was input"




if __name__ == '__main__':
	print runApp(text)