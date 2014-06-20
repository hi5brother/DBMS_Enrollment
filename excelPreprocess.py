#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:      reformats the class lists with multiple sections into one excel spreadsheet
#
# Author:      DBMS
#
# Created:     20/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os
import xlrd
import xlwt
from xlutils.copy import copy
#import win32com.client

from dbFormat import findCol

def findFiles(location, extension):

    ''' #Searches a location for all files that have a specific extension
        #Used to return all the excel workbooks (xls) locations to the main function
    '''
    workbooksList=[]    #delcaration, stores the file locations of all the workbooks

    for filename in os.listdir(location): #goes through every file in the folder
        if filename[-3:]==extension:
            workbooksList.append(location+"\\"+filename)  #adds the file if the last 3 char are "xls"

    return workbooksList

def locateHeadings(headingsList,sheetAddress):

    '''Generate the column numbers holding the headings
    '''
    headingsLocation=[]
    for heading in headingsList:
        headingsLocation.append(findCol(sheetAddress,heading))

    return headingsLocation

def copyData(fileLocation,sheetAddress):

    '''Copies all cells from the fileLocation workbook and outputs the cells
    '''

    oldWB=xlrd.open_workbook(fileLocation,on_demand=True)

    numRowsOldWB=sheetAddress.nrows-1   #dimensions of the old workbook
    numCellsOldWB=sheetAddress.ncols 


    cellData=[[0 for x in xrange(numCellsOldWB)]for x in xrange(numRowsOldWB)]  #multiD array that will store all the data

    curr_row=-1
    while curr_row<numRowsOldWB:        #incrementing through the rows of the WB
        curr_row+=1

        row = sheetAddress.row(curr_row)

        curr_cell=-1
        while curr_cell<numCellsOldWB:      #incrementing through the columns of a row
            curr_cell+=1

            cellData[curr_row-1][curr_cell-1]=sheetAddress.cell_value(curr_row,curr_cell-1) 

    return cellData



def recreateWB(fileLocation,sheetAddress,cellData):
    '''Copies the one workbook using xlutils 
    then adds onto the new workbook using the data copied using copyData
    and currently saves as "1.xls"
    '''

    wb=xlrd.open_workbook(fileLocation,on_demand=True)  #xlrd open workbook
    numRows=sheetAddress.nrows

    newWB=xlwt.Workbook()   #xlwt open workbook
    sheet1=newWB.add_sheet("sheet1",cell_overwrite_ok=True)
    newWB=copy(wb)

    for i in range(len(cellData[:][:])):    #iterate through the rows of the copied data
        for j in range(len(cellData[1][:])):
            newWB.get_sheet(0).write(i+numRows,j,cellData[i][j])    #copies the new data to the end of the old data

    newWB.save("1.xls")



def checkCourseCode(filesList,sheetAddressList):

    headings=["Subject","Catalog Number","Term"]   #these are the headings that need to be searched for
    courseCodes=[[] for x in xrange(len(headings))] #multiD array that stores subject, catalog, and term for each course


    for i in range(len(sheetAddressList)):
        xlrd.open_workbook(filesList[i],on_demand=True)
        headingsLocation=locateHeadings(headings,sheetAddressList[i])

        tempValues=[]
        for dataCol in headingsLocation:    
            if type(sheetAddressList[i].cell(2,dataCol).value) is float:
                courseCodes[i].append(int(sheetAddressList[i].cell(2,dataCol).value))   #converts the term float value into an int
            else:
                courseCodes[i].append(sheetAddressList[i].cell(2,dataCol).value) 
    
    for i in range(len(sheetAddressList)):
        for j in range(len(sheetAddressList)-1):
            if courseCodes[i] == courseCodes[j] and i != j:
                print "DUPLICATE"+str(i)
            



def main():
    progDirectory=os.getcwd()
    dataLocation=progDirectory+"\\data"
    excelExtension="xls"

    filesList=findFiles(dataLocation,excelExtension)
 
    wbData=[]
    sheetAddress=[]

    for i in range(len(filesList)):
        wbData.append(xlrd.open_workbook(filesList[i]))
        sheetAddress.append(wbData[i].sheet_by_index(0))

    try:
        os.remove(progDirectory+"\\1.xls")
    except WindowsError:
        print "can't find"
    else: 
        pass

    recreateWB(filesList[0],sheetAddress[0],copyData(filesList[0],sheetAddress[0]))

    

if __name__ == '__main__':
        main()
