#-------------------------------------------------------------------------------
# Name:        time and dates
# Purpose:      date and time are objects and the methods must be called to find the date time values
#				sqltime and pythontime can both be output
#
# Author:      DBMS
#
# Created:     21/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import os

import time
from datetime import date

import sqlite3

import extractData

def SQLTime():		#SQL time capabilities
	conn = extractData.connectDB()
	c = conn.cursor()

	c.execute("SELECT strftime('%s','now');")	
	unixTime =  c.fetchall()		#grab the unix time string

	c.execute("SELECT datetime(?, 'unixepoch','localtime');", (unixTime[0]))		#find the date time string from the unix time string
	timeString = c.fetchone()

	conn.commit()
	conn.close

	return (timeString[0])



def pythonTime():		#Python's time module
	today = date.today()				 
	now = time.strftime("%H:%M:%S")

	return str(today) + " " + now



if __name__ == '__main__':

	print SQLTime()
	
	print pythonTime()