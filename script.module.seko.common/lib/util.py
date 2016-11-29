# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 aout 2014

@author: Seko
@summary: Util library
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import sys
import xbmc
import xbmcplugin
import urllib
import urllib2
import re

# ____________________     V A R I A B L E S     ____________________

# Get base_url, add_handle and arguments
__base_url__ = sys.argv[0]
__handle__ = None
if len(sys.argv) > 1:
    __handle__ = int(sys.argv[1])   

 
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
    return __base_url__ + '?' + urllib.urlencode(query)


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
            xbmc.executebuiltin("System.Exec(open "+url+")")
        elif osWin:
            xbmc.executebuiltin("System.Exec(cmd.exe /c start "+url+")")
        elif osLinux and not osAndroid:
            # Need the xdk-utils package
            xbmc.executebuiltin("System.Exec(xdg-open "+url+")")                    
        elif osIOS:
            xbmc.executebuiltin("System.Exec(open "+url+")")
        elif osAndroid:
            if webBrowserId == "0":
                # ___ Open media with standard android web browser
                xbmc.executebuiltin("StartAndroidActivity(com.android.browser,android.intent.action.VIEW,,"+url+")")
            elif webBrowserId == "1":
                # ___ Open media with Mozilla Firefox
                xbmc.executebuiltin("StartAndroidActivity(org.mozilla.firefox,android.intent.action.VIEW,,"+url+")")                    
            elif webBrowserId == "2":
                # ___ Open media with Chrome
                xbmc.executebuiltin("StartAndroidActivity(com.android.chrome,,,"+url+")")                            
            elif webBrowserId == "3":
                # ___ Open media with Opera
                xbmc.executebuiltin("StartAndroidActivity(com.opera.mini.android,android.intent.action.VIEW,,"+url+")")            
            elif webBrowserId == "4":
                # ___ Open media with Opera Web TV Browser
                xbmc.executebuiltin("StartAndroidActivity(com.opera.tv.browser.sony.dia,android.intent.action.VIEW,,"+url+")")
            
    except Exception, e:
        xbmc.log("Error during open the url "+url+" in web browser "+webBrowserId,xbmc.LOGERROR)
        xbmc.log(e,xbmc.LOGERROR)  
        