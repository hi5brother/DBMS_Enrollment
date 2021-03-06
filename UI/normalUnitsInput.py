#-------------------------------------------------------------------------------
# Name:        
#               asks for input for the normal units number 
#               commerce students have 33 in 2014, others have 30 units
#               
#           
# Purpose:
#
# Author:      DBMS
#
# Created:     17/07/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *
import tkFont

programs = [("BA"),
            ("BAH"),
            ("BSC"),
            ("BSCH"),]

class NormalUnitsInputApp:
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
        self.infoBox = Label(self.container, text = "Please enter the program's normal combined \ncourse load for the Fall and Winter terms. \n If the program does not generate grants, input \"n/a\".", font = self.font)
        self.infoBox.config(width = 45, height = 3)
        self.infoBox.grid(row = 0, column = 0)

        self.infoBox2 = Label(self.container, text = "Number of normal units (e.g. 33, 30, 27)",font = self.font)
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
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.container, font = self.buttonFont)            #the quit button will just quit
        self.quitButton['text'] = "Back"
        self.quitButton.grid(row = i + 3,column = 0)
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
    root.title("Normal Units")
    app = NormalUnitsInputApp(root,programs)
    root.mainloop()

    """Error checking and validating the input values
    """
    if app.backStatus:
        return "BACK"
    outputData = []

    try:        #attribute error happens when NO values are output
        for data in app.data:
            
            if "$" in data:     
                data = data.translate(None,"$")         #removes the $ sign if it is present

            if data.isdigit():
                outputData.append(float(data))      #converts the weight value from str to float
            elif data.lower() == "n/a":
                outputData.append(0)        #makes sure it is always n/a
            else:
                return "User Error: Invalid inputs were used"       #if it isnt a number of "n/a"

    except AttributeError:
        return "Data Error: No data was input"

    for data in outputData:
        if data == "":      #error message if a programWeight was not entered
            return "User Error: Not all programs had units inputted"
        elif data > 100.0:    
            return "User Error: The number of units is unreasonably big (over 100)"
        elif data < 0.0:
            return "User Error: The number of untis has negative value"

    return outputData

if __name__ == '__main__':
    print runApp(programs)