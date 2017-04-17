# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 aout 2014

@author: Seko
@summary: Web Util library
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import sys
import xbmc
import urllib
import urllib2
import re

# ____________________     V A R I A B L E S     ____________________

# Get base_url, add_handle and arguments
base_url = sys.argv[0]

# Header configuration
HEADER_CFG = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive'}

# ____________________       M E T H O D S       ____________________
def build_url(query):
    """
        Method to build an url
    """
    return base_url + '?' + urllib.urlencode(query)

def encodeStr(string):
    """
        Method to encode a string
    """
    return urllib.quote(string)

def isUrlAcceptResume(url):
    """
        Method to know if the url accept resuming
    """
    # __ Result
    result = False
    # __ Create the request
    urlRequest = urllib2.Request(url, headers=HEADER_CFG)
    
    # __ Start the connection
    con = urllib2.urlopen(urlRequest)

    # __ Get headers informations, to know if we can resume the download
    responseHeader = con.info()
    if 'Accept-Ranges' in responseHeader:
        xbmc.log("Accept-Ranges: "+responseHeader['Accept-Ranges'])
        if responseHeader['Accept-Ranges'] != 'none':
            result = True
        
    # __ Close the connection    
    con.close()
    
    # __ Return the result
    return result


def getJSValue(jsStrValue):
    jsStrValue=jsStrValue.replace('!+[]','1')
    jsStrValue=jsStrValue.replace('+[]','0')
    jsStrValue=jsStrValue.replace('+!![]','1')
    jsStrValue=jsStrValue.replace('+![]','0')
    return str(jsStrValue.count('1'))


def byPassDDOSProtection(urlOpener, html, domain_url):
    """
        Method to pass the ddos protection of an url
        
        @param urlOpener: the urllib2 opener
        @param html: the html code returned with the error 503
        @param domain_url: the domain url of the web site, ex : http://www.dpstream.net/
        
        @return 
    """
    jschl=re.compile('name="jschl_vc" value="(.+?)"/>').findall(html)
    if jschl:
        # ___ Get the jschl_vc value 
        jschl = jschl[0]
        
        # ___ Calculate the jschl_answer value
        # ___ For instance : lCwCYNm={"kXpCZcngKcE":+((!+[]+!![]+!![]+!![]+[])+(!+[]+!![]+!![]+!![]+!![]+!![]+!![]+!![]+!![]))};
        
        # ___ Get the array variable, for instance 'lCwCYNm '
        tab=re.compile('var.*, (.*)(={"(.*)?":(.*)};)').findall(html)[0][0]
        # ___ Get the jschl_answer variable, for instance 'kXpCZcngKcE'
        variable=re.compile('var.*, (.*)(={"(.*)?":(.*)};)').findall(html)[0][2]
        
        
        # ___ Calculate, the initial value of the jschl_answer variable
        value=re.compile('var.*, (.*)(={"(.*)?":(.*)};)').findall(html)[0][3]       
        valueOne=re.compile('.*?\(\((.*)\)\+\((.*)\)\)').findall(value)[0][0]
        valueTwo=re.compile('.*?\(\((.*)\)\+\((.*)\)\)').findall(value)[0][1]   
        initialValue = eval(getJSValue(valueOne)+getJSValue(valueTwo))
           
        # ___ Add other calculated line
        otherLine=re.compile(';'+tab+'\.'+variable+'(.*)a\.value').findall(html)[0]
        
        for partToProcess in otherLine.split(';'):
            # __ For each line, calculate the new value of jschl_answer
            if len(re.compile('.*?\(\((.*)\)\+\((.*)\)\)').findall(partToProcess)) == 1 :
                # __ Case of number with 2 characters :
                valueOne=re.compile('.*?\(\((.*)\)\+\((.*)\)\)').findall(partToProcess)[0][0]        
                valueTwo=re.compile('.*?\(\((.*)\)\+\((.*)\)\)').findall(partToProcess)[0][1]
                addValue = eval(getJSValue(valueOne)+getJSValue(valueTwo))
                
            elif len( re.compile('('+tab+'\.'+variable+').*=(.*)').findall(partToProcess) ) == 1 :
                # __ Case of number with 1 characters : 
                valueOne=re.compile('('+tab+'\.'+variable+').*=(.*)').findall(partToProcess)[0][1]
                addValue = eval(getJSValue(valueOne))
            
            if partToProcess.startswith(tab+'.'+variable) :
                partToProcess = partToProcess.replace(tab+'.'+variable,'')        
            
            # ___ Calculate the new value depending on the mathematical character
            mathSign = partToProcess[0:1]
            if mathSign == '*':
                initialValue = initialValue * addValue
            elif mathSign == '/':
                initialValue = initialValue / addValue  
            elif mathSign == '+':
                initialValue = initialValue + addValue   
            elif mathSign == '-':
                initialValue = initialValue - addValue
                
        # ___ Add the length of the current address
        domain = re.compile('https?://(.+?)/').findall(domain_url)[0]
        initialValue = initialValue + len(domain)
        
        # ___ Ask the new url
        response = urlOpener.open(domain_url+'cdn-cgi/l/chk_jschl?jschl_vc=%s&jschl_answer=%s'%(jschl,initialValue))
        # ___ Return the redirection
        return response
        
        
def openInWebbrowser(url,webBrowserId=0):
    """
        Method to open a url in a webbrowser
        
        @param url: the url to open
        @param webBrowserId: the webbrowser id (Use only for andorid system)
        
        @note: 
            0 - Android Browser
            1 - Firefox
            2 - Chrome
            3 - Opera
            4 - Opera TV        
    """
    # ____ Display the list of choise
    osWin = xbmc.getCondVisibility('system.platform.windows')
    osOsx = xbmc.getCondVisibility('system.platform.osx')
    osLinux = xbmc.getCondVisibility('system.platform.linux')
    osAndroid = xbmc.getCondVisibility('System.Platform.Android')
    osIOS = xbmc.getCondVisibility('System.Platform.IOS')    
   
    # ___ Open in web browser 
    try:
        
        if osOsx:
            #xbmc.executebuiltin("RunAppleScript(tell application \"Safari\" to make new document with properties {URL:\""+urlToPlay+"\"})")                        
            xbmc.executebuiltin("System.Exec(open "+str(url)+")")
        elif osWin:
            xbmc.executebuiltin("System.Exec(cmd.exe /c start "+str(url)+")")
        elif osLinux and not osAndroid:
            # Need the xdk-utils package
            xbmc.executebuiltin("System.Exec(xdg-open "+str(url)+")")                    
        elif osIOS:
            xbmc.executebuiltin("System.Exec(open "+str(url)+")")
        elif osAndroid:
            if webBrowserId == "0":
                # ___ Open media with standard android web browser
                xbmc.executebuiltin("StartAndroidActivity(com.android.browser,android.intent.action.VIEW,,"+str(url)+")")
            elif webBrowserId == "1":
                # ___ Open media with Mozilla Firefox
                xbmc.executebuiltin("StartAndroidActivity(org.mozilla.firefox,android.intent.action.VIEW,,"+str(url)+")")                    
            elif webBrowserId == "2":
                # ___ Open media with Chrome
                xbmc.executebuiltin("StartAndroidActivity(com.android.chrome,,,"+str(url)+")")                            
            elif webBrowserId == "3":
                # ___ Open media with Opera
                xbmc.executebuiltin("StartAndroidActivity(com.opera.mini.android,android.intent.action.VIEW,,"+str(url)+")")            
            elif webBrowserId == "4":
                # ___ Open media with Opera Web TV Browser
                xbmc.executebuiltin("StartAndroidActivity(com.opera.tv.browser.sony.dia,android.intent.action.VIEW,,"+str(url)+")")
            
    except Exception, e:
        xbmc.log("Error during open the url "+str(url)+" in web browser "+str(webBrowserId),xbmc.LOGERROR)
        xbmc.log(e,xbmc.LOGERROR)  
 

    
def getFileName(url):
    """
        Method to get the filename to download
        @param the url
        @return the fileName
    """    
    patternURL = re.compile('(.*)(\/)(.*)(\\.)((.*){3})')
    match = patternURL.match(url.strip())
    if match is not None:           
        fileName = match.group(3)+match.group(4)+match.group(5)
    else:
        fileName = None
    
    return fileName  

def getFileExtension(url):
    """
        Method to get the filename to download
        @param the url
        @return the fileName
    """    
    patternURL = re.compile('(.*)(\/)(.*)(\\.)((.*){3})')
    match = patternURL.match(url.strip())
    if match is not None:           
        fileExtension = match.group(5)
    else:
        fileExtension = None
    
    return fileExtension   


class SmartRedirectHandler(urllib2.HTTPRedirectHandler):
    """
        Class SmartRedirectHandler for redirection
    """     
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)      
        result.status = code                           
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):  
        # ___ Change clkme.in by cllkme.com 
        if headers['location'].startswith('http://clkme.in'):
            headers['location']=headers['location'].replace('http://clkme.in','http://cllkme.com')
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)              
        result.status = code                                
        return result 
            
            