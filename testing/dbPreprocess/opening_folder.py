#-------------------------------------------------------------------------------
# Name:        folder opening
# Purpose:      open all excel files in a the current folder
#
# Author:      DBMS
#
# Created:     14/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import xlrd

def findFiles(location, extension):
    #cdLocation=os.getcwd()  #gets the current folder location

    workbooksList=[]    #store the file locations of all the workbooks

    for filename in os.listdir(location): #goes through every file in the folder
        if filename[-3:]==excelExtension:
            workbooksList.append(location+"\\"+filename)  #adds the file if the last 3 char are "xls"

    return workbooksList


excelExtension="xls"
cdLocation=os.getcwd()
print findFiles(cdLocation,excelExtension)


