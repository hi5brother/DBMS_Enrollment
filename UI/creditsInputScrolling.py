#-------------------------------------------------------------------------------
# Name:        input credits of a course WITH SCROLLING
#               can be scaled to include all the courses in the list
#               used to calculate share of tuition
#               
#               returns all the data in a list
#               if info is missing, it returns an error message
# Purpose:
#
# Author:      DBMS
#
# Created:     08/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
'''Create a scrolling parent frame with a canvas = self.frame.interior
    Put widgets into self.frame.interior after inheriting the VerticalScrolledFrame object
'''
from Tkinter import *

courses=[("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),
        ("BIOL 102"),
        ("ANAT 216"),]

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())
        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

    def destroyFrame(self):
        self.quit()

class SampleApp(Tk):
        def __init__(self, courses):
            root = Tk.__init__(self)

            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()

            self.initialize(courses)
            self.backStatus = False

        def initialize(self,courses):
            self.infoBox = Label(self.frame.interior, text = "Please enter the credits of each course. \n For a two term course, please divide  \nthe credits by two (e.g. PHGY 214A has 3 credits).")
            self.infoBox.config(width = 40, height = 3)
            self.infoBox.grid(row = 0, column = 0)

            self.infoBox2 = Label(self.frame.interior, text = "Credits (e.g. 3.0, 4.5)")
            self.infoBox2.config(width = 40, height = 2)
            self.infoBox2.grid(row = 0, column = 1)

            self.entry = []

            for i in range(len(courses)):           #iterates based on number of courses
                self.txtBox = Label(self.frame.interior, text = courses[i], justify = LEFT)
                self.txtBox.grid(row = i + 1)    #the name of each course

                self.entry.append(Entry(self.frame.interior))
                self.entry[i].grid(row = i + 1, column = 1)          #entry field for credits of each course
                self.entry[i].insert(0, 3.0)


            self.subButton = Button(self.frame.interior)             #the submit button will process data then quit
            self.subButton['text'] = "Submit"
            self.subButton.grid(row = i + 3,column = 1)
            self.subButton['command'] = self.submit

            self.quitButton = Button(self.frame.interior)            #the quit button will just quit
            self.quitButton['text'] = "Back"
            self.quitButton.grid(row = i + 3,column = 0)
            self.quitButton['command'] = self.quit
        def submit(self):
            self.data = []                      #initialize the piece of data

            for entry in self.entry:
                self.data.append(entry.get())  #parses the data in the array into a list
            self.frame.destroyFrame()            
            self.frame.interior.destroy()

        def quit(self):
            self.backStatus = True
            self.frame.destroyFrame()
            self.frame.interior.destroy()

def runApp(courses):
    
    app = SampleApp(courses)
    app.title("DBMS Enrollment Credits Input")
    app.mainloop()
    app.destroy()

    """Error checking and validating the input values
    """

    if app.backStatus:
        return "BACK"
        
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
