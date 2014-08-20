#-------------------------------------------------------------------------------
# Name:        
#				asks for values for unit fees
#               special cases are PHD students and what not...
#				
#			
# Purpose:
#
# Author:      DBMS
#
# Created:     16/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *
import tkFont

programs = [("BA"),
			("BAH"),
			("BSC"),
			("BSCH"),]

class FeeUnitsInputApp:
	def __init__(self, parent, programs):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()

		self.makeFonts()
		self.initialize(programs)
		self.backStatus = False

	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)

	def initialize(self, programs):
		self.infoBox = Label(self.container, text = "Please enter the unit fee for each program. \n If no money is generated from the program, input \"n/a\".", font = self.font)
		self.infoBox.config(width = 50, height = 2)
		self.infoBox.grid(row = 0, column = 0)

		self.infoBox2 = Label(self.container, text = "Unit Fee (e.g. $201.96)", font = self.font)
		self.infoBox2.config(width = 40, height = 2)
		self.infoBox2.grid(row = 0, column = 1)

		self.entry = []

		for i in range(len(programs)):
			self.txtBox = Label(self.container, text = programs[i], justify = LEFT, font = self.font)
			self.txtBox.grid(row = i + 1)

			self.entry.append(Entry(self.container, font = self.optionFont))
			self.entry[i].grid(row = i + 1, column = 1)

		self.subButton = Button(self.container, font = self.buttonFont)             #the submit button will process data then quit
		self.subButton['text'] = "Submit"
		self.subButton.grid(row = i + 3,column = 1)
		self.subButton.config(width = 13)
		self.subButton['command'] = self.submit

		self.quitButton = Button(self.container, font = self.buttonFont)            #the quit button will just quit
		self.quitButton['text'] = "Back"
		self.quitButton.grid(row = i + 3,column = 0)
		self.quitButton.config(width = 10)
		self.quitButton['command'] = self.quit


	def submit(self):
		self.data = []                      #initialize the piece of data

		for entry in self.entry:
			self.data.append(entry.get())  #parses the data in the array into a list

		self.parent.destroy()

	def quit(self):
		self.backStatus = True
		self.parent.destroy()

def runApp(programs):
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("Program Unit Fees")
	app = FeeUnitsInputApp(root,programs)
	root.mainloop()

	"""Error checking and validating the input values
	"""

	if app.backStatus:
		return "BACK"

	outputData = []

	try:		#attribute error happens when NO values are output
		for data in app.data:
			if "$" in data:     
				data = data.translate(None,"$")         #removes the $ sign if it is present
 
			if data.isdigit() or data.replace('.',"",1).isdigit():
				outputData.append(float(data))		#converts the $ value from str to float
			elif data.lower() == "n/a":
				outputData.append(0)		#makes sure it is always n/a
			else:
				return "User Error: Invalid inputs were used"		#if it isnt a number of "n/a"

	except AttributeError:
	 	return "Data Error: No data was input"

	for data in outputData:
		if data == "":		#error message if a unit fee was not entered
			return "User Error: Not all programs had unit fees inputted"
		elif data > 1000.0:	
			return "User Error: The unit fee is huge"
		elif data < 0.0:
			return "User Error: Unit fee has negative value"

	return outputData

if __name__ == '__main__':
	output = runApp(programs)
	print output
	# print output
	# print output.count('Error')
	#print 'Error' in output
