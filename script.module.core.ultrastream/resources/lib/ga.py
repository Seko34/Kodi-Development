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
import base64
import constant
from random import randint
from urllib import urlencode
from urllib2 import urlopen
from urlparse import urlunparse
from hashlib import sha1
from os import environ
# ____________________     V A R I A B L E S     ____________________


# ____________________     F U N C T I O N S       ____________________

def pushData():
    # Set your property id via the environment or simply type it
    # below
    PROPERTY_ID = environ.get("GA_PROPERTY_ID", base64.b64decode("VUEtOTIwOTIxNDYtMQ=="))
    
    # Generate the visitor identifier somehow. I get it from the
    # environment, calculate the SHA1 sum of it, convert this from base 16
    # to base 10 and get first 10 digits of this number.    
    VISITOR = environ.get("GA_VISITOR", urlopen('http://ident.me').read().decode('utf8'))
    VISITOR = str(int("0x%s" % sha1(VISITOR).hexdigest(), 0))[:10]
    
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
    
    