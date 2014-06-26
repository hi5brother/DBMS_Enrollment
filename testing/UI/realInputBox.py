#-------------------------------------------------------------------------------
# Name:        testing of a text input box
# Purpose:
#
# Author:      DBMS
#
# Created:     25/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

class InputDataApp:
    def __init__(self,parent):
        self.parent=parent
        self.container=Frame(parent)        #frame container
        self.container.pack()
        self.initialize()

    def initialize(self):
        self.txtBox = Label(self.container,text = "Please enter the data")
        self.txtBox.config(width = 50, height = 5)
        self.txtBox.pack(side = TOP)

        self.entry = Entry(self.container)        #this is the next field for data entry
        self.entry.pack(side = TOP)

        self.subButton = Button(self.container)       #the submit button will process data then quit
        self.subButton['text'] = "Submit"
        self.subButton.pack(side = LEFT)
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.container)      #the quit button will just quit
        self.quitButton['text'] = "Quit"
        self.quitButton.pack(side = RIGHT)
        self.quitButton['command'] = self.quit

        #self.data = None      #initialize the piece of data

    def submit(self):
        self.data = self.entry.get()  #the data is stored in the object's .data
        self.parent.destroy()

    def quit(self):
        self.parent.destroy()

def runApp():
    root = Tk()
    root.title("DBMS Enrollment")
    app = InputDataApp(root)
    root.mainloop()

    try:
	print app.data
	return app.data
		
    except AttributeError:
	print "No data"
	return None

if __name__ == '__main__':
    runApp()