#-------------------------------------------------------------------------------
# Name:        studentProcessing
# Purpose:
#
# Author:      DBMS
#
# Created:     19/06/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def findImproperStudent(arrlist=[],*array): #finds the index for headings and whitespaces (where there should be student ID's)

    '''When the list of student objects is passed, this function finds the
        headings that are improper (such as headings and whitespaces)
        These improper rows are indicated by student ID field that is not a float
    '''
    pop=[]
    for i in range(len(arrlist)-1):
        if type(arrlist[i].studID) is not float:
            pop.append(i)
    return pop

def findDuplicate(arrlist=[],*array):

    '''When the list of student objects is passed, this function finds the
        duplicate rows. This accounts for people who are double majors, and have
        two rows of the same information. but with different plans
    '''
    pop=[]
    for i in range(len(arrlist)-1):

        if arrlist[i].studID==arrlist[i+1].studID:
            pop.append(i)
            i=i+1

    return pop

def findTriple(arrlist=[],*array):
    '''This function finds the triple rows for triple majors. It passes the first index of the three rows
        This first row is then popped off in another procedure
    '''
    pop=[]

    for i in range(len(arrlist)-2):
        if arrlist[i].studID==arrlist[i+1].studID and arrlist[i].studID==arrlist[i+2].studID:
            pop.append(i)

    return pop