# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 aout 2014

@author: Seko
@summary: Util library
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import re
import unicodedata
import HTMLParser

# ____________________     V A R I A B L E S     ____________________



# ____________________       M E T H O D S       ____________________
def remove_special_char(str):
    """
    Metho to remove all special characters to a string
    
    @param str: the string to remove all special char
    """
    try:
        newStr = str.decode('UTF-8')
        # ___ Remove special characters
        for c in "!@#$%^&*()[]{};:,./<>?\|~-=_+":
                
            try:
                newStr = re.sub("["+c+"]", "", newStr)
            except:
                newStr = re.sub("[\\"+c+"]", "", newStr)
                
        # ___ Remove simple quote
        for c in "`'’":
            
            try:
                newStr = re.sub("["+c+"]", " ", newStr)
            except:
                newStr = re.sub("[\\"+c+"]", " ", newStr)
        
        newStr = re.sub("\s\s", " ", newStr)
        
        # ___ Remove ’
        if isinstance(newStr, unicode):
            newStr = newStr.replace(u"\u2019", " ")
        
        str = newStr.encode('UTF-8')
    except:
        pass
    return str

def deleteAccent(str):
    """
        Method to delete accent from title
        
        @param title: the title to process
        
        @return the title without accent
    """
    accents = { 'a': ['à', 'ã', 'á', 'â'],
                'e': ['é', 'è', 'ê', 'ë'],
                'i': ['î', 'ï'],
                'u': ['ù', 'ü', 'û'],
                'o': ['ô', 'ö'] }
    for (char, accented_chars) in accents.iteritems():
        for accented_char in accented_chars:
            str = str.replace(accented_char, char)
    return str
    
def unescapeHtml(str):
    """
        Method to unescape html
        @param str: the string to process
        
        @return the title unescaped html
    """
    # ___ Unescaping HTML
    
    h = HTMLParser.HTMLParser()
    newStr = str.decode('UTF-8')
    newStr = h.unescape(newStr)
    str = newStr.encode('UTF-8')
    return str
    
def normalize(str):
    """
        Method to normalize a string
        @param str: the string to normalize
    """
    
    # ___ Unescaping HTML
    str = unescapeHtml(str)
    
    # ___ Transform string in unicode
    try:
        str = unicode(str, 'utf-8')
    except:
        pass
        
    
    try:
        # ___ Transform to utf-8 and return the string
        try:             
            return str.decode('ascii').encode("utf-8")
        except: 
            pass
        
        # ___ Else normalize character by character
        t = ''
        for i in str:
            c = unicodedata.normalize('NFKD',unicode(i,"ISO-8859-1"))       
            c = c.encode("ascii","ignore").strip()
            if i == ' ': c = i
            t += c
        
        # ___ Transform the result in utf-8
        return t.encode("utf-8")
    except:        
        return str
    
def getYearFromTitle(title):
    """
        Method to get the year in the title
        @param title: the name
        
        @return the year
    """
    patternYear = re.compile('(.*)(\\(*|\[*)(\d{4})(\\)*|\]*)(.*)')
    match = patternYear.match(title.strip())
    if match is not None:           
        year = int(match.group(3))
    else:
        year = None
    
    return year    
    
def removeYearFromTitle(title):
    """
        Method to remove the year in the title
        @param title: the name
        
        @return the new title
    """
    # ___ Do not remove anything if the title is a year (ex: 2012)
    patternYear = re.compile('\d{4}')
    match = patternYear.match(title.strip())
    if match is not None:           
        return title
        
    patternYear = re.compile('(.*)( +)(\\(|\[)(\d{4})(\\)|\])(.*)')
    match = patternYear.match(title.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = title
    
    return newTitle.strip()
    
def getQualityFromTitle(title):
    """
        Method to get the quality in the title
        @param title: the name
        
        @return the quality
    """ 
    patternQuality = re.compile('(.*)(DVDRIP|720P|1080P|BDRIP|BRRIP|DVDSCR|WEBRIP|HDTS|WEB-DL|HDRIP|MKV|BLU-RAY|BLURAY|BLUE\-RAY|XVID|X264|TS.MD|HDTV|\|R5|R6|SDTV)(.*)', re.IGNORECASE)
    match = patternQuality.match(title.strip())
    if match is not None:           
        quality = str(match.group(2))
    else:
        quality = None
    
    patternQuality = re.compile('(.*)(\\(|\[| )(TS||CAM|WEB|HD)(\\)|\]| )(.*)', re.IGNORECASE)
    match = patternQuality.match(title.strip())
    if match is not None and quality is None:
        quality = match.group(3)       
            
    return quality    
    
def removeQualityFromTitle(title):
    """
        Method to remove the quality in the title
        @param title: the name
        
        @return the new title
    """    
    patternQuality = re.compile('(.*)(\\(*|\[*)(DVDRIP|720P|1080P|BDRIP|BRRIP|DVDSCR|WEBRIP|HDTS|WEB-DL|HDRIP|MKV|BLU-RAY|BLURAY|BLUE\-RAY|XVID|X264|TS.MD|HDTV|\|R5|R6|SDTV)(\\)*|\]*)(.*)', re.IGNORECASE)
    match = patternQuality.match(title.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = title
        
    patternQuality = re.compile('(.*)(\\(|\[| )(TS||CAM|WEB|HD)(\\)|\]| )(.*)', re.IGNORECASE)
    match = patternQuality.match(title.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = title
    
    return newTitle.strip()
 
def getLangFromTitle(title):
    """
        Method to get the language in the title
        @param title: the name
        
        @return the language
    """
    
    patternLang = re.compile('(.*)(\[*|\(*|\|*|\{*)(FRENCH|TRUEFRENCH|TRUEFR|VF)(\]*|\)*|\|*|\}*)(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:    
        lang = 'FR'
        return lang
    else:
        lang = None
    
    
    patternLang = re.compile('(.*)(\[*|\(*|\|*|\{*)(ENGLISH)(\]*|\)*|\|*|\}*)(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:           
        lang = 'EN'
        return lang
    else:
        lang = None
        
    patternLang = re.compile('(.*)(\[*|\(*|\|*|\{*| )(VOST)(.*)(\]*|\)*|\|*|\}*| *)(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:           
        lang = 'VO'
        return lang
    else:
        lang = None
        
    patternLang = re.compile('(.*)(\[|\(|\||\{| )(VO|EN|FR|VF)(\]|\)|\||\}| )(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:
        return match.group(3).upper()
    else:
        lang = None
        
    patternLang = re.compile('(.*)(\[|\(|\||\{| )(VO|EN|FR|VF)$', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:
        return match.group(3).upper()
    else:
        lang = None
    
    patternLang = re.compile('(VO|EN)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:
        return 'VO'
    else:
        lang = None  

    patternLang = re.compile('(VF|FR)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:
        return 'FR'
    else:
        lang = None  
    
    return lang      
    
def removeLangFromTitle(title):
    """
        Method to remove the lang in the title
        @param title: the name
        
        @return the new title year
    """
    # __ We remove all lang except 'FR' and 'EN'
    patternLang = re.compile('(.*)(\[*|\(*|\|*|\{*)(FRENCH|TRUEFRENCH|TRUEFR|ENGLISH)(\]*|\)*|\|*|\}*)(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = title     
    
    # __ We remove all 'FR' and 'EN' if it is in bracket
    patternLang = re.compile('(.*)(\[|\(|\||\{| )(VO|EN|FR)(\]|\)|\||\}| )(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = title         
     
    
    patternLang = re.compile('(.*)(\[|\(|\||\{| )(VO|EN|FR|VF)$', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:
        newTitle = match.group(1)
    else:
        newTitle = title 
   
        
    patternLang = re.compile('(.*)(\[*|\(*|\|*|\{*| )(VOST)(.*)(\]*|\)*|\|*|\}*| *)(.*)', re.IGNORECASE)
    match = patternLang.match(newTitle.strip())
    if match is not None:           
        newTitle = match.group(1)
    else:
        newTitle = newTitle
            
    return newTitle.strip()

def getSubtitleFromTitle(title):
    """
        Method to get the subtitle in the title
        @param title: the name
        
        @return the subtitle
    """
    
    patternLang = re.compile('(.*)(\[|\(|\||\{| )(VOST)(.*)(\]|\)|\||\}| )(.*)', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:           
        subtitle = match.group(4).strip()
        return subtitle
    else:
        subtitle = None
        
    patternLang = re.compile('(.*)(\[|\(|\||\{| |)(VOST |VOST)(.*)$', re.IGNORECASE)
    match = patternLang.match(title.strip())
    if match is not None:  
        subtitle = match.group(4).strip()
        return subtitle
    else:
        subtitle = None
            
    return subtitle

def getServerFromTitle(title):
    """
        Method to get the server in the title
        @param title: the name
        
        @return the server (1FICHIER, MULTI etc...)
    """
    patternServer = re.compile('((\[|\()(.*)?(\]|\)))(.*)')
    match = patternServer.match(title.strip())
    if match is not None:       
        server = str(match.group(3))
    else:
        server = None  
    return server  
    
    
def removeServerFromTitle(title):
    """
        Method to remove the server in the title
        @param title: the name
        
        @return the new title year
    """
    patternLang = re.compile('((\[|\().*?(\]|\)))(.*)')
    match = patternLang.match(title.strip())
    if match is not None:           
        newTitle = match.group(4)
    else:
        newTitle = title       
    
                
    return newTitle.strip()    
    
def cleanTitle(title):
    """
        Method to clean a title
        
        @return the new title without quality, year and lang
    """
    
    # ___ Remove pre string
    patternToProcess = re.compile('(\.\:|\+UPX)(.*?)')
    match = patternToProcess.match(title.strip())
    if match is not None:
        title = match.group(2).strip() 
    
    # ___ Remove server, language, year and quality
    title = removeServerFromTitle(title)
    title = removeLangFromTitle(title)  
    title = removeYearFromTitle(title) 
    title = removeQualityFromTitle(title) 
        
    # ___ Remove post string
    patternToProcess = re.compile('.*?(\[|\()(.*)')
    match = patternToProcess.match(title.strip())
    if match is not None:
        title = title[0:title.find(match.group(1).strip())].strip() 
    
    return title

def getHostname(url):
    """
        Method to get the hostname from an url
        @param url: the http link
    
        @return the hostname
    """

    hostPattern = re.compile('(http|https)(://)(www\.|)(.*?)(\.)(.*)(/)(.*)')
    match = hostPattern.match(url)
    if match is not None:  
        return match.group(4).title()
    else:
        return None  
   
def detectType(text):
    """
       Method to detect the type of a text
       @param text: the text to identify 
    """
    if isinstance(text, str):
        print "Ordinary string"
    elif isinstance(text, unicode):
        print "Unicode string"
    else:
        print "not a string"
        
def toUTF8(text):
    if isinstance(text, str):
        return text
    elif isinstance(text, unicode):
        return text.encode('UTF-8')
    else:
        return text
    
#title = 'http://youwatch.org/embed-0iohlgkcdrl7.html/'
#print getHostname(title)