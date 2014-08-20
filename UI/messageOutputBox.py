#-------------------------------------------------------------------------------
# Name:        outputs messages#				
#			
# Purpose:		takes a list with strings and then outputs it in a box
#
# Author:      DBMS
#
# Created:     13/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
import tkFont
text  = ["YO DAWG DIS IS KEWL"," Yo DAWG NOT COOL","LOL MY ABS"]

class OutputDataApp:
	def __init__(self,parent, dataString):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()

		self.makeFonts()
		self.initialize(dataString)

	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)

	def initialize(self,data):
		for string in data:
			self.txtBox = Label(self.container,text=string, font = self.font)
			self.txtBox.config(width = 50, height = 2)
			self.txtBox.pack(side = TOP)

		self.okButton = Button(self.container, font = self.buttonFont)
		self.okButton['text'] = "OK"
		self.okButton.pack(side = BOTTOM)
		self.okButton['command'] = self.quit
		
	def quit(self):
		self.parent.destroy()
	
def runApp(text):
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("DBMS Enrollment Calculator")
	app = OutputDataApp(root, text)
	root.mainloop()
	
if __name__ == '__main__':
	runApp(text)
