#-------------------------------------------------------------------------------
# Name:        testing of a text output box
# Purpose:		pass a 
#
# Author:      DBMS
#
# Created:     25/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
text  = ["YO DAWG DIS IS KEWL"," Yo DAWG NOT COOL","LOL MY ABS"]

class OutputDataApp:
	def __init__(self,parent, dataString):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack()
		self.initialize(dataString)
		
	def initialize(self,data):
		for string in data:
			self.txtBox = Label(self.container,text=string)
			self.txtBox.config(width = 50, height = 2)
			self.txtBox.pack(side = TOP)

		
		self.okButton = Button(self.container)
		self.okButton['text'] = "OK"
		self.okButton.pack(side = BOTTOM)
		self.okButton['command'] = self.quit
		
	def quit(self):
		self.parent.destroy()
	
def runApp(text):
	root = Tk()
	root.title("DBMS Enrollment")
	app = OutputDataApp(root, text)
	root.mainloop()
	
if __name__ == '__main__':
	runApp(text)
	
