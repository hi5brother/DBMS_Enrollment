#-------------------------------------------------------------------------------
# Name:        error message box that accepts a string that will be displayed in the box. 
#				has an OK button that is pressed to kill the box
# Purpose:		
#
# Author:      DBMS
#
# Created:     15/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
import tkFont
text = "YO DAWG DIS IS KEWL"

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
		

		self.txtBox = Label(self.container,text = data, font = self.font)
		self.txtBox.config(width = len(data) + 5, height = 4)
		self.txtBox.pack(side = TOP)
		
		self.okButton = Button(self.container,font = self.buttonFont)
		self.okButton.font = self.font
		self.okButton['text'] = "OK"
		self.okButton.pack(side = BOTTOM)
		self.okButton['command'] = self.quit
		
	def quit(self):
		self.parent.destroy()
	
def runApp(text):
	root = Tk()
	root.iconbitmap('icon_table.ico')
	root.title("DBMS Enrollment Error")
	app = OutputDataApp(root, text)
	root.mainloop()
	
if __name__ == '__main__':
	runApp(text)
	
