# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 02 Jan 2016

@author: Seko
@summary: Template for source class

'''
#---------------------------------------------------------------------
# ____________________        I M P O R T        ____________________
import xbmc
import sys
import kodiUtil
import re
from item import StreamItem
from logger import Logger
from src_mod.sourceTemplate import streamingSourceTemplate as Source
from BeautifulSoup import BeautifulSoup
if sys.argv[0].endswith('test.py'):
    import test.dummyMiscFunctions as miscFunctions
else:
    import miscFunctions as miscFunctions
import strUtil
import cookielib

# ____________________        C L A S S          ____________________
class Dummy(Source):
    
    
    # ___ The source ID
    ID = -1
    
    # ___ The name of the source
    NAME = 'Dummy'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','Dummy')
    
    # MENU
    
    MAIN_MENU_OPT = [#Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     #Source.MAIN_MENU_TVSHOW,
                     #Source.MAIN_MENU_ANIME,
                     #Source.MAIN_MENU_SHOW,
                     #Source.MAIN_MENU_DOCUMENTARY]
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     #Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     Source.MENU_MOVIE_CATEGORY_GENRE
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [] 
    
    MENU_ANIME_OPT = [] 
    
    def isLogin(self):          
        return True
    
    def login(self):
        """
            Method to login
        """        
        pass   
            
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        pass
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        pass
    
    def searchAnime(self, title):
        """
            Method to search a anime
            @return a list of StreamItem
        """
        pass
    
    def getTvShowSeasons(self, tvShowStreamItem):
        """
            Method to get the seasons list of a tv show
            @return a list of StreamItem
        """
        pass    
    
    def getAnimeSeasons(self, tvShowStreamItem):
        """
            Method to get the seasons list of an anime
            @return a list of StreamItem
        """
        pass
    
    def getTvShowEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        pass
    
    def getAnimeEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        pass
    
    def getLinks(self,streamItem):       
        """
            Method to get all links
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(streamItem)
        if soup is not None:
            
            divs = soup.findAll("div")
            count = 0  
            
            # ___ Case of standard link page
            for div in divs:                 
                # __ For each iframe
                iframes = div.findAll("iframe")
                for iframe in iframes:
                    if (iframe['src'].startswith('http://') or iframe['src'].startswith('https://')):
                        
                        # __ Get the link
                        href = iframe['src'].encode('UTF-8')
                        href = self.formatLink(href)

                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setHref(href)                 
                        element.regenerateKodiTitle()
                        
                        self.appendLinkInList(element, elementList)
                
                # __ For each embed
                embeds = div.findAll("embed")
                for embed in embeds:
                    if (embed['src'].startswith('http://') or embed['src'].startswith('https://')):
                        # __ Get the link
                        href = embed['src'].encode('UTF-8')
                        href = self.formatLink(href)
                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setHref(href)                        
                        element.regenerateKodiTitle()
                        
                        self.appendLinkInList(element, elementList)
                        
                                           
                count = len(elementList)            
                      
        return elementList
    
    
    
    def getMovieLink(self,movieStreamItem):
        """
            Method to get all links of a movie
            @return a list of StreamItem
        """
        return self.getLinks(movieStreamItem)
    
    def getTvShowEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        pass    
    
    def getAnimeEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        pass
    
    def getLastMovie(self):
        """
            Method to get all last movie
            @return a list of StreamItem
        """                
        pass
    
    def getLastTvShow(self):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        pass
    
    def getLastAnime(self):
        """
            Method to get all last anime
            @return a list of StreamItem
        """
        pass  
    
    def getTopMovie(self):
        """
            Method to get top movie
            @return a list of StreamItem
        """
        pass
    
    
    def getTopTvShow(self):
        """
            Method to get top tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getTopAnime(self):
        """
            Method to get top anime
            @return a list of StreamItem
        """
        pass
    
    def getMostViewMovie(self):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        pass
    
    
    def getMostViewTvShow(self):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getMostViewAnime(self):
        """
            Method to get top week anime
            @return a list of StreamItem
        """        
        pass
    
    def getTopWeekMovie(self):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        pass
    
    
    def getTopWeekTvShow(self):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getTopWeekAnime(self):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        pass
    
    def getAlphabeticMovieList(self,letter,page):
        
        """
            Method to get an alphabatic list of movie
            @return a list of StreamItem
        """
        pass
    def getAlphabeticTvShowList(self,letter,page):
        
        """
            Method to get an alphabatic list of tv show
            @return a list of StreamItem
        """
        pass
    def getAlphabeticAnimeList(self,letter,page):
        
        """
            Method to get an alphabatic list of anime
            @return a list of StreamItem
        """
        pass
    
    def getStreamingLink(self,href):
        
        """
            Method to get all links in a page
            @return a list of link
        """
        pass
    
    def getSettingsXml(self):
        """
            Method to get the xml settings of the current source
        """
        xmlSettingStr = ''
        xmlSettingStr += '<setting label="DummyLabel" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_dummmy_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr