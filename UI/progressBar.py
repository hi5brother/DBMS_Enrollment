#-------------------------------------------------------------------------------
# Name:       
#               
#
# Purpose:
#
# Author:      DBMS
#
# Created:     13/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from Tkinter import *
import ttk
messageString = "LOOOL"

class progressBar():
	def __init__(self,parent, messageString):
		self.parent = parent
		self.container = Frame(parent)
		self.container.pack(expand=True, fill=BOTH, side=TOP)
		self.initialize(messageString)

	def initialize(self, messageString):
		self.textBox = Label(self.container, text = messageString)
		self.textBox.config(width = 50, height = 2)
		self.textBox.pack(side = TOP)
		self.progressBar = ttk.Progressbar(self.container, orient = "horizontal", mode = "indeterminate",length = 100)
		self.progressBar.pack(expand = True, fill = BOTH, side = TOP)
		self.progressBar.start(25)

def main(messageString):
	root = Tk()
	root.title("In Progress")
	app = progressBar(root, messageString)

	root.mainloop()

if __name__ == '__main__':
	main(messageString)
