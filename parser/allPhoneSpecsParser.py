#!/usr/bin/env python2.7

import urllib2, zlib, os, sys, re, pprint, json, sqlite3
from bs4 import BeautifulSoup
import pdb

DATABASE_FILE = '/home/dbases/phone_details.db'

# parse complete specifications of a all phones given data.json (provides url for each phone and name of phone) and write to database

def open_url(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError,TypeError:
        print "Error: Type is None"

def get_subheading(row):    
    if not row.findAll("td"):
        return ""
    result = ""
    subheading = row.findAll("td")[0].contents[0]    
    if subheading == u'\xa0':
        result = " "
    else:
        result = subheading.contents[0]
    return result

def get_phone_details(url):
    page = ""
    soup = ""
    phone_name = ""
    phone_details = {}    
    try:
        page = open_url(url)
        soup = BeautifulSoup(page)
        phone_name = soup.title.string.split('-')[0]        
        phone_details[phone_name] = {}        
        tables = soup.findAll("table")        
        
        for table in tables:            
            # find th in this table
            heading = table.find("th").text
            headingdict = {heading : {}}
            rows = table.findAll("tr")
            previous = ""
            for row in rows:                
                subheading = get_subheading(row)
                # if empty tr
                if subheading == "":
                    continue
                info = row.findAll("td")[1].text                
                # if current subheading is " ", then append current info to previous subheading's info
                if subheading == " " and previous != "":
                    headingdict[heading][previous] += ", " + info
                else:
                    headingdict[heading].update({subheading : info})
                    previous = subheading                
            
            phone_details[phone_name].update(headingdict)             
        return phone_details
        
    except TypeError, e:
        print "Error: Type is none " + str(e)
        
def update_database():
    count = 0
    try:
        with sqlite3.connect(DATABASE_FILE) as con:        
            home_page_url = "http://www.gsmarena.com/"
            print home_page_url
            with open('data.json', 'rb') as input_file:
                loaded_data = json.load(input_file)                
                pdb.set_trace()                
                for brand in loaded_data:
                    for model in loaded_data[brand]:
                        phone_name = brand + " " + model
                        # find if details already in database. if yes, skip this
                        cur = con.cursor()
                        query = 'select Name from PhoneSpecs where Name='+'\"' + phone_name + '\"'
                        cur.execute(query)
                        if cur.fetchone() is not None:
                            continue                    
                        phone_url = home_page_url + loaded_data[brand][model]["href"]
                        print phone_url
                        phone_details = get_phone_details(phone_url)                    
                        cur = con.cursor()
                        query = 'insert into PhoneSpecs(Name, Specs) values("%s", ?)' % (phone_name)
                        cur.execute(query, (json.dumps(phone_details),))
                        con.commit()
                        print "Number of rows updated: %d" % cur.rowcount
                        count +=1
                        print count
    except TypeError, e:
        print "Error: Type is none " + str(e)
        
if __name__ == '__main__':    
    update_database()
    
    
    
