

# initialize
import xml.etree.cElementTree as ET
import pprint
import re
import operator
import codecs
import json
import requests
import sys
from bs4 import BeautifulSoup as bs
import pymongo
from pymongo import MongoClient
from collections import defaultdict, OrderedDict
from time import sleep


def get_addy(soup, node):
    
    title = soup.find('span', itemprop='name').text
    areas = soup.find_all('span', itemprop='addressAddress')
    
    if len(areas) == 1:
        area2 = None
        area1 = areas[0].text
    elif len(areas) == 2:
        area2 = areas[0].text
        area1 = areas[1].text
    else:
        print str(node) + " has not 1 nor 2 areas"
    
    local = soup.find_all('span', itemprop='addressLocality')
    city = local[0].text
    region3 = local[0].text
    region = soup.find_all('span', itemprop='addressRegion')
    region2 = region[0].text
    region1 = region[1].text
    postcode = soup.find('span', itemprop='postalCode').text
    
    out = OrderedDict({
        'key': postcode,
        'value': OrderedDict({
            'full': title,
            'building': area2,
            'street': area1,
            'region3': region3,
            'region2': region2,
            'region1': region1,
            'city': city,
            'postcode': postcode
        })
    })
    
    return out


def get_site(start=1, end=124289, pause=2):
    sleep(pause)
    client = MongoClient("mongodb://localhost:27017")
    db = client.openmap
    main = 'http://sgp.postcodebase.com/node/'
    for i in range(start, end):
        try:
            r = requests.get(main + str(i))
            soup = bs(r.text, 'lxml')
            result = get_addy(soup, i)
            db.postcode.insert_one(result['value'])
        except pymongo.errors.DuplicateKeyError:
            print "page: " + str(i) + " already exists"
        except:
            return i
    print "complete"


def clean(d, addy_list, addy_dict):
    
    addy = d['address']
    postcode_post = None
    postcode_st = None
    flag_post = None
    flag_st = None
    addy_post = None
    addy_st = None
    
    # try postcode first
    if 'postcode' in addy.keys():
        flag_post = True
        postcode_post = addy['postcode']
        addy_post = addy_dict[postcode_post]
        
    if 'street' in addy.keys():
        flag_st = True
        addy_st = addy['street'].lower()
        if 'housenumber' in addy.keys():
            addy_match = addy_st + ", " + addy['housenumber']
        else:
            addy_match = addy_st
            
        addy_regex = re.compile(r"\b.*?" + re.escape(addy_match) + r"\b.*?")
        result_reg = [l for l in addy_list for m in [addy_regex.search(l)] if m]
        if len(result_reg) > 0:
            postcode_st = result_reg[0].split("__")[1]
            addy_st = addy_dict[postcode_st]
            
    if flag_post and flag_st:
        if addy_post and addy_st:
            if postcode_post == postcode_st:
                result = 'both info avail, found and match'
            
            else:
                result = 'both info avail, found but no match'
        
        elif addy_post:
            result = 'both info avail, only postcode found'

        elif addy_st:
            result = 'both info avail, only street found'
            
        else:
            result = 'both info avail, nothing found'
            
    elif flag_post:
        if addy_post:
            result = 'only postcode available and found'
            
        else:
            result = 'only postcode available and not found'
            
    elif flag_st:
        if addy_st:
            result = 'only street available and found'
            
        else:
            result = 'only street available and not found'
            
    else:
        result = "something is wrong"
    
    return [addy_post, addy_st, result]


def clean_singapore(start=0, end=None):
    
    # data to clean
    query = {"$and": [
    {"$or": [
    {'address.city': {'$exists': 1, '$eq':'Singapore'}},
    {'address.country': {'$exists': 1, '$eq':'SG'}}
    ]},
    {'address': {'$exists': 1}},
    {"$or": [
    {'address.street': {'$exists': 1}},
    {'address.postcode': {'$exists': 1}}
    ]},
    ]}

    tab = OrderedDict((
        ('both info avail, found and match', 0),
        ('both info avail, found but no match', 0),
        ('both info avail, only postcode found', 0),
        ('both info avail, only street found', 0),
        ('both info avail, nothing found', 0),
        ('only postcode available and found', 0),
        ('only postcode available and not found', 0),
        ('only street available and found', 0),
        ('only street available and found', 0),
        ('something is wrong', 0),
        ('exception', 0)
    ))
    client = MongoClient("mongodb://localhost:27017")
    db = client.openmap
    coll = db.mapdata_raw
    dat_in_query = coll.find(query)
    dat_in = [x for x in dat_in_query]
    
    # full address to postcode dictionary
    dat_post = db.postcode.find({}, {'full': 1, 'postcode': 1})
    addy_list = [x['full'].lower() + "__" + x['postcode'] for x in dat_post]
    
    dat_all = db.postcode.find()
    addy_dict = {x['postcode']: x for x in dat_all}

    if end:
        end = end
    else:
        end = len(dat_in)
    cnt = 0
    error_cnt = []
    dat_out = []
    for d in dat_in[start:end]:
        try:
            out = clean(d, addy_list, addy_dict)
            tab[out[2]] += 1
            dat_new = OrderedDict((
                ('address', d),
                ('add_post', out[0]),
                ('add_st', out[1]),
                ('type', out[2])
            ))
            dat_out.append(dat_new)
        except:
            tab['exception'] += 1
            error_cnt.append(cnt)
        cnt += 1
        sys.stdout.write("Progress: {} of {} \r".format(cnt, end) ) # Cursor up one line
        sys.stdout.flush()
    return [dat_out, tab, error_cnt]
