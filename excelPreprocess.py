#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
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
import win32com.client

def findFiles(location, extension):

    ''' #Searches a location for all files that have a specific extension
        #Used to return all the excel workbooks (xls) locations to the main function
    '''
    workbooksList=[]    #delcaration, stores the file locations of all the workbooks

    for filename in os.listdir(location): #goes through every file in the folder
        if filename[-3:]==extension:
            workbooksList.append(location+"\\"+filename)  #adds the file if the last 3 char are "xls"

    return workbooksList

def main():
    cdLocation=os.getcwd()
    excelExtension="xls"


if __name__ == '__main__':
    main()
