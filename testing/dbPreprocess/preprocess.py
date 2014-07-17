#------------------------------------------------------------------------------
# Name:        preprocess_v1
# Purpose:      create a database by extracting data from a spreadsheet
#               extract the data and process it into the SQLite database
#               This processes a SINGLE spreadsheet and obtains the necessary
#               info for each student, and also finds the current course code
# Author:      DBMS
#
# Created:     12/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#------------------------------------------------------------------------------
import os
import sqlite3
import xlrd
import xlwt
import string
import types

class Student:
    def __init__(self):#,studID,program,proj_level,plan1,plan2,total_credits):
        '''self.studID=studID
        self.program=program
        self.proj_level=proj_level
        self.plan1=plan1
        self.plan2=plan2
        self.total_credits=total_credits'''
        pass

    def printValues(self):  #output the attributes of a student
        print str(self.studID)+" ,"+self.program+" ,"+str(self.proj_level)+" ,"+self.plan

    def convert(self):  #convert student ID from float into int
        self.studID=int(self.studID)
        self.proj_level=int(self.proj_level)
        #self.plan=unicode(self.plan)

class Course:
    def __init__(self):#subject, catalog_number, credits, term
        pass

    def printCourse(self):
        print str(self.subject)+" "+str(self.catalog_number)+" ,"+str(self.credits)

def findImproperStudent(arrlist=[],*array): #finds the index for headings and whitespaces (where there should be student ID's)
    pop=[]
    for i in range(len(arrlist)-1):
        if type(arrlist[i].studID) is not float:
            pop.append(i)
    return pop

def findDuplicate(arrlist=[],*array):   #finds the index of student objects that are duplicates
    pop=[]
    for i in range(len(arrlist)-1):
        if arrlist[i].studID==arrlist[i+1].studID:  #checks if the next row has the same student ID
            pop.append(i) #must pop the second occurence
    return pop

def findCol(sheetAddress,heading):  #finds the column number of the column that has the 'heading'

    for col in range(sheetAddress.ncols):
        if sheetAddress.cell(1,col).value==heading:
            return col

def generateHeading(sheetAddress,colHeadings,headingTypes): #creates a heading used for the SQL table from the input headings
    headingsLoc=[]

    for i in range(len(colHeadings)):
        headingsLoc.append(findCol(sheetAddress,colHeadings[i]))

        colHeadings[i]=colHeadings[i].replace(' ','_')  #make a heading such as "Student ID" into "student_id"
        colHeadings[i]=colHeadings[i].lower()
        colHeadings[i]=str(colHeadings[i]+" "+headingTypes[i])

    colHeadings=", ".join(colHeadings) #forming one string for the sql table heading
    return colHeadings

def generateHeadingNoExcel(colHeadings,headingTypes):
    for i in range(len(colHeadings)):
        colHeadings[i]=colHeadings[i].replace(' ','_')  #make a heading such as "Student ID" into "student_id"
        colHeadings[i]=colHeadings[i].lower()
        colHeadings[i]=str(colHeadings[i]+" "+headingTypes[i])

    colHeadings=", ".join(colHeadings) #forming one string for the sql table heading
    return colHeadings

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#open database stuff
cdLocation=os.getcwd()
#print cdLocation
dbLocation=cdLocation+"test.db"



conn=sqlite3.connect(dbLocation)
c=conn.cursor()

c.execute("PRAGMA foreign_keys=ON;")    #enables foreign keys

#open workbook for reading (xlrd)

wbData=xlrd.open_workbook(cdLocation+'\QU_RG_CLASS_LIST_GRADE_476707713 (2).xls')

sheetAddress=wbData.sheet_by_index(0)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#determining headings from excel and making into table headings for sql [hardcoded but will make into dropdown input for UI]
studentTableHeadings=["Student ID","Program","Proj Level","Plan"]
dataTypes=["INTEGER NOT NULL UNIQUE","TEXT NOT NULL","INTEGER NOT NULL","TEXT NOT NULL"]    #where student_id is a unique field


headingsLocation=[]
for i in range (len(studentTableHeadings)):
    #print (findCol(sheetAddress,studentTableHeadings[i]))
    headingsLocation.append(findCol(sheetAddress,studentTableHeadings[i]))

studentSQLHeadings=generateHeading(sheetAddress,studentTableHeadings,dataTypes)

studentSQLHeadings=studentSQLHeadings+", plan2 TEXT, plan3 TEXT"  #amend the headings to add the second plan column (for double majors)

#create the array of students
studList=[Student() for i in range(sheetAddress.nrows)]

for row in range(sheetAddress.nrows):
    values=[]
    for dataCol in headingsLocation:
        values.append(sheetAddress.cell(row,dataCol).value)
    studList[row].studID=(values[0])
    studList[row].program=values[1]
    studList[row].proj_level=(values[2])
    studList[row].plan=values[3]
    studList[row].plan2=""
    studList[row].plan3=""

#delete headings/whitespace AND duplicates
popRows=[]
#finds the headings and whitespaces
popRows.extend(findImproperStudent(studList))

#finds the duplicates and adds the indices to the popRows list
for i in findDuplicate(studList):
    studList[i+1].plan2=studList[i].plan    #before the duplicate is popped, the second plan is added to the data row

popRows.extend(findDuplicate(studList))

#when iterating in reverse, the wrong things do not get popped off the list
for i in reversed(popRows):
    studList.pop(i)

popRows=[]

#finalize input data
for i in range(len(studList)):
    studList[i].convert()
    #studList[i].printValues()

for i in findDuplicate(studList):   #finds the duplicates again (accounts for con ed, who have BED + double major for their plans, 3 rows)
    studList[i+1].plan3=studList[i].plan

popRows.extend(findDuplicate(studList))
#print popRows

for i in reversed(popRows): #pop the triples
    studList.pop(i)

#c.execute("DROP TABLE students;")
c.execute("CREATE TABLE students(stud_id INTEGER PRIMARY KEY,"+studentSQLHeadings+")")

for i in range(len(studList)):
    c.execute("INSERT INTO students (student_id,program,proj_level,plan,plan2,plan3) VALUES(?,?,?,?,?,?);",(studList[i].studID,studList[i].program,studList[i].proj_level,studList[i].plan,studList[i].plan2,studList[i].plan3))

conn.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#get the course code and information
courseTableHeadings=["Subject","Catalog Number"]
dataTypes=["TEXT NOT NULL","INTEGER NOT NULL"]

headingsLocation=[]
for i in range (len(courseTableHeadings)):
    headingsLocation.append(findCol(sheetAddress,courseTableHeadings[i]))

courseSQLHeadings=generateHeading(sheetAddress,courseTableHeadings,dataTypes)

courseInfo=Course()

values=[]
for dataCol in headingsLocation:
    values.append(sheetAddress.cell(2,dataCol).value)
courseInfo.subject=(values[0])
courseInfo.catalog=values[1]

#c.execute("DROP TABLE courses")
c.execute("CREATE TABLE courses(course_id INTEGER PRIMARY KEY,"+courseSQLHeadings+")")

c.execute("INSERT INTO courses (subject, catalog_number) VALUES(?,?);",(courseInfo.subject,courseInfo.catalog))

conn.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#add course foreign key to student table

c.execute("SELECT * FROM students ORDER BY student_id;")
newList=c.fetchall()

maxCourses=7

for i in range(maxCourses):
    c.execute("ALTER TABLE students ADD COLUMN course"+str(i+1)+" INTEGER REFERENCES courses(course_id);")

c.execute("SELECT course_id FROM courses WHERE course_id=(SELECT MAX(course_ID) FROM courses);")

temp=c.fetchone()   #convert the tuple to an integer
courseNum=0
count=0
for a in reversed(temp):
    courseNum=courseNum+a*10**count
    count=count+1

for i in range(len(studList)): #LOOK OUT WHEN USING MORE THAN 1 SPREADSHEET
    pass
    #adds the current course number to the student record without deleting past course entries
    #when course2 is not null, but course 1 is filled, the course2 is written to
##    c.execute('''UPDATE students
##                SET course5=CASE
##                WHEN course1 IS NOT NULL
##                AND course2 IS NOT NULL
##                AND course3 IS NOT NULL
##                AND course4 IS NOT NULL
##                AND course5 IS NULL THEN ? END''',(str(courseNum)))
##    c.execute('''UPDATE students
##                SET course4=CASE
##                WHEN course1 IS NOT NULL
##                AND course2 IS NOT NULL
##                AND course3 IS NOT NULL
##                AND course4 IS NULL
##                AND course5 IS NULL THEN ? END''',(str(courseNum)))
##    c.execute('''UPDATE students
##                SET course3=CASE
##                WHEN course1 IS NOT NULL
##                AND course2 IS NOT NULL
##                AND course3 IS NULL
##                AND course4 IS NULL
##                AND course5 IS NULL THEN ? END''',(str(courseNum)))
##    c.execute('''UPDATE students
##                SET course2=CASE
##                WHEN course1 IS NOT NULL
##                AND course2 IS NULL
##                AND course3 IS NULL
##                AND course4 IS NULL
##                AND course5 IS NULL THEN ? END''',(str(courseNum)))
##    c.execute('''UPDATE students
##                SET course1=CASE
##                WHEN course1 IS NULL
##                AND course2 IS NULL
##                AND course3 IS NULL
##                AND course4 IS NULL
##                AND course5 IS NULL THEN ? END''',(str(courseNum)))

##    c.execute('''UPDATE students
##                CASE students.course1
##                WHEN NULL THEN students.course1=
##                WHEN NOT NULL THEN
##                    CASE students.course2
##                    WHEN NULL THEN students.course2=
##                    WHEN NOT NULL THEN
##                        CASE students.course3
##                        WHEN NULL THEN students.course3=
##                        WHEN NOT NULL THEN
##                            CASE students.course4
##                            WHEN NULL THEN students.course4=
##                            WHEN NOT NULL THEN
##                                CASE students.course5
##                                WHEN NULL THEN students.course5=
##                                WHEN NOT NULL THEN
##                                    CASE students.course6
##                                    WHEN NULL THEN students.course6=
##                                    END''')

c.execute('''SELECT * FROM students''')
val=c.fetchall()

for stud in studList:   #goes through all the students in current course list
    for row in val: #goes through all rows of the table
        for i in reversed(range(1,maxCourses+1)):   #accesses the row's course values, course 1 thru maxCourses
            if row[len(row)-i] is None and stud.studID==row[1]: #must check if the student is enrolled in the current course
                #print str(stud.studID)+" , "+str(row[1])
                c.execute('''UPDATE students SET course'''+str(maxCourses+1-i)+'''=? WHERE student_id=?;''',(str(courseNum),row[1]))
                break

##c.execute('''SELECT * FROM students''')
##temp=c.fetchone()
##print temp

conn.commit()

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#join tables to create enrollment
a=[]
b=[]
c.execute("SELECT stud_id,course_id FROM students JOIN courses ON students.course1=courses.course_id;")

for i in range(5):
    temp1,temp2=c.fetchone()
    a.append(temp1)
    b.append(temp2)
    #print (c.fetchone())
##print a[2]
##print b[2]



enrollmentsHeadings=["stud_id","course_id"]
dataTypes=["INT","INT"]

enrollmentsSQLHeadings=generateHeadingNoExcel(enrollmentsHeadings,dataTypes)

enrollmentsSQLHeadings=enrollmentsSQLHeadings+", FOREIGN KEY (stud_id) REFERENCES students(stud_id) ON DELETE CASCADE, FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE"


c.execute("CREATE TABLE enrollments(enrollments_id INTEGER PRIMARY KEY,"+enrollmentsSQLHeadings+")")

c.execute("INSERT INTO enrollments(stud_id,course_id) SELECT stud_id,course_id FROM students JOIN courses ON students.course1=courses.course_id;")

conn.commit()

conn.close()

