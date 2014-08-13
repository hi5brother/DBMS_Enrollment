# from Tkinter import Scrollbar as tkScrollBar
# from Tkinter import Frame as tkFrame
# from Tkinter import Canvas as tkCanvas
# from Tkinter import Entry as tkEntry
# from Tkinter import StringVar as tkStringVar
# from Tkinter import Tk, HORIZONTAL, N, S, E, W, RIGHT, LEFT, BOTTOM, X, Y, BOTH
# from Tkinter import TOP


# class Widget(tkFrame):
#     def __init__(self, master=None):
#         tkFrame.__init__(self, master)

#         self._str    = tkStringVar()
#         self._widget = tkEntry(self)

#         self._widget.config(textvariable=self._str, borderwidth=1, width=0)
#         self._widget.pack(expand=True, fill=X)

#     def settext(self, str_):
#         self._str.set(str_)

#     def gettext(self):
#         return self._str.get()


# class Application(tkFrame):
#     def __init__(self, rows, cols, master=None):
#         tkFrame.__init__(self, master)

#         yScroll = tkScrollBar(self)
#         xScroll = tkScrollBar(self, orient=HORIZONTAL)

#         self._canvas = tkCanvas(self,
#                 yscrollcommand=yScroll.set, xscrollcommand=xScroll.set)
#         yScroll.config(command=self._canvas.yview)
#         xScroll.config(command=self._canvas.xview)

#         self._table      = [[0 for x in range(rows)] for x in range(cols)]
#         self._tableFrame = tkFrame(self._canvas)

#         for col in range(cols):
#             self._tableFrame.grid_columnconfigure(col, weight=1)
#             for row in range(rows):
#                 self._table[row][col] = Widget(master=self._tableFrame)
#                 self._table[row][col].settext("(%d, %d)" % (row, col))
#                 self._table[row][col].grid(row=row, column=col, sticky=E+W)

#         print self._tableFrame.winfo_reqheight()

#         # For debugging
#         self._canvas.config(background="blue")
#         self._tableFrame.config(background="red")

#         yScroll.pack(side=RIGHT, fill=Y)
#         xScroll.pack(side=BOTTOM, fill=X)

#         self._canvas.create_window(0, 0, window=self._tableFrame, anchor=N+W)
#         self._canvas.pack(side=LEFT, fill=BOTH, expand=True)


# tkRoot  = Tk()

# # Application Size and Center the Application
# appSize = (800, 600)
# w       = tkRoot.winfo_screenwidth()
# h       = tkRoot.winfo_screenheight()

# x = w / 2 - appSize[0] / 2
# y = h / 2 - appSize[1] / 2
# tkRoot.geometry("%dx%d+%d+%d" % (appSize + (x, y)))
# tkRoot.update_idletasks() # Force geometry update

# app = Application(5, 5, master=tkRoot)
# app.pack(side=TOP, fill=BOTH, expand=True)
# tkRoot.mainloop()
'''~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
http://stackoverflow.com/questions/16188420/python-tkinter-scrollbar-for-frame
'''
from Tkinter import *   # from x import * is bad practice
from ttk import *

# http://tkinter.unpythonic.net/wiki/VerticalScrolledFrame

class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling

    """
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


if __name__ == "__main__":

    class SampleApp(Tk):
        def __init__(self):
            root = Tk.__init__(self)


            self.frame = VerticalScrolledFrame(root)
            self.frame.pack()
            self.label = Label(text="Shrink the window to activate the scrollbar.")
            self.label.pack()

            self.infoBox = Label(self.frame.interior, text = "Please enter the credits of each course. \n For a two term course, please divide  \nthe credits by two (e.g. PHGY 214A has 3 credits).")
            #self.infoBox.config(width = 40, height = 3)
            self.infoBox.grid(row = 0, column = 0)

            self.infoBox2 = Label(self.frame.interior, text = "Credits (e.g. 3.0, 4.5)")
            #self.infoBox2.config(width = 40, height = 2)
            self.infoBox2.grid(row = 0, column = 1)

            self.entry = []

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
            
            self.parent.destroy()

        def quit(self):
            self.backStatus = True
            self.parent.destroy()

    app = SampleApp()
    app.mainloop()