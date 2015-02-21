#!/usr/bin/env python2.7

# to print the phone specifications on browser given phone name
import json, sqlite3

print 'Content-type: text/html\n\n'

with sqlite3.connect("/home/dbases/phone_details.db") as con:
    cur = con.cursor()
    name = "Apple iPhone 6"
    query = 'select Name, Specs from PhoneSpecs where Name='+'\"' + name + '\"'    
    cur.execute(query)
    print cur.fetchone()[1]
    
