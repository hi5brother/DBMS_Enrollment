#-------------------------------------------------------------------------------
# Name:        
#               asks for input for BIU to determine grant money
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

class BIUInputApp:
    def __init__(self, parent):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack()
        self.initialize()
        self.backStatus = False

    def initialize(self):
        self.infoBox = Label(self.container, text = "Please enter the BIU value.")
        self.infoBox.config(width = 30, height = 2)
        self.infoBox.grid(row = 1, column = 0)

        self.infoBox2 = Label(self.container, text = "BIU value in dollars \n (e.g. 2 386.00, 2 591.98)")
        self.infoBox2.config(width = 30, height = 2)
        self.infoBox2.grid(row = 0, column = 1)

        self.entry = []

        self.entry = (Entry(self.container))
        self.entry.grid(row = 1, column = 1)

        self.subButton = Button(self.container)             #the submit button will process data then quit
        self.subButton['text'] = "Submit"
        self.subButton.grid(row = 3,column = 0)
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.container)            #the quit button will just quit
        self.quitButton['text'] = "Back"
        self.quitButton.grid(row = 3,column = 1)
        self.quitButton['command'] = self.quit

    def submit(self):
        self.data = []                      #initialize the piece of data        
        self.data = self.entry.get()  #parses the data in the array into a list

        self.parent.destroy()

    def quit(self):
        #self.data = None
        self.backStatus = True
        self.parent.destroy()

def runApp():
    root = Tk()
    root.title("BIU Value")
    app = BIUInputApp(root)
    root.mainloop()

    """Error checking and validating the input values
    """
    if app.backStatus:
        return "BACK"

    outputData = []

    try:                                 #attribute error happens when NO values are output
        if "$" in app.data:     
            data = data.translate(None,"$")         #removes the $ sign if it is present
            
        if app.data.isdigit() or data.replace('.',"",1).isdigit():
            outputData.append((float(app.data)) )     #converts the BIU value from str to float
        else:
            return "User Error: Invalid inputs were used"       #if it isnt a number or "n/a"

    except AttributeError:
        return "Data Error: No data was input"

    if outputData[0] == "":      #error message if BIU was not entered
        return "User Error: BIU value was not inputted"
    elif outputData[0] > 10000.0:    
        return "User Error: The BIU value is unreasonably big (over 10 000)"
    elif outputData[0] < 0.0:
        return "User Error: The BIU value has negative value"

    return outputData

if __name__ == '__main__':
    print runApp()