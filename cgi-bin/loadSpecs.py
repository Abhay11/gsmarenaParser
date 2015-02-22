#!/usr/bin/env python2.7

# to print the phone specifications on browser given phone name
import json, sqlite3

print 'Content-type: text/html\n\n'

with sqlite3.connect("/home/dbases/phone_details.db") as con:
    cur = con.cursor()
    name = "Lava Iris 405+"
    query = 'select Name, Specs from PhoneSpecs where Name='+'\"' + name + '\"'    
    cur.execute(query)
    result = cur.fetchone()
    if result is not None:
        specs = result[1]
        print specs
    else:
        print "Invalid input. Data for this phone does not exist."
    
