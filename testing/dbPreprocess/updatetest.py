#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      DBMS
#
# Created:     15/05/2014
# Copyright:   (c) DBMS 2014
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import os
import sqlite3
#open database stuff
cdLocation=os.getcwd()
#print cdLocation
dbLocation=cdLocation+"updatetest.db"

conn=sqlite3.connect(dbLocation)
c=conn.cursor()

##c.execute('''CREATE TABLE Customer
##(CustID INT IDENTITY PRIMARY KEY,
##FirstName VARCHAR(40) NOT NULL,
##LastName VARCHAR(40) NOT NULL,
##StateCode VARCHAR(20) NOT NULL,
##PayRate money NOT NULL DEFAULT 0.00,
##Gender VARCHAR(1) NOT NULL)''')
##

##c.execute('''INSERT INTO Customer (FirstName, LastName, StateCode, PayRate,Gender)
##VALUES('Tejendra', 'Kumar', 'UP', 150.00,'M')''')
##
##c.execute('''INSERT INTO Customer (FirstName, LastName, StateCode, PayRate,Gender)
##VALUES('Jolly', 'Kapoor', 'MP', 50.00 ,'F')''')
##
##c.execute('''INSERT INTO Customer (FirstName, LastName, StateCode, PayRate,Gender)
##VALUES('Pavan', 'Kumar', 'MP', 200.00 ,'M')''')
##
##c.execute('''INSERT INTO Customer (FirstName, LastName, StateCode, PayRate,Gender)
##VALUES('Boby', 'Sharma', 'DL', 180.00 ,'F')''')
##
##c.execute('''INSERT INTO Customer (FirstName, LastName, StateCode, PayRate,Gender)
##VALUES('Asif', 'Khan', 'DL', 210.00 ,'M')''')

conn.commit()

c.execute('''SELECT * from Customer;''')

c.execute('''UPDATE Customer
            SET StateCode = CASE StateCode
             WHEN 'MP' THEN 'Madhya Pradesh'
             WHEN 'UP' THEN 'Uttar Pradesh'
             WHEN 'DL' THEN 'Delhi'
             ELSE NULL
             END''')

conn.commit()
c.execute('''SELECT FirstName, StateCode=
            CASE StateCode
             WHEN 'MP' THEN 'Madhya Pradesh'
             WHEN 'UP' THEN 'Uttar Pradesh'
             WHEN 'DL' THEN 'Delhi'
             ELSE NULL
             END), PayRate
            FROM Customer''')

temp=c.fetchall()
print temp
