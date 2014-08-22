#-------------------------------------------------------------------------------
# Name:        gridbox output box

# Purpose:		will output a two dimensional list in the form of a grid, with a scrollbar
#
# Author:      DBMS
#
# Created:     21/08/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import xlwt
import tkFont

from Tkinter import *
data = [['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 215 - Fall 2013.xls', u'ANAT', u' 215', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 216 - Winter 2014.xls', u'ANAT', u' 216', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 315 - Fall 2013.xls', u'ANAT', u' 315', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\ANAT 316 - Winter 2014.xls', u'ANAT', u' 316', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 218 - Winter 2014.xls', u'BCHM', u' 218', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 310 - Winter 2014.xls', u'BCHM', u' 310B', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 313 - Winter 2014.xls', u'BCHM', u' 313', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 315 - Fall 2013.xls', u'BCHM', u' 315', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\BCHM 316 - Winter 2014.xls', u'BCHM', u' 316', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\MICR 221 - Winter 2014.xls', u'MICR', u' 221', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 (ONLINE) - Summer 2013.xls', u'PHAR', u' 100', 2135], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 (ONLINE) - Winter 2014.xls', u'PHAR', u' 100', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 100 - Fall 2013.xls', u'PHAR', u' 100', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 340 - Winter 2014.xls', u'PHAR', u' 340', 2139], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHAR 450 - Fall 2013.xls', u'PHAR', u' 450', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 210 (ONLINE) - Summer 2013.xls', u'PHGY', u' 210', 2135], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 210 (ONLINE) - Winter 2014.xls', u'PHGY', u' 210', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 214 - Winter 2014.xls', u'PHGY', u' 214B', 2141], ['C:\\Users\\DBMS\\Documents\\Daniel\\DBMS_Enrollment\\full_data\\PHGY 350 - Fall 2013.xls', u'PHGY', u' 350', 2139]]

class VerticalScrolledFrame(Frame):
    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)            

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set, height = 350)
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

class GridBoxApp(Tk):
	'''it accepts two dimensional lists (with columns for file location, course code, cat number, term number)
	'''
	def __init__(self,data):		
		root = Tk.__init__(self)

		self.frame = VerticalScrolledFrame(root)
		self.frame.pack()
		self.makeFonts()
		
		self.initialize(data)
		self.status = False

	def makeFonts(self):
		#Font stuff
		self.font = tkFont.Font(family = "Segoe UI", size = 12)
		self.gridFont = tkFont.Font (family = "Futura", size = 10)
		self.optionFont = tkFont.Font(family = "Segoe UI", size = 10)
		self.buttonFont = tkFont.Font(family = "Segoe UI", size = 10)

	def initialize(self,data):
		rows = len(data)
		cols = len(data[0])

		for i in range(rows):
			for j in range(cols):

				if j == 0:		#this is the width of the box for subject e.g. ANAT
					width = 90
				elif j == 1:	#width of box for catalog number e.g. 215
					width = 7
				elif j == 2:	#width of box for term number e.g. 2139
					width = 5  	
				elif j == 3:	#width of box for the location of the spreadsheet e.g. C:\Users\DBMS...
					width = 7

				self.box = Label(self.frame.interior, text = data[i][j], relief = RIDGE, width = width, font = self.gridFont)
				self.box.grid(row = i,column = j)

		self.subButton = Button(self.frame.interior, font = self.buttonFont)
		self.subButton['text'] = "Import"
		self.subButton.config(width = 13)
		self.subButton.grid(row = rows + 1, column = 2, columnspan = 2)
		self.subButton['command'] = self.submit

		self.backButton = Button(self.frame.interior, font = self.buttonFont)
		self.backButton['text'] = "Back"
		self.backButton.config(width = 7)
		self.backButton.grid(row = rows + 1, column = 1)
		self.backButton['command'] = self.back

	def submit(self):
		self.status = True
		self.frame.destroyFrame()            
		self.frame.interior.destroy()

	def back(self):
		self.status = False
		self.frame.destroyFrame()
		self.frame.interior.destroy()


def runApp(data):
	app = GridBoxApp(data)
	app.iconbitmap('icon_table.ico')
	app.title("List of Excel Spreadsheets")
	app.mainloop()

	try:
		app.destroy()
	except tkinter.TclError:    #for some reason, the app frame does not go away afterwards
		pass

	return app.status

if __name__ == '__main__':
	runApp(data)

