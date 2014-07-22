#-------------------------------------------------------------------------------
# Name:        preprocess_v4
# Purpose:      create a database by extracting data from a spreadsheet
#               extract the data and process it into the SQLite database
#               This extracts the data from multiple spreadsheets
#
#               preprocesses the excel workbooks to make things into floats (relies on win32com.client which isn't working)
#               
#               UI tkinter widgets will ask for inputs from the user for variables (BIU, program weights, etc.)
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

import time
import sqlite3  #SQLite API
import xlrd #reading xls files
import xlwt #writing xls files
import string
import types
import win32com.client  #for executing excel macros @@@@@@@@@@@@not installed for some reason

import extractData      #various functions used, stores location of DATABASE
import studentProcessing        #module that deletes whitespace, double/triple majors when processing each spreadsheet
import dbFormat                 #formats the tables for the database

import UI.creditsInput    #UI box for inputting credits
import UI.feeUnitsInput       #UI box for inputting unit fees
import UI.programWeightsInput      #asks for program weights, returns list  (also asks for 1st year Arts and Sci)
import UI.formulaFeesInput     #asks for formula fees, returns list
import UI.BIUInput             #asks for BIU and returns a list with 1 element
import UI.normalUnitsInput
import UI.errorMessageBox  #UI that displays the error

import dateTimeOutput
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

def checkTableExist(curDB, tableName):
    '''Checks if the table with "tableName" exists
    Returns True if it exists and False if it doesn't exist
    '''
    curDB.execute('''SELECT CASE
                WHEN tbl_name = ? THEN 1     
                ELSE 0
                END
                FROM sqlite_master
                WHERE tbl_name = ? AND type = "table"''',(str(tableName),str(tableName)))

    temp = curDB.fetchone()

    if temp == (1,):      
        return True
    else:
        return False

def getStudents(headingsNeeded, currentSheet):
    '''Returns a list of student objects, with each object containing 
        student id, program, year, plan (including double and triple majors)
        
        Also will removes duplicates (who result from double majors) when 
        parsing from the excel spreadsheet. 

        A single student will show up twice if he or she is a double major, 
        but the function will pop off the duplicate and append the double major 
        plan to the appropriate student object
    '''

    headingsLocation = []

    for i in range(len(headingsNeeded)):
        headingsLocation.append(dbFormat.findCol(currentSheet,headingsNeeded[i]))

    studList = [Student() for i in range(currentSheet.nrows)]         #create the array of students

    print str(currentSheet) + " " + str(currentSheet.nrows) #@@@@@@@@@@@@@@@@@@@@@@

    for row in range(currentSheet.nrows):
        '''parse the data of each excel row into a Student object, which is in the array'''
        values = []
        for dataCol in headingsLocation:
            values.append(currentSheet.cell(row,dataCol).value)

        studList[row].studID = (values[0])
        studList[row].program = values[1]
        studList[row].proj_level = (values[2])
        studList[row].plan = values[3]
        studList[row].plan2 = ""
        studList[row].plan3 = ""

    studList = studentProcessing.removeBEDProg(studList)    #prevents BED from being the plan

    popRows = []

    popRows.extend(studentProcessing.findImproperStudent(studList))   #finds the headings and whitespaces and flags the index
    for i in studentProcessing.findTriple(studList):
       '''finds the triples (accounts for con ed, who MAY have B.ED + double major for their plans, 3 rows)'''
       studList[i + 2].plan3 = studList[i].plan
    popRows.extend(studentProcessing.findTriple(studList))            #flags the index for triples


    print popRows
    for i in reversed(popRows):                     #when iterating in reverse, the wrong things do not get popped off the list
        studList.pop(i)                             #pop off headings/whitespaces and triples

    popRows = []                                      #resets the list so we can add duplicate indexes

    for stud in studList:
        print str(stud.studID) + "   " +stud.program
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

        Will return the subject code (e.g. ANAT), catalog number (e.g. 215) and term (e.g. 2135)
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

def checkWorkBookValues(currentSheet):
    '''FOR ERROR CHECKING REMOVE @@@@@@@@@@@@@@@@@@@@@@@
    '''
    studList = [Student() for i in range(currentSheet.nrows)]         #create the array of students

    print str(currentSheet) + " " + str(currentSheet.nrows) #@@@@@@@@@@@@@@@@@@@@@@

    for row in range(currentSheet.nrows):
        '''parse the data of each excel row into a Student object, which is in the array'''
        values = []

        values.append(currentSheet.cell(row,6).value)

        print type(values[0])


def checkError(funcOutput):     #returns false is there is an error, returns true if no error exists
    '''Checks the output of the function to see if an error message was returned
    '''

    if 'Error' in funcOutput:       #sees if the output returns an error
        return False
    else:                       #output does not return an error
        return True

def main():
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
    """Initialize the Excel workbook connections for reading using xlrd module
        Find all xls files and then store the location and addresses of all of them
    """
    excelExtension = "xls"
    filesList = findFiles(rawDataLocation,excelExtension)

    wbData = []
    sheetAddress = []
    for i in range(len(filesList)):
        wbData.append(xlrd.open_workbook(filesList[i]))
        sheetAddress.append(wbData[i].sheet_by_index(0)) #will access and store the location of the FIRST sheet in each workbook

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Preprocess the excel columns from text to float
    '''Use Excel Macros and control it through coms with win32com.client
    '''
    preprocessHeadings = ["Student ID","Proj Level","Term"]   #these are the headings of columns that are floats and need to be made into floats

    macroLocation = cdLocation + "\\excelMacro\\intToFloat.xlsm" #"""@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ change to make it dynamic"""

    xl = win32com.client.Dispatch("Excel.Application")    #accesses the excel application
    xl.Visible = 1

    wbPre = xl.Workbooks.Open(macroLocation)              #open the workbook containing the macro

    wbList = []

    for i in range(len(filesList)):


        wbList.append(0)
        #wbList[i] = xl.Workbooks.Open(filesList[i]) #open all the workbooks that need to be changed

        preprocessHeadingsLocation = dbFormat.findHeadingsList(preprocessHeadings,sheetAddress[i])
        #this only uses one set of table headings so if the table heading columns are different, there will be   problem

        for j in range(len(preprocessHeadingsLocation)):

            preprocessHeadingsLocation[j] = preprocessHeadingsLocation[j] + 1   #the table headings must be incremented by 1 so the macro below can process the correct heading

            xl.Application.Run("makeTexttoFloat",preprocessHeadingsLocation[j],filesList[i])


    wbPre.Save()            #close and save the excel workbook with macros
    wbPre.Close(True)

    xl.Application.Quit()   #killing the dispatch
    xl.Visible = 0            #need to make it not visible
    del (xl)

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Reopens the files using XLRD again (after being updated using macro)
    wbData = []
    sheetAddress = []
    for i in range(len(filesList)):
        wbData.append(xlrd.open_workbook(filesList[i]))
        sheetAddress.append(wbData[i].sheet_by_index(0)) #will access and store the location of the FIRST sheet in each workbook

    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #Create Table Headings

    #students table
    #determining headings from excel and making into table headings for sql [hardcoded but will make into dropdown input for UI]

    studentTableHeadings = ["Student ID","Program","Proj Level","Plan"]
    studentDataTypes = ["INTEGER NOT NULL UNIQUE","TEXT NOT NULL","INTEGER NOT NULL","TEXT NOT NULL"]    #where student_id is a unique field
    maxCourses = 10    #number of courses that can be enrolled in (should be 5 for A&S for one term, 10 for a year)<<<LOOK INTO IT

    #c.execute("DROP TABLE students")
    if checkTableExist(c,"students") is False:
        
        studentSQLHeadings = dbFormat.generateHeading(sheetAddress[0],studentTableHeadings,studentDataTypes)

        studentSQLHeadings = studentSQLHeadings + ", plan2 TEXT, plan3 TEXT"  #amend the headings to add the second plan column (for double majors)

        c.execute("CREATE TABLE students(stud_id INTEGER PRIMARY KEY," + studentSQLHeadings + ")")

        for i in range(maxCourses):
            c.execute("ALTER TABLE students ADD COLUMN course" + str(i + 1) + " INTEGER REFERENCES courses(course_id);")

    #course table
    courseTableHeadings = ["Subject","Catalog Number","TERM"]    #catalog number must be null because of suffix letters e.g. PHYG 214A
    courseDataTypes = ["TEXT NOT NULL","TEXT NOT NULL","INTEGER NOT NULL"]
    #c.execute("DROP TABLE courses;")
    if checkTableExist(c,"courses") is False:
        
        headingsLocation = []
        for i in range (len(courseTableHeadings)):
            headingsLocation.append(dbFormat.findCol(sheetAddress[0],courseTableHeadings[i]))   #headingsLocation are found in order of courseTableHeadings, not actual order on sheet

        courseSQLHeadings = dbFormat.generateHeading(sheetAddress[0],courseTableHeadings,courseDataTypes)

        c.execute("CREATE TABLE courses(course_id INTEGER PRIMARY KEY," + courseSQLHeadings + ")")

    #time stamp table
    if checkTableExist(c,"timeRecord") is False:

        c.execute('''CREATE TABLE timeRecord 
                    (
                        time_id INTEGER PRIMARY KEY, 
                        timeStam TEXT
                    );''')

        c.execute('''INSERT INTO timeRecord (timeStam) VALUES (?);''',(dateTimeOutput.pythonTime(),))

    #info stored about programs, used to calculate tuition and grants
    if checkTableExist(c,"program_info") is False:

        c.execute('''CREATE TABLE program_info 
                    (
                        program_id INTEGER PRIMARY KEY, 
                        program_name TEXT UNIQUE, 
                        unit_fees FLOAT, 
                        formula_fees FLOAT, 
                        program_weight FLOAT,
                        normal_units INTEGER
                    );''')

    #storing values like BIU
    if checkTableExist(c,"constants") is False:

        c.execute('''CREATE TABLE constants 
                    (
                        id INTEGER PRIMARY KEY, 
                        name TEXT, 
                        value INTEGER
                    );''')


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
        c.execute('''INSERT INTO courses(subject, catalog_number, course_code, term) 
                    VALUES(?,?,?,?);''',(courseLists[i].subject, courseLists[i].catalog, courseNames[i], courseLists[i].term))

        studentLists.append(getStudents(studentTableHeadings,sheetAddress[i]))

        for stud in studentLists[i]: #OR IGNORE will only input the record if it is unique (does not show the error message)
            c.execute('''INSERT OR IGNORE INTO students (student_id, program, proj_level, plan, plan2, plan3) 
                        VALUES(?,?,?,?,?,?);''',(stud.studID,stud.program,stud.proj_level,stud.plan,stud.plan2,stud.plan3))

        c.execute('''SELECT course_id 
                    FROM courses 
                    WHERE course_id=(SELECT MAX(course_ID) 
                                    FROM courses);''') 
                    #finds the course_id of the most recently entered course list from the courses table

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

    c.execute('''UPDATE timeRecord 
                SET timeStam = ? 
                WHERE time_id = 1;''', (dateTimeOutput.pythonTime(),))     #updates the time stamp for the table after the spreadsheets were pulled

    '''Input the credits using the entry widget (creditsInput module) and then updates the database
    '''

    c.execute("ALTER TABLE courses ADD credits FLOAT;")
    c.execute('''SELECT course_code, term FROM courses;''') #grabs names of all the courses
    allCourses = c.fetchall()

    courseDisplayName = []

    for i in range(len(allCourses)):
        #first element [i][0] is the course code, the second [i][1] is the term that the course is in
        courseDisplayName.append(allCourses[i][0] + " - Term: " + str(allCourses[i][1]))    


    creditsList = UI.creditsInput.runApp(courseDisplayName)    #initializes the entry widget to input credits data
    while not checkError(creditsList):                  #do while loop that repeats until there is no more error
        UI.errorMessageBox.runApp(creditsList)
        creditsList = UI.creditsInput.runApp(courseDisplayName)

    for credit in creditsList:
        c.execute('''UPDATE courses SET credits = ?;''',(credit,))      #adds to each course record the number of credits


    '''Insert auxiliary tables that contain information for processing
    - Unit Fees
    - BIU/Formula Fee
    - Program Weights

    '''
    #UNIT FEES~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    c.execute("SELECT DISTINCT program FROM students;")
    programList = c.fetchall()
    print programList

    unitFeesList = UI.feeUnitsInput.runApp(programList)
    while not checkError(unitFeesList) and not len(programList) == len(unitFeesList):         #do while loop that repeats until there is no more error
        UI.errorMessageBox.runApp(unitFeesList)
        unitFeesList = UI.feeUnitsInput.runApp(programList)

    if len(programList) == len(unitFeesList):       #double check that appropriate number of values were input    
        for i in range(len(programList)):

            val = ''.join(programList[i])       #convert the tuple to a str for the name of a program

            c.execute("INSERT INTO program_info (program_name, unit_fees) VALUES (?,?);",(val, unitFeesList[i]))

    #BIU~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    BIUList = UI.BIUInput.runApp()
    while not checkError(BIUList) and not len(BIUList) == 1:
        UI.errorMessageBox.runApp(BIUList)
        BIUList = UI.BIUInput.runApp()

    if len(BIUList) == 1:
        c.execute("INSERT INTO constants (name, value) VALUES (?,?);",("BIU Value", BIUList[0]))

    #Formula Fees~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    formulaFeeList = UI.formulaFeesInput.runApp(programList)
    while not checkError(formulaFeeList) and not len(programList) == len(formulaFeeList):
        UI.errorMessageBox.runApp(formulaFeeList)
        formulaFeeList = UI.formulaFeesInput.runApp(programList)

    if len(programList) == len(formulaFeeList):
        for formulaFee in formulaFeeList:

            c.execute("UPDATE program_info SET formula_fees = ?;",(formulaFee,))

    #Number of normal units~~~~~~~~~~~~~~~~~~~~~

    normalUnitsList = UI.normalUnitsInput.runApp(programList)
    while not checkError(normalUnitsList) and not len(programList) == len(normalUnitsList):
        UI.errorMessageBox.runApp(normalUnitsList)
        normalUnitsList = UI.normalUnitsInput.runApp(progromList)

    if len(programList) == len(normalUnitsList):
        for numOfUnits in normalUnitsList:

            c.execute("UPDATE program_info SET normal_units = ?;", (numOfUnits,))

    #Program Weights~~~~~~~~~~~~~~~~~~~~~~~~~~
    programList.append("1st Year Arts")     #must consider program weights are different for 1st year
    programList.append("1st Year Science")

    progWeightsList = UI.programWeightsInput.runApp(programList)
    while not checkError(progWeightsList) and not len(programList) == len(progWeightsList):
        UI.errorMessageBox.runApp(progWeightsList)
        progWeightsList = UI.programWeightsInput.runApp(programList)

    if len(programList) == len(progWeightsList):
        for progWeight in progWeightsList[:2]:

            c.execute("UPDATE program_info SET program_weight = ?;",(progWeight,))

        for i in range(len(progWeightsList)-2,len(progWeightsList)):

            c.execute("INSERT INTO program_info(program_name, program_weight) VALUES (?,?);",(programList[i], progWeightsList[i],))

            

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()