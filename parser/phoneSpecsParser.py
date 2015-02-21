#!/usr/bin/env python2.7

import urllib2, zlib, os, sys, re, pprint, json
from bs4 import BeautifulSoup

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
        
if __name__ == '__main__':
    url = "http://www.gsmarena.com/apple_iphone_6-6378.php"
    phone_details = get_phone_details(url)
    print phone_details
    
    with open('iphone6.json', 'wb') as fp:
        json.dump(phone_details, fp)
        
    with open('iphone6.json', 'rb') as fp:
        loaded_data = json.load(fp)
        
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(loaded_data)

