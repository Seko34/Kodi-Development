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
import re
import strUtil
import json
from BeautifulSoup import BeautifulSoup
from src_mod.sourceTemplate import streamingSourceTemplate as Source
from item import StreamItem
from logger import Logger

if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:
    import miscFunctions as miscFunctions 
    
# ____________________        C L A S S          ____________________
class Streamay(Source):
        
    # ___ The source ID
    ID = 2
    
    # ___ The name of the source
    NAME = 'Streamay'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://streamay.bz/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','Streamay')
    
    # MENU
    
    MAIN_MENU_OPT = [#Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     #Source.MAIN_MENU_TVSHOW,
                     #Source.MAIN_MENU_ANIME,
                     #Source.MAIN_MENU_SHOW,
                     #Source.MAIN_MENU_DOCUMENTARY]
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     #Source.MENU_MOVIE_EXCLUE,
                     #Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     #Source.MENU_MOVIE_TOPWEEK,
                     #Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     #Source.MENU_MOVIE_CATEGORY_GENRE
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [#Source.MENU_TVSHOW_SEARCH
                       ] 
    
    MENU_ANIME_OPT = [] 
    
    def isLogin(self):          
        return True
    
    def login(self):
        """
            Method to login
        """        
        pass   
            
    
    def getItemsFromContent(self,content,type):
        """
            Method to get movie list
            @param content: the html content
            @param type: the type to extract
            @return the StreamItem list
        """
        elementList = []
        typeEl = None
        results = json.loads(content)

        if results is not None and len(results)>0:           
            for result in results:
                detail = result['result']
                title =detail['title'].encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                href = detail['url']
                year = detail['anneeProduction']
                quality = detail['qualite']  
                lang = strUtil.getLangFromTitle(detail['langue'])
                self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang) 
                element.setId(detail['id'])
                element.setSourceId(self.ID) 
                
                # __ Get the type
                if result['type'] == 'Film':
                        typeEl = StreamItem.TYPE_MOVIE           
                        element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                        element.setType(StreamItem.TYPE_MOVIE)              
                elif result['type'] == 'Série':
                    typeEl = StreamItem.TYPE_TVSHOW           
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)  
                    element.setTvShowName(title)   
                elif result['type'] == 'Manga':  
                    typeEl = StreamItem.TYPE_ANIME           
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_ANIME)  
                    element.setTvShowName(title)   
                
                
                if typeEl is not None and typeEl == int(type):      
                    # __ Get the poster
                    element.setIconImage(self.buildHref('/cdn/img/'+detail['img']))
                    
                    # __ Set the genre
                    element.setMetadataGenre(detail['genre'])
                    
                    # __ Add the element to the list
                    elementList.append(element)
        
        return elementList
    
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        post_href = 'search'
        data = {'k':title}
        response = self.postPage(post_href,data)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            elementList = self.getItemsFromContent(content, StreamItem.TYPE_MOVIE)
                    
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(post_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        post_href = 'search'
        data = {'k':title}
        response = self.postPage(post_href,data)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()            
            elementList = self.getItemsFromContent(content, StreamItem.TYPE_TVSHOW) 
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search tv show ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(post_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchAnime(self, title):
        """
            Method to search a anime
            @return a list of StreamItem
        """
        post_href = 'search'
        data = {'k':title}
        response = self.postPage(post_href,data)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()            
            elementList = self.getItemsFromContent(content, StreamItem.TYPE_ANIME) 
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Anime ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(post_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
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
    
   
    def getMovieLink(self,movieStreamItem):
        """
            Method to get all links of a movie
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        
        soupI = self._initOpenPage(movieStreamItem)
        streamers = soupI.findAll('a', attrs = {'data-streamer' : True})
        
        for streamer in streamers:
            response = self.openPage('streamer/'+movieStreamItem.getId()+'/'+streamer['data-streamer'])
            if response is not None and response.getcode()==200:
                content = response.read()
                jsonR = json.loads(content)
                # __ Create the element                       
                element = movieStreamItem.copy()
                element.setAction(StreamItem.ACTION_PLAY)
                element.setType(StreamItem.TYPE_STREAMING_LINK)
                element.setHref(jsonR['code'])           
                element.regenerateKodiTitle()
            
                self.appendLinkInList(element, elementList)
                   
                                  
                          
        return elementList
    
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
    
    def getLastMovie(self,streamItem=False):
        """
            Method to get all last movie
            @return a list of StreamItem
        """                
        pass
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        pass
    
    def getLastAnime(self,streamItem=False):
        """
            Method to get all last anime
            @return a list of StreamItem
        """
        pass  
    
    def getTopMovie(self,streamItem=False):
        """
            Method to get top movie
            @return a list of StreamItem
        """
        pass
    
    
    def getTopTvShow(self,streamItem=False):
        """
            Method to get top tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getTopAnime(self,streamItem=False):
        """
            Method to get top anime
            @return a list of StreamItem
        """
        pass
    
    def getMostViewMovie(self,streamItem=False):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        pass
    
    
    def getMostViewTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getMostViewAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """        
        pass
    
    def getTopWeekMovie(self,streamItem=False):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        pass
    
    
    def getTopWeekTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        pass
    
    
    def getTopWeekAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        pass
    def getExclueMovie(self,streamItem=False):
        """
            Method to get exclu movie
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        response = self.openPage('')
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
               pass 
                    
        return elementList   
    
    
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
        xmlSettingStr += '<setting label="Streamay" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_streamay_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr