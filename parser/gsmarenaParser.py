#!/usr/bin/env python2.7

import urllib2, zlib, os, sys, re, pprint, json
from bs4 import BeautifulSoup

home_page_url = "http://www.gsmarena.com/"
brand_urls = {}
all_urls_for_brands = {}

brand_details = {}

def open_url(url):
    try:
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read()
    except urllib2.HTTPError,TypeError:
        print "Error: Type is None"

### TO OPEN A COMPRESSED URL ( URL ENDING WITH ".gz" ) AND DECOMPRESS THE PAGE
def get_plain_page(url):
    compressed_page = open_url(url)
    if compressed_page:
        d = zlib.decompressobj(16 + zlib.MAX_WBITS)
        decompressed_page = d.decompress(compressed_page)
        return decompressed_page
    else:
        return False
    
# get url of first page of all brands
def get_brand_urls():
    decompressed_page = ""
    soup = ""
    
    try:
        decompressed_page = open_url(home_page_url)
        soup = BeautifulSoup(decompressed_page)
        #print soup
        # dictionary = { "<brandname>" : "<relative_url>"}
        
        brands = soup.find("div", {"id": "brandmenu"}).find('ul').findAll('li')
        #print brands
        for li in brands:
            #print li.find('a').contents[0]
            #print li.find('a')['href']
            brand_urls[li.find('a').contents[0]] = li.find('a')['href']
        
        #print brand_urls
    except TypeError, e:
        print "Error: Type is none " + e
        
def get_all_urls_for_brands():
    #all_urls_for_brands = {}
    for keys in brand_urls:
        listofurlsforabrand = []
        # append the current url to the list
        listofurlsforabrand.append(brand_urls[keys])        
        page = open_url(home_page_url+brand_urls[keys])
        soup = BeautifulSoup(page)
        
        # if the first page is the only page for a brand, there the div with class="nav-pages" is absent
        if soup.find("div", {"class":"nav-pages"}) is None:
            continue
        
        allA = soup.find("div",{"class":"nav-pages"}).findAll('a')
        # append the remaining urls 
        for element in allA:            
            if (element.contents[0]).isnumeric():                
                listofurlsforabrand.append(element["href"])
        #print listofurlsforabrand
        all_urls_for_brands[keys] = listofurlsforabrand
        #break
    print all_urls_for_brands
    return all_urls_for_brands
    


def get_model_details(model):    
    model_details = {}                
    model_details["href"] = model.find('a')['href']
    model_details["img_src"] = model.find('a').find('img')['src']
    model_details["title"] = model.find('a').find('img')['title']
    print model_details
    return model_details
    
    

        
def get_brand_model_urls():    
    #brand_details = {}
    for keys in all_urls_for_brands:        
        #print keys
        brand_name = keys
        brand_details[brand_name] = {}
        for elem in all_urls_for_brands[keys]:            
            brand_list_url = home_page_url + elem
            brand_list_page = open_url(brand_list_url)
            soup = BeautifulSoup(brand_list_page)
            models_block = soup.findAll("div", {"class": "makers"})
            for models in models_block:
                model_list = models.find('ul').findAll('li')
                for model in model_list:
                    model_info = {}                    
                    model_name = model.find('a').contents[1].contents[0]                   
                    model_info[model_name] = get_model_details(model)
                    brand_details[brand_name].update(model_info)
                    
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(brand_details)
        
        
        
    

        
if __name__ == '__main__':
    get_brand_urls()
    print brand_urls
    get_all_urls_for_brands()
    get_brand_model_urls()
    
    with open('data.json', 'wb') as fp:
        json.dump(brand_details, fp)
        
    with open('data.json', 'rb') as fp:
        loaded_data = json.load(fp)
        
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(loaded_data)
    

    

        

