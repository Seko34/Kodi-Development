# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 01 Nov 2016

@author: Seko
@summary: Trailer functions

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import urllib2
import cookielib
import webUtil
import traceback
import re
import xbmc
import constant as constant
import miscFunctions as miscFunctions
from BeautifulSoup import BeautifulSoup
from logger import Logger
import strUtil

# ____________________     C L A S S       ____________________
class YoutubeTrailer(object):
    
    __LOGGER__ = Logger('UltraStream','YoutubeTrailer')
    
    def __init__(self):
        """
            Constructor
        """
        # ___ We active cookies support for urllib2
        self.cookiejar = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))

    def searchTrailer(self,title):
        """
            Method to search a trailer
            @param title: the movie title
            @return the youtube id
            
        """
        searchParam = strUtil.deleteAccent(title)+' '+str(constant.__addon__.getLocalizedString(70012))
        href = 'https://www.youtube.com/results?q=' + webUtil.encodeStr(searchParam)
        self.__LOGGER__.log(href,xbmc.LOGDEBUG)
        request = urllib2.Request(href, headers=webUtil.HEADER_CFG)
        response = None
        
        try: 
            response = self.urlOpener.open(request)
        except urllib2.HTTPError as e:
            response = e 
        except:
            traceback.print_exc()
            miscFunctions.displayNotification('Error during searching trailer for '+title)
            
        if response and response.getcode() == 200:
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
            link = soup.find('a',{'class':re.compile('(yt-uix-tile-link yt-ui-ellipsis yt-ui-ellipsis-2 yt-uix-sessionlink)(.*)(spf-link)(.*)')})
            
            patternIdYoutube = re.compile('(\/watch\?v=)(.*)')
            match = patternIdYoutube.match(link['href'])
            if match is not None:
                id=match.group(2)                
                self.__LOGGER__.log('id = '+id,xbmc.LOGDEBUG)
                return id
        
        return None
    
    def playTrailer(self,title):
        """
            Method to play the movie trailer
            @param title: the movie title
        """
        id = self.searchTrailer(title)
        if id is not None:
            url = 'plugin://plugin.video.youtube/play/?video_id=%s' % id
            xbmc.executebuiltin('PlayMedia('+ url + ')')
            
