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
        ("ANAT 216"),
        ("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),
        ("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),
        ("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),
        ("BIOL 102"),
        ("BIOL 103"),
        ("ANAT 215"),
        ("ANAT 216"),]

class CreditsInputApp:
    def __init__(self,parent,courses):
        self.parent = parent
        self.container = Frame(parent)           #frame container
        self.container.pack()
        self.initialize(courses)        #pass a list of courses 
        self.backStatus = False


    def initialize(self,courses):  

        self.infoBox = Label(self.container, text = "Please enter the credits of each course. \n For a two term course, please divide  \nthe credits by two (e.g. PHGY 214A has 3 credits).")
        self.infoBox.config(width = 40, height = 3)
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
        self.quitButton['text'] = "Back"
        self.quitButton.grid(row = i + 3,column = 1)
        self.quitButton['command'] = self.quit

    def submit(self):
        self.data = []                      #initialize the piece of data

        for entry in self.entry:
            self.data.append(entry.get())  #parses the data in the array into a list
        
        self.parent.destroy()

    def quit(self):
        self.backStatus = True
        self.parent.destroy()


class CreditsInputScrollingApp2():

    def __init__(self, parent, courses):
        self.parent = parent
        self.container = Frame(parent)
        self.container.pack()
        self.initialize(courses)
        self.backStatus = False

    def initialize(self, courses):

        '''Set up the canvas, which houses the scroll bar
        '''
        self.scroll = Scrollbar(self.container, orient='vertical')

        self._canvas = Canvas(self.container, yscrollcommand=self.scroll.set, width = 500, height = 100)


        self.scroll.config(command=self._canvas.yview)
        self.scroll.pack(side = "right", fill = "y")

        self.inFrame = Frame(self._canvas)

        '''Add the widgets into the canvas (self.inFrame)
        '''

        self.infoBox = Label(self.inFrame, text = "Please enter the credits of each course. \n For a two term course, please divide  \nthe credits by two (e.g. PHGY 214A has 3 credits).")
        self.infoBox.config(width = 40, height = 3)
        self.infoBox.grid(row = 0, column = 0)

        self.infoBox2 = Label(self.inFrame, text = "Credits (e.g. 3.0, 4.5)")
        self.infoBox2.config(width = 40, height = 2)
        self.infoBox2.grid(row = 0, column = 1)

        self.entry = []

        for i in range(len(courses)):           #iterates based on number of courses
            self.txtBox = Label(self.inFrame, text = courses[i], justify = LEFT)
            self.txtBox.grid(row = i + 1)    #the name of each course

            self.entry.append(Entry(self.inFrame))
            self.entry[i].grid(row = i + 1, column = 1)          #entry field for credits of each course


        self.subButton = Button(self.inFrame)             #the submit button will process data then quit
        self.subButton['text'] = "Submit"
        self.subButton.grid(row = i + 3,column = 0)
        self.subButton['command'] = self.submit

        self.quitButton = Button(self.inFrame)            #the quit button will just quit
        self.quitButton['text'] = "Back"
        self.quitButton.grid(row = i + 3,column = 1)
        self.quitButton['command'] = self.quit

        self.inFrame.pack()

        '''Create the widget in the canvas 
        '''
        print self.inFrame.winfo_reqwidth()
        print self.inFrame.winfo_reqheight()
        print self._canvas.winfo_reqwidth()
        print self._canvas.winfo_reqheight()
        #self._canvas.config(width = self.inFrame.winfo_width(), height = self.inFrame.winfo_height())
        self._canvas.create_window(0,0, window = self.inFrame, anchor = N + W)
        self._canvas.pack(side = LEFT, fill = BOTH, expand = True)
        self._canvas.bind("<Configure>", self.resize_frame)

    def resize_frame(self, e):
        self._canvas.itemconfig(self.inFrame, height=e.height, width=e.width)

    def submit(self):
        self.data = []                      #initialize the piece of data

        for entry in self.entry:
            self.data.append(entry.get())  #parses the data in the array into a list
        
        self.parent.destroy()

    def quit(self):
        self.backStatus = True
        self.parent.destroy()



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

        text = Label(self, text = "John")
        text.pack()
        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

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


class VerticalScrolledFrame2(Frame):
    def __init__(self,parent):
        Frame.__init__(self,parent)

        self.vscrollbar = Scrollbar(self, orient = VERTICAL)
        self.vscrollbar.pack(fill = Y, side = RIGHT, expand = FALSE)
        self.canvas = Canvas(self, yscrollcommand = vscrollbar.set)
        self.canvas.pack(side = LEFT, fill = BOTH, expand = TRUE)
        self.vscrollbar.config(command = canvas.yview)

        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        self.interior = interior = Frame(self.canvas)
        self.interior_id = self.canvas.create_window(0,0,window = self.interior, anchor = NW)

        def _configure_interior(event):
            size = (self.interior.winfo_reqwidth(), self.interior.winfo_reqheight())
            self.canvas.config (width = self.interior.winfo_reqdith())

            if interior.winfo_reqdith() != self.canvas.winfo_width():
                self.canvas.config(width = interior.winfo_reqwidth())
        self.interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if self.interior.winfo_reqdith() != self.canvas.winfo_width():
                self.canvas.itemconfigure(interior_id, width = self.canvas.winfo_width())

        self.interior.bind('<Configure>', _configure_canvas)

        self.pack()

class SampleApp(Tk):
        def __init__(self, courses):
            root = Tk.__init__(self)

            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.pack()
            self.initialize(courses)

        def initialize(self,courses):
            self.infoBox = Label(self.frame.interior, text = "Please enter the credits of each course. \n For a two term course, please divide  \nthe credits by two (e.g. PHGY 214A has 3 credits).")
            #self.infoBox.config(width = 40, height = 3)
            self.infoBox.grid(row = 0, column = 0)

            self.infoBox2 = Label(self.frame.interior, text = "Credits (e.g. 3.0, 4.5)")
            #self.infoBox2.config(width = 40, height = 2)
            self.infoBox2.grid(row = 0, column = 1)

            self.entry = []

            for i in range(len(courses)):           #iterates based on number of courses
                self.txtBox = Label(self.frame.interior, text = courses[i], justify = LEFT)
                self.txtBox.grid(row = i + 1)    #the name of each course

                self.entry.append(Entry(self.frame.interior))
                self.entry[i].grid(row = i + 1, column = 1)          #entry field for credits of each course


            self.subButton = Button(self.frame.interior)             #the submit button will process data then quit
            self.subButton['text'] = "Submit"
            self.subButton.grid(row = i + 3,column = 0)
            self.subButton['command'] = self.submit

            self.quitButton = Button(self.frame.interior)            #the quit button will just quit
            self.quitButton['text'] = "Back"
            self.quitButton.grid(row = i + 3,column = 1)
            self.quitButton['command'] = self.quit
        def submit(self):
            self.data = []                      #initialize the piece of data

            for entry in self.entry:
                self.data.append(entry.get())  #parses the data in the array into a list
            
            self.frame.destroy()

        def quit(self):
            self.backStatus = True
            self.frame.destroy()




def runApp(courses):
    root = Tk()
    root.title("Course Credits")
    app = CreditsInputApp(root,courses)
    root.mainloop()

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

def runScrollingApp(courses):
    root = Tk()
    root.title("Course Credits")
    app = SampleApp(courses)
    root.mainloop()

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
    print runScrollingApp(courses)