#-------------------------------------------------------------------------------
# Name:        dbFormat
# Purpose:      has functions called from preprocess.py that are used to create and use the sql tables
#               some functions are used to create sql tables based on the excel info
#
# Author:      DBMS
#
# Created:     19/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import sqlite3

def findCol(sheetAddress,heading):
    '''Finds the column number of the column that has the specific 'heading'
    '''

    for col in range(sheetAddress.ncols):
        if sheetAddress.cell(1,col).value==heading:
            return col

def findHeadingsList(headingsNeeded, currentSheet):
    '''Returns the column locations of all the headings for a specific table
    '''
    headingsLocation=[]
    for i in range(len(headingsNeeded)):
        headingsLocation.append(findCol(currentSheet,headingsNeeded[i]))
    return headingsLocation

def generateHeading(sheetAddress,colHeadings,headingTypes):
    '''Using the headings (eg. Student ID, Proj Level) and the associated data types
        (eg. INTEGER UNIQUE NOT NULL, INTEGER NOT NULL) to declare the SQL table,
        a signle string is generated containing all the necessary information to
        CREATE TABLE
        This function uses the headings directly from an Excel workbook
    '''

    for i in range(len(colHeadings)):

        colHeadings[i]=colHeadings[i].replace(' ','_')  #make a heading such as "Student ID" into "student_id"
        colHeadings[i]=colHeadings[i].lower()
        colHeadings[i]=str(colHeadings[i]+" "+headingTypes[i])

    colHeadings=", ".join(colHeadings) #forming one string for the sql table heading
    return colHeadings

def generateHeadingNoExcel(colHeadings,headingTypes):
    '''Using the headings (eg. Student ID, Proj Level) and the associated data types
    (eg. INTEGER UNIQUE NOT NULL, INTEGER NOT NULL) to declare the SQL table,
    a signle string is generated containing all the necessary information to
    CREATE TABLE
    The headings are NOT generated from an Excel workbook
    '''
    for i in range(len(colHeadings)):
        colHeadings[i]=colHeadings[i].replace(' ','_')  #make a heading such as "Student ID" into "student_id"
        colHeadings[i]=colHeadings[i].lower()
        colHeadings[i]=str(colHeadings[i]+" "+headingTypes[i])

    colHeadings=", ".join(colHeadings) #forming one string for the sql table heading
    return colHeadings

def checkTableExist(tableName):
    '''Checks if the table with "tableName" exists
    Returns True if it exists and False if it doesn't exist
    '''

    c.execute('''SELECT CASE
                WHEN tbl_name = ? 
                THEN 1
                ELSE 0
                END
                FROM sqlite_master
                WHERE tbl_name = ? AND type = "table"''',(str(tableName),str(tableName)))

    temp = c.fetchone()

    if temp == (1,):
        return True
    else:
        return False

def checkColumnExist(c,columnName, tableName):
    '''Checks if the column exists in a table
        Returns True if it exists and False if it doesn't exist
    '''

    sqlString = "SELECT " + columnName + " FROM " + tableName
    try:
        c.execute(sqlString)

    except sqlite3.OperationalError:
        return False
    return True

# def checkRecordExist(c,record,columnName,tableName):
#     '''Checks if a record exists
#         Returns True if it exists and False if it doesn't exist
#     '''

#     sqlString = "SELECT " + columnName + " FROM " + tableName " WHERE "