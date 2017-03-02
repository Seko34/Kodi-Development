# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 16 Fev 2016

@author: Seko
@summary: GA
          Inspired from https://gist.github.com/pyzen/3980219 :
          Simple proof of concept code to push data to Google Analytics.

          Related blog post: http://www.canb.net/2012/01/push-data-to-google-analytics-with.html

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import re
import kodiUtil
import copy
import base64
import constant
import webUtil
import random
import urllib
import urllib2
import traceback
import time
from cookielib import CookieJar
from random import randint
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlunparse
from hashlib import sha1
from os import environ

# ____________________     V A R I A B L E S     ____________________

PROPERTY_ID = environ.get("GA_PROPERTY_ID", base64.b64decode("VUEtOTIwOTIxNDYtMQ=="))
# Generate the visitor identifier somehow. I get it from the
# environment, calculate the SHA1 sum of it, convert this from base 16
# to base 10 and get first 10 digits of this number.
VISITOR = environ.get("GA_VISITOR", urlopen('http://ident.me').read().decode('utf8'))
VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]

#resolution = '1366x768'
#vp =  '1366x424'

resolutionInfo = xbmc.getInfoLabel('System.ScreenResolution')
resolutionPattern = re.compile('(.*)(x)(.*)(@)(.*)')
match  = resolutionPattern.match(resolutionInfo)
resolution = match.group(1)+'x'+match.group(3)
vp =  match.group(1)+'x'+str(max(250,(int(match.group(3))-500)))


# ____________________     F U N C T I O N S       ____________________
def pushData(streamItem,type=False):
    
    
    # ___ The path to visit
    PATH = "Kodi-UltraStream"
    
    kernelVersion = xbmc.getInfoLabel('System.KernelVersion')    
    constant.__LOGGER__.log(str(kernelVersion),xbmc.LOGDEBUG)
    kernelPattern = re.compile('(.*)(\()(.*)')
    matchKernel  = kernelPattern.match(kernelVersion)
    if matchKernel is not None:
        kernelVersion = matchKernel.group(1)
        
    # ___ Get the current resolution
    resolution = xbmc.getInfoLabel('System.ScreenResolution')
    constant.__LOGGER__.log(str(resolution),xbmc.LOGDEBUG)
    resolutionPattern = re.compile('(.*)(x)(.*)(@)(.*)')
    match  = resolutionPattern.match(resolution)
    resolutionStr = match.group(1)+match.group(2)+match.group(3)
    
    PATH = PATH +'/'+kodiUtil.__kodiVersion__ +'/'+kernelVersion
    if type:
        PATH = type
    
    # ___ Collect everything in a dictionary
    DATA = {"utmwv": "5.2.2d",
            "utmn": str(randint(1, 9999999999)),
            "utmp": PATH,
            "utmac": PROPERTY_ID,
            "utmcc": "__utma=%s;" % ".".join(["1", VISITOR, "1", "1", "1", "1"]),
            "utmcs": "UTF-8",
            "utmdt": "Addon Usage",
            "utme": "Kodi "+kodiUtil.__kodiVersion__ + " - " +kernelVersion,
            "utmsc":"24-bit",
            "utmsr":resolutionStr}
           
    
    # ___ Encode this data and generate the final URL
    URL = urlunparse(("http",
                      "www.google-analytics.com",
                      "/__utm.gif",
                      "",
                      urlencode(DATA),
                      ""))
    
    # ___ Make the request
    constant.__LOGGER__.log("Requesting : "+str(URL),xbmc.LOGDEBUG)
    constant.__LOGGER__.log(urlopen(URL).info(),xbmc.LOGDEBUG)
    if type:
        _GAEvent(streamItem,type)
    else:
        _GAView(streamItem)
 
def _GAView(streamItem):
        
    # ___ Get random value between 75 000 000 and 85 000 000
    value1 = str(random.randint(75000000, 85000000))
    # ___ Get random value between 600 000 000 and 700 000 000
    valuea = str(random.randint(600000000,700000000))
    # __ Get current timeStamp
    timeStamp = getTimeStampStr()
    
    data = {
        'v':'1', # Protocol version, current is 1
        '_v':'j47', # SDK Version number
        'a':valuea, #'669510368 Random number used to link Google Analytics to Adsense 
        't':'pageview', # Hit type => Must be one of 'pageview', 'screenview', 'event', 'transaction', 'item', 'social', 'exception', 'timing'.
        '_s':'1', # hit Sequence - increments each time an event (inc pageview)
        'dl': streamItem.getGAUrl(), # Document location url : our initial url
        'ul':'fr', #user language
        'de':'UTF-8', # document encoding
        'dt':'Kodi UltraStream', # Document title
        'sd':'24-bit', # screen color
        'sr':resolution, # screen resolution
        'vp':vp, # View Port size (browser window visible area)
        'je':'1', 
        'fl':'24.0 r0', 
        '_u':'SEAAAAABI~', 
        'jid':value1, #
        'cid': ".".join(["1", VISITOR, "1", "1", "1", "1"]),
        'tid':PROPERTY_ID, 
        '_r':'1',
        'z':'260111890' 
        } 
    _GACollect(data,streamItem.getGAUrl())
    
def _GAEvent(streamItem,type):
    # ___ Get random value between 75 000 000 and 85 000 000
    value1 = str(random.randint(75000000, 85000000))
    # ___ Get random value between 600 000 000 and 700 000 000
    valuea = str(random.randint(600000000,700000000))
    # __ Get current timeStamp
    timeStamp = getTimeStampStr()
    data = {
        'v':'1',
        '_v':'j47',
        'a':valuea, 
        't':'event',
        '_s':'2',
        'dl':streamItem.getGAUrl(),
        'ul':'fr',
        'de':'UTF-8', 
        'dt':'Kodi UltraStream',
        'sd':'24-bit',
        'sr':resolution,
        'vp':vp,
        'je':'1',
        'fl':'24.0 r0',
        'ec':'play', # Event category
        'ea': type, # Event action
        'el':'success', # Event label
        '_utma':'1.'+value1+'.'+str(int(timeStamp)-1)+'.'+timeStamp+'.'+timeStamp+'.1',
        '_utmz':'1.'+timeStamp+'.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)',
        '_utmht':timeStamp,
        '_u':'SEACAAABI~', # Verification code generated by GA ?
        'jid':value1, #
        'cid': ".".join(["1", VISITOR, "1", "1", "1", "1"]),            
        'tid':PROPERTY_ID,            
        'z':'1705799455'
        } 
    _GACollect(data,streamItem.getGAUrl())
        
   
def _GACollect(data,url): 
    gaurl = 'https://www.google-analytics.com/r/collect?'+urllib.urlencode(data)
    headers = copy.copy(webUtil.HEADER_CFG)
    headers['Referer'] = url
    # ___ Init cookiejar
    cookiejar = CookieJar()
    # ___ Ini urlOpener
    urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    request = urllib2.Request(gaurl,headers=headers)
    try: 
        urlOpener.open(request) 
    except:
        traceback.print_exc()   
        
def getTimeStampStr():
    """
        Method to get the current timestamp in str
    """
    return str(int(time.time()))


