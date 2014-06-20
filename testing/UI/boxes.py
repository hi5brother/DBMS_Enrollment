#-------------------------------------------------------------------------------
# Name:        testUI
# Purpose:
#
# Author:      DBMS
#
# Created:     19/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from Tkinter import *

class App:

    def __init__(self, master):

        frame = Frame(master)
        frame.pack()


        self.hi_there = Button(frame, text="Hello", command=self.say_hi)    #button
        self.hi_there.pack(side=RIGHT)

        self.ok=Entry(master)                   #text field
        self.ok.pack(side=LEFT)
        self.ok.delete(0,END)
        self.ok.insert(0,"something")

        self.ok2=Button(frame,text="OK",command=self.get)
        self.ok2.pack(side=RIGHT)


    def say_hi(self):
        print "hi there, everyone!"

    def get(self):
        game = self.ok.get()
        print game

class Output():
    def __init__(self,master,data):

        frame=Frame(master)
        frame.pack()

        self.hi_there = Text()          #text field that outputs what is passed into function
        self.hi_there.insert(END,data)
        self.hi_there.pack(side=LEFT)

class Input():
    def __init__(self,master):
        frame=Frame(master)
        frame.pack()

        self.text=Text()                #text field
        self.text.pack(side=RIGHT)
        self.text.insert(END,"Hi")

        self.enter=Entry(master)        #text entry field
        self.enter.pack(side=LEFT)
        self.enter.insert(1,"Please enter name")

        self.ok=Button(frame,text="Confirm",command=master.quit)    #button that quits window when clicked
        self.ok.pack(side=RIGHT)

    def showFields(self):
        return self.enter.get()

class CheckButtonInput():
    def __init__(self,master):
        frame=Frame(master)
        frame.pack()

        self.var=IntVar()

        self.button=Checkbutton(master,text="1",variable=self.var, command=self.printVar)
        self.button.pack()

    def printVar(self):
        print self.var.get()    #returns 1 if the button is checked, and 0 if it isn't

class RadiobuttonInput():
    def __init__(self,master,itemList):
        frame=Frame(master)
        frame.pack()
        MODES = [
        ("ANAT 315", 1),
        ("ANAT 316", 2),
        ("BIOL 205", 3),
        ("CHEM 281", 4),]


        self.v=IntVar()
        for i,mode in MODES:
            self.button=Radiobutton(master,text=i,variable=self.v,value=mode,command=self.output())
            self.button.pack(anchor=W)

        self.exit=Button(master,text="Exit",command=self.output)

    def output(self):
        print self.v.get


class ScrollInput():
    def __init__(self,master,itemList):
        frame=Frame(master)
        frame.pack()

        scroll=Scrollbar(master)
        scroll.pack(side=RIGHT,fill=Y)
        listbox=Listbox(master,yscrollcommand=scroll.set)

        for i in range(len(itemList)):
            listbox.insert(END,itemList[i])

        listbox.pack(side=LEFT,fill=BOTH)
        scroll.config(command=listbox.yview)


def OutputBox():

    root1=Tk()
    app=Output(root1,"hi")      #initialized and takes the second parameter was the output
    root1.mainloop()

def InputBox():

    root1=Tk()
    app=Input(root1)

    root1.mainloop()
    name = app.showFields()

    print name

def checkButtonBox():
    root1=Tk()
    app=CheckButtonInput(root1)
    root1.mainloop()

def RadiobuttonBox(items):
    root1=Tk()
    app=RadiobuttonInput(root1,items)
    root1.mainloop()


def ScrollBox(items):
    root1=Tk()
    app=ScrollInput(root1,items)
    root1.mainloop()

itemList=["Whoa","This is cool","I need this"]
RadiobuttonBox(itemList)
