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
text = "YO DAWG DIS IS KEWL"

class OutputDataApp:
	def __init__(self,parent, dataString):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize(dataString)
		
	def initialize(self,data):
		self.txtBox = Label(self.container,text = data)
		self.txtBox.config(width = len(data), height = 4)
		self.txtBox.pack(side = TOP)
		
		self.okButton = Button(self.container)
		self.okButton['text'] = "OK"
		self.okButton.pack(side = BOTTOM)
		self.okButton['command'] = self.quit
		
	def quit(self):
		self.parent.destroy()
	
def runApp(text):
	root = Tk()
	root.title("DBMS Enrollment ERROR")
	app = OutputDataApp(root, text)
	root.mainloop()
	
if __name__ == '__main__':
	runApp(text)
	
