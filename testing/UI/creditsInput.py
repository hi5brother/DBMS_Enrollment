#-------------------------------------------------------------------------------
# Name:        input credits of a course
#               can be scaled to include all the courses in the list
#               used to calculate share of tuition
#               
#               returns all the data in a list
#               if info is missing, it returns an error message
# Purpose:
#
# Author:      DBMS
#
# Created:     15/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

courses=[("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),]

class CreditsInputApp:
    def __init__(self,parent,courses):
        self.parent = parent
        self.container = Frame(parent)           #frame container
        self.container.pack()
        self.initialize(courses)        #pass a list of courses 

    def initialize(self,courses):  

        self.entry = []
        for i in range(len(courses)):           #iterates based on number of courses
            self.txtBox = Label(self.container, text = courses[i]).grid(row = i)    #the name of each course

            self.entry.append(Entry(self.container))
            self.entry[i].grid(row = i,column = 1)          #entry field for credits of each course


        self.subButton = Button(self.container)             #the submit button will process data then quit
        self.subButton['text'] = "Submit"
        self.subButton.grid(row = i + 1,column = 0)
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.container)            #the quit button will just quit
        self.quitButton['text'] = "Quit"
        self.quitButton.grid(row = i + 1,column = 1)
        self.quitButton['command'] = self.quit

    def submit(self):
        self.data = []                      #initialize the piece of data

        for entry in self.entry:
            self.data.append(entry.get())  #parses the data in the array into a list
        
        self.parent.destroy()

    def quit(self):
        self.parent.destroy()

def runApp(courses):
    root = Tk()
    root.title("DBMS Enrollment Course Credits")
    app = CreditsInputApp(root,courses)
    root.mainloop()

    for data in app.data:
        try:    
            data = float(data)      #error if it is not a number (cannot be convert to float)
        except ValueError:
            return "Value Error: A credit value is not a number"

    for data in app.data:
        if data == "":         #error message if a credit was not entered
            return "User Error: Not all courses had credits inputted"   

    try:
	   print app.data
	   return app.data
		
    except AttributeError:
	   print "No data"
	   return None

if __name__ == '__main__':
    runApp(courses)