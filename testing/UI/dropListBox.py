#-------------------------------------------------------------------------------
# Name:        testing of a droplist
# Purpose:		has two dropdown boxes and returns the values that are inputed
#				
#	self.courseOption = apply(OptionMenu,(self.container,self.var) + tuple(optionsList))	#first dropdown box
#											container		output variable		list of objects
# Author:      DBMS
#
# Created:     25/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

optionsList = [
	"ANAT",
	"BCHM",
	"CHEM",
	"PHAR",]
	
optionsList2 = [
	100,
	101,
	102,
	103,
	104,]
	
class DropListApp:
	def __init__(self,parent,optionsList,optionsList2):
		self.parent = parent
		self.container = Frame(parent)        #frame container
		self.container.pack()
		self.initialize(optionsList, optionsList2)
		
	def initialize(self,optionsList, codeOption):
		self.txtBox = Label(self.container,text = "Please select the course")		#textbox of description
		self.txtBox.config(width = 50, height = 5)
		self.txtBox.pack(side = TOP)
		
		self.var = StringVar()
		self.var.set("Course")
		
		self.courseOption = apply(OptionMenu,(self.container,self.var) + tuple(optionsList))	#first dropdown box
		self.courseOption.pack(side = LEFT)
		
		self.varCode = IntVar()
		self.varCode.set("Code")
		
		self.codeOption = apply(OptionMenu,(self.container,self.varCode) + tuple(codeOption))	#second dropdown box
		self.codeOption.pack(side = LEFT)
		
		self.subButton = Button(self.container)
		self.subButton['text'] = "Submit"
		self.subButton.pack(side = BOTTOM)
		self.subButton['command'] = self.submit
		
		self.data=[]		#initialize the dataset
		
	def submit(self):
		self.data.append(self.var.get())		#data[0] will be the course
		self.data.append(self.varCode.get())	#data[1] will be the course code
		self.parent.destroy()
		
def runApp(optionsList, optionsList2):
	root = Tk()
	root.title("DBMS Enrollment") 
	app = DropListApp(root,optionsList,optionsList2)
	root.mainloop()
	print app.data
	
if __name__ == '__main__':
	runApp(optionsList,optionsList2)
	