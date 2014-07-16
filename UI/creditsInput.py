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

        self.infoBox = Label(self.container, text = "Please enter the credits of each course.")
        self.infoBox.config(width = 40, height = 2)
        self.infoBox.grid(row = 0, column = 0)

        self.infoBox2 = Label(self.container, text = "Credits (e.g. 3.0, 4.5)")
        self.infoBox2.config(width = 40, height = 2)
        self.infoBox2.grid(row = 0, column = 1)

        self.entry = []

        for i in range(len(courses)):           #iterates based on number of courses
            self.txtBox = Label(self.container, text = courses[i], justify = LEFT)
            self.txtBox.grid(row = i + 1)    #the name of each course

            self.entry.append(Entry(self.container))
            self.entry[i].grid(row = i + 1, column = 1)          #entry field for credits of each course


        self.subButton = Button(self.container)             #the submit button will process data then quit
        self.subButton['text'] = "Submit"
        self.subButton.grid(row = i + 3,column = 0)
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.container)            #the quit button will just quit
        self.quitButton['text'] = "Quit"
        self.quitButton.grid(row = i + 3,column = 1)
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

    """Error checking and validating the input values
    """

    outputData = []
    try:        #attribute error happens when NO values are output
        for data in app.data:
            try:    
                outputData.append(float(data))      #error if it is not a number (cannot be convert to float)

            except ValueError:
                return "Value Error: A credit value is not a number"
    except AttributeError:
        return "Data Error: No data was input"

    for data in outputData:

        if data == "":         #error message if a credit was not entered
            return "User Error: Not all courses had credits inputted"   
        elif data > 9:
            return "User Error: Credit was greater than 9"
        elif data < 0:
            return "User Error: Credit has negative value"
            
    return outputData
    
if __name__ == '__main__':
    print runApp(courses)