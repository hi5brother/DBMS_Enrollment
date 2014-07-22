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
    pop = []
    for i in range(len(arrlist) - 1):
        if type(arrlist[i].studID) is not float:
            pop.append(i)
    return pop

def removeBEDProg(arrlist = [], *array):
    '''A DBMS course cannot be attributed to a BED program, so if BED is shown as
        a student's program, it is false.

        This function prevents BED from showing as the program
    '''

    for i in range(len(arrlist) - 2):

        if arrlist[i].studID == arrlist[i + 1].studID and arrlist[i].studID == arrlist[i + 2].studID:
            '''Treats triple majors and removes the BED designation
            '''
            if arrlist[i].program == 'BED':
                arrlist[i].program = arrlist[i + 1].program

            elif arrlist[i + 1].program == 'BED':
                arrlist[i + 1].program = arrlist[i].program

            elif arrlist[i + 2].program == 'BED':
                arrlist[i + 1].program = arrlist[i].program

    for i in range(len(arrlist) - 1):

        if arrlist[i].studID == arrlist[i + 1].studID:
            if arrlist[i].program == 'BED':  
                '''Considers the students who have BED, BSC for the double major
                '''

                arrlist[i].program = arrlist[i + 1].program

            elif arrlist[i + 1].program == 'BED':
                '''Considers the students who have BA, BED for the double major
                '''
                
                arrlist[i + 1].program = arrlist[i].program

    return arrlist


def findDuplicate(arrlist = [],*array):

    '''When the list of student objects is passed, this function finds the
        duplicate rows. This accounts for people who are double majors, and have
        two rows of the same information. but with different plans

        A DBMS course cannot be attributed to a BED program, so if BED is shown as
        a student's program, it is false.
    '''
    pop = []
    for i in range(len(arrlist) - 1):

        if arrlist[i].program == 'BED' and arrlist[i].studID == arrlist[i + 1].studID:  
            '''Considers the students who have BED, BSC for the double major
            '''

            arrlist[i].program == arrlist[i + 1].program

        elif arrlist[i + 1].program == 'BED' and arrlist[i].studID == arrlist[i + 1].studID:
            '''Considers the students who have BA/BCOMM, BED for the double major
            '''
            
            arrlist[i + 1].program == arrlist[i].program

        if arrlist[i].studID == arrlist[i + 1].studID:
            pop.append(i)
            i = i + 1

    return pop

def findTriple(arrlist = [],*array):
    '''This function finds the triple rows for triple majors. It passes the first index of the three rows
        This first row is then popped off in another procedure
    '''
    pop = []

    for i in range(len(arrlist) - 2):

        if arrlist[i].studID == arrlist[i + 1].studID and arrlist[i].studID == arrlist[i + 2].studID:

            pop.append(i)

    return pop