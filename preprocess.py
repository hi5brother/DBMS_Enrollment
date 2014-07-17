#-------------------------------------------------------------------------------
# Name:        preprocess_v3
# Purpose:      create a database by extracting data from a spreadsheet
#               extract the data and process it into the SQLite database
#               This extracts the data from multiple spreadsheets
#               Uses a scaled preprocess_v1 and should be changed later on
#               further scales the application to take all the spreadsheets
#               preprocesses the excel workbooks to make things into floats
#
#
# Author:      DBMS
#
# Created:     21/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import sys
import sqlite3  #SQLite API
import xlrd #reading xls files
import xlwt #writing xls files
import string
import types
import win32com.client  #for executing excel macros

import studentProcessing        #module that deletes whitespace, double/triple majors when processing each spreadsheet
import dbFormat                 #formats the tables for the database


sys.path.append(os.getcwd() + '/UI')    #adding the UI modules to the path
import creditsInput     #UI box for inputting credits
import feeUnitsInput       #UI box for inputting unit fees
import programWeightsInput
import formulaFeesInput
import BIUInput

import errorMessageBox  #UI that displays the error

import calcTuition

class Student:
    def __init__(self):#,studID,program,proj_level,plan1,plan2,total_credits):
        pass

    def printValues(self):  #output the attributes of a student
        print str(self.studID)+" ,"+self.program+" ,"+str(self.proj_level)+" ,"+self.plan

    def convert(self):  #convert student ID from float into int
        self.studID=int(self.studID)
        self.proj_level=int(self.proj_level)

    ''' The student object is used to store the traits of each student (e.g.
        stud_id, program, proj_level). These traits are declared and added to each
        object when the data is parsed from the Excel workbooks
    '''

class Course:
    def __init__(self):#subject, catalog_number, credits, term
        pass

    def concatenateCourseCode(self):
        return str(self.subject) + str(self.catalog)

    def printCourse(self):
        print str(self.subject) + " " + str(self.catalog) + " ," + str(self.credits)

def findFiles(location, extension):

    ''' #Searches a location for all files that have a specific extension
        #Used to return all the excel workbooks (xls) locations to the main function
    '''
    workbooksList = []    #delcaration, stores the file locations of all the workbooks

    for filename in os.listdir(location): #goes through every file in the folder
        if filename[-3:] == extension:
            workbooksList.append(location + "\\" + filename)  #adds the file if the last 3 char are "xls"

    return workbooksList

def checkTableExist(tableName):
    '''Checks if the table with "tableName" exists
    Returns True if it exists and False if it doesn't exist
    '''
    c.execute('''SELECT CASE
                WHEN tbl_name = ? THEN 1
                ELSE 0
                END
                FROM sqlite_master
                WHERE tbl_name = ? AND type = "table"''',(str(tableName),str(tableName)))

    temp = c.fetchone()

    if temp == (1,):
        return True
    else:
        return False


def getStudents(headingsNeeded, currentSheet):

    headingsLocation = []

    for i in range(len(headingsNeeded)):
        headingsLocation.append(dbFormat.findCol(currentSheet,headingsNeeded[i]))

    studList = [Student() for i in range(currentSheet.nrows)]         #create the array of students

    print str(currentSheet) + " " + str(currentSheet.nrows) #@@@@@@@@@@@@@@@@@@@@@@

    for row in range(currentSheet.nrows):
        '''parse the data of each row into a Student object, which is in the array'''
        values = []

        for dataCol in headingsLocation:

            values.append(currentSheet.cell(row,dataCol).value)

        studList[row].studID = (values[0])
        studList[row].program = values[1]
        studList[row].proj_level = (values[2])
        studList[row].plan = values[3]
        studList[row].plan2 = ""
        studList[row].plan3 = ""
        #print type(studList[row].studID)

    popRows = []

    popRows.extend(studentProcessing.findImproperStudent(studList))   #finds the headings and whitespaces and flags the index
    #print popRows
    for i in studentProcessing.findTriple(studList):
       '''finds the triples (accounts for con ed, who MAY have B.ED + double major for their plans, 3 rows)'''
       studList[i + 2].plan3 = studList[i].plan
    popRows.extend(studentProcessing.findTriple(studList))            #flags the index for triples

    #print str(currentSheet) + str(len(studList)) #@@@@@@@@@@@@@@@@@@
    #print popRows
    for i in reversed(popRows):                     #when iterating in reverse, the wrong things do not get popped off the list
        studList.pop(i)                             #pop off headings/whitespaces and triples

    popRows = []                                      #resets the list so we can add duplicate indexes

    for i in studentProcessing.findDuplicate(studList):               #finds the duplicates and adds the indices to the popRows list
        studList[i + 1].plan2 = studList[i].plan        #before the duplicate is popped, the second plan is added to the data row
    popRows.extend(studentProcessing.findDuplicate(studList))

    for i in reversed(popRows):                     #when iterating in reverse, the wrong things do not get popped off the list
        studList.pop(i)
    popRows = []

    for i in range(len(studList)):
        studList[i].convert()                       #finalize input data

    return studList                                    #returns a list of Student objects

def getCourseInfo(neededHeadings,currentSheet):
    '''Returns a course object, which contains the necessary info for a course record
        in the database, for the course table
    '''

    headingsLocation = []

    for i in range (len(neededHeadings)):
        headingsLocation.append(dbFormat.findCol(currentSheet,neededHeadings[i]))

    courseInfo = Course()     #initialize the course object

    values = []

    for dataCol in headingsLocation:
        values.append(currentSheet.cell(2,dataCol).value)

    courseInfo.subject = values[0]
    courseInfo.catalog = values[1]
    courseInfo.term = values[2]

    return courseInfo

def checkError(funcOutput):     #returns false is there is an error, returns true if no error exists
    '''Checks the output of the function to see if an error message was returned
    '''
    if 'Error' in funcOutput:       #sees if the output returns an error
        return False
    else:                       #output does not return an error
        return True

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Open Database
''' Initialize all the connections to SQLite
    Configure database stuff
'''
cdLocation = os.getcwd()
dbLocation = cdLocation + "\\testv2.db" #"""@@@@@@@@@@@@@@@@@@@ TAKE OUT THE HARD CODE"""
rawDataLocation = cdLocation + "\\full_data"

os.remove(dbLocation) #"""@@@@@@@@@@ REMOVES THE DB EACH TIME THIS RUNS, FOR TESTING PURPOSES"""

conn = sqlite3.connect(dbLocation)
c = conn.cursor()

c.execute("PRAGMA foreign_keys=ON;")    #enables foreign keys

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Open Excel workbooks
'''Initialize the Excel workbook connections for reading using xlrd module
    Find all xls files and then store the location and addresses of all of them
'''
excelExtension = "xls"
filesList = findFiles(rawDataLocation,excelExtension)

wbData = []
sheetAddress = []
for i in range(len(filesList)):
    wbData.append(xlrd.open_workbook(filesList[i]))
    sheetAddress.append(wbData[i].sheet_by_index(0)) #will access and store the location of the FIRST sheet in each workbook

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Preprocess the excel columns from text to float
preprocessHeadings = ["Student ID","Proj Level","Term"]   #these are the headings of columns that are floats and need to be made into floats

macroLocation = cdLocation + "\\excel\\intToFloat.xlsm" #"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ change to make it dynamic"""

xl = win32com.client.Dispatch("Excel.Application")    #accesses the excel application
xl.Visible = 1

wbList = []

for i in range(len(filesList)):
    wbList.append(0)
    wbList[i] = xl.Workbooks.Open(filesList[i]) #open all the workbooks that need to be changed

    preprocessHeadingsLocation = dbFormat.findHeadingsList(preprocessHeadings,sheetAddress[i])
    #this only uses one set of table headings so if the table heading columns are different, there will be   problem

    for j in range(len(preprocessHeadingsLocation)):
        preprocessHeadingsLocation[j] = preprocessHeadingsLocation[j] + 1   #the table headings must be incremented by 1 so the macro below can process the correct heading

wbPre = xl.Workbooks.Open(macroLocation)              #open the workbook containing the macro

for k in range(len(preprocessHeadingsLocation)):    #change every column effected heading in each excel workbook
    #print preprocessHeadingsLocation[k]
    xl.Application.Run("makeTexttoFloat",preprocessHeadingsLocation[k])

for i in range(len(filesList)):
    wbList[i].Save()
    wbList[i].Close()   #close and save all the workbooks that were changed

wbPre.Save()            #close and save the excel workbook with macros
wbPre.Close(True)

xl.Application.Quit()   #killing the dispatch
xl.Visible = 0            #need to make it not visible
del (xl)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Create Table Headings

#students table
#determining headings from excel and making into table headings for sql [hardcoded but will make into dropdown input for UI]

studentTableHeadings = ["Student ID","Program","Proj Level","Plan"]
studentDataTypes = ["INTEGER NOT NULL UNIQUE","TEXT NOT NULL","INTEGER NOT NULL","TEXT NOT NULL"]    #where student_id is a unique field
maxCourses = 10    #number of courses that can be enrolled in (should be 5 for A&S for one term, 10 for a year)<<<LOOK INTO IT

#c.execute("DROP TABLE students")
if checkTableExist("students") is False:
    

    studentSQLHeadings = dbFormat.generateHeading(sheetAddress[0],studentTableHeadings,studentDataTypes)

    studentSQLHeadings = studentSQLHeadings + ", plan2 TEXT, plan3 TEXT"  #amend the headings to add the second plan column (for double majors)

    c.execute("CREATE TABLE students(stud_id INTEGER PRIMARY KEY," + studentSQLHeadings + ")")

    for i in range(maxCourses):
        c.execute("ALTER TABLE students ADD COLUMN course" + str(i + 1) + " INTEGER REFERENCES courses(course_id);")

#course table
courseTableHeadings = ["Subject","Catalog Number","TERM"]    #catalog number must be null because of suffix letters e.g. PHYG 214A
courseDataTypes = ["TEXT NOT NULL","TEXT NOT NULL","INTEGER NOT NULL"]
#c.execute("DROP TABLE courses;")
if checkTableExist("courses") is False:
    
    headingsLocation = []
    for i in range (len(courseTableHeadings)):
        headingsLocation.append(dbFormat.findCol(sheetAddress[0],courseTableHeadings[i]))   #headingsLocation are found in order of courseTableHeadings, not actual order on sheet

    courseSQLHeadings = dbFormat.generateHeading(sheetAddress[0],courseTableHeadings,courseDataTypes)
    #print courseTableHeadings
    #print courseSQLHeadings

    c.execute("CREATE TABLE courses(course_id INTEGER PRIMARY KEY," + courseSQLHeadings + ")")

###enrollments table
##
##enrollmentsHeadings=["stud_id","course_id"]
##if checkTableExist("enrollments") is False:
##
##    dataTypes=["INT","INT"]
##    foreignKeyHeadingData=", FOREIGN KEY (stud_id) REFERENCES students(stud_id) ON DELETE CASCADE, FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE"
##
##    enrollmentsSQLHeadings=generateHeadingNoExcel(enrollmentsHeadings,dataTypes)
##
##    enrollmentsSQLHeadings=enrollmentsSQLHeadings+foreignKeyHeadingData
##
##
##    c.execute("CREATE TABLE enrollments(enrollments_id INTEGER PRIMARY KEY,"+enrollmentsSQLHeadings+")")

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Pulling student data

''' Each student list from a workbook is appended to the master student list (studentLists).
    Thus, each item in that array is an array itself, making studentLists a multi-dimensional
    array.
    A tuple in the list courseLists has just the information about the course from a particular
    workbook. It is a one-dimensional array.
    A list in studentList will correspond to a tuple in courseList when the index of the two lists
    are the same. e.g. studentLists[2] will correspond to courseLists[2]
'''


studentTableHeadings = ["Student ID","Program","Proj Level","Plan"]     #restate because some function above messes with it
courseTableHeadings = ["Subject","Catalog Number","Term"]

studentLists = []
courseLists = []
courseNames = []

for i in range(len(sheetAddress)):
    courseLists.append(getCourseInfo(courseTableHeadings,sheetAddress[i]))
    courseNames.append(courseLists[i].concatenateCourseCode())

c.execute("ALTER TABLE courses ADD course_code TEXT;")  #adding the column with the concatenateCourseCoded course code
for i in range(len(sheetAddress)):
    c.execute("INSERT INTO courses(subject, catalog_number, course_code, term) VALUES(?,?,?,?);",(courseLists[i].subject, courseLists[i].catalog, courseNames[i], courseLists[i].term))

    studentLists.append(getStudents(studentTableHeadings,sheetAddress[i]))

    for stud in studentLists[i]: #OR IGNORE will only input the record if it is unique (does not show the error message)
        c.execute("INSERT OR IGNORE INTO students (student_id, program, proj_level, plan, plan2, plan3) VALUES(?,?,?,?,?,?);",(stud.studID,stud.program,stud.proj_level,stud.plan,stud.plan2,stud.plan3))

    c.execute("SELECT course_id FROM courses WHERE course_id=(SELECT MAX(course_ID) FROM courses);") #finds the course_id of the most recently entered course list from the courses table

    #convert the tuple to an integer
    temp=c.fetchone()
    courseNum=0
    count=0
    for a in reversed(temp):
        courseNum=courseNum+a*10**count
        count=count+1

    ''' Goes through all the students in the current course list and accesses all rows from the SQL database.
     It will add the courses that a student is enrolled in.
    '''
    c.execute("SELECT * FROM students")
    val=c.fetchall()

    for stud in studentLists[i]: #goes through all the students in current course list
        for row in val: #goes through all rows of the table
            for i in reversed(range(1,maxCourses+1)): #accesses the row's course values, course 1 thru maxCourses
                if row[len(row)-i] is None and stud.studID==row[1]: #must check if the student is enrolled in the current course
                    c.execute("UPDATE students SET course"+str(maxCourses+1-i)+"=? WHERE student_id=?;",(str(courseNum),row[1]))
                    break


'''Input the credits using the entry widget (creditsInput module) and then updates the database
'''

c.execute("ALTER TABLE courses ADD credits FLOAT;")
c.execute("SELECT course_code, term FROM courses;") #grabs names of all the courses
allCourses = c.fetchall()

courseDisplayName = []

for i in range(len(allCourses)):
    #first element [i][0] is the course code, the second [i][1] is the term that the course is in
    courseDisplayName.append(allCourses[i][0] + " - Term: " + str(allCourses[i][1]))    


creditsList = creditsInput.runApp(courseDisplayName)    #initializes the entry widget to input credits data
while not checkError(creditsList):                  #do while loop that repeats until there is no more error
    errorMessageBox.runApp(creditsList)
    creditsList = creditsInput.runApp(courseDisplayName)

for credit in creditsList:
    c.execute("UPDATE courses SET credits = ?;",(credit,))      #adds to each course record the number of credits


'''Insert auxiliary tables that contain information for processing
- Unit Fees
- BIU/Formula Fee
- Program Weights

'''
#UNIT FEES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c.execute("CREATE TABLE program_info (program_id INTEGER PRIMARY KEY, program_name TEXT UNIQUE, unit_fees FLOAT);")
c.execute("SELECT DISTINCT program FROM students;")
programList = c.fetchall()

unitFeesList = feeUnitsInput.runApp(programList)
while not checkError(unitFeesList) and not len(programList) == len(unitFeesList):         #do while loop that repeats until there is no more error
    errorMessagBox.runApp(unitFeesList)
    unitFeesList = feeUnitsInput.runApp(programList)

if len(programList) == len(unitFeesList):       #double check that appropriate number of values were input    
    for i in range(len(programList)):

        val = ''.join(programList[i])       #convert the tuple to a str for the name of a program

        c.execute("INSERT INTO program_info (program_name, unit_fees) VALUES (?,?);",(val, unitFeesList[i]))


#BIU~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c.execute("CREATE TABLE constants (id INTEGER PRIMARY KEY, name TEXT, value INTEGER);")

BIUList = BIUInput.runApp()
while not checkError(BIUList) and not len(BIUList) == 1:
    errorMessageBox.runApp(BIUList)
    BIUList = BIUInput.runApp()

if len(BIUList) == 1:
    c.execute("INSERT INTO constants (name, value) VALUES (?,?);",("BIU Value", BIUList[0]))

#Formula Fees~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
c.execute("ALTER TABLE program_info ADD formula_fee FLOAT;")

formulaFeeList = formulaFeesInput.runApp(programList)
while not checkError(formulaFeeList) and not len(programList) == len(formulaFeeList):
    errorMessageBox.runApp(progWeightsList)
    formulaFeeList = formulaFeesInput.runApp(programList)

if len(programList) == len(formulaFeeList):
    for formulaFee in formulaFeeList:

        c.execute("UPDATE program_info SET formula_fee = ?;",(formulaFee,))


 #Program Weights~~~~~~~~~~~~~~~~~~~~~~~~~~
c.execute("ALTER TABLE program_info ADD program_weight FLOAT;")

progWeightsList = programWeightsInput.runApp(programList)
while not checkError(progWeightsList) and not len(programList) == len(progWeightsList):
    errorMessageBox.runApp(progWeightsList)
    progWeightsList = programWeightsInput.runApp(programList)

if len(programList) == len(progWeightsList):
    for progWeight in progWeightsList:

        c.execute("UPDATE program_info SET program_weight = ?;",(progWeight,))


conn.commit()
conn.close()