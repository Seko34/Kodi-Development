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
import json
import strUtil
import copy
import icons
import constant as constant
from BeautifulSoup import BeautifulSoup
from src_mod.sourceTemplate import streamingSourceTemplate as Source
from item import StreamItem
from logger import Logger
import webUtil

if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:
    import miscFunctions as miscFunctions
# ____________________        C L A S S          ____________________
class Sokrostream(Source):
    
    
    # ___ The source ID
    ID = 3
    
    # ___ The name of the source
    NAME = 'Sokrostream'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://sokrostream.biz/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','Sokrostream')
    
    # MENU
    
    MAIN_MENU_OPT = [#Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     Source.MAIN_MENU_TVSHOW,
                     #Source.MAIN_MENU_ANIME,
                     #Source.MAIN_MENU_SHOW,
                     #Source.MAIN_MENU_DOCUMENTARY]
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     #Source.MENU_MOVIE_EXCLUE,
                     Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     #Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     #Source.MENU_MOVIE_CATEGORY_GENRE,
                     Source.MENU_MOVIE_LIST
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [
                       Source.MENU_TVSHOW_SEARCH,
                       Source.MENU_TVSHOW_LAST,
                       Source.MENU_TVSHOW_TOPRATE,
                       Source.MENU_TVSHOW_LIST
                       ] 
    
    MENU_ANIME_OPT = [] 
    
    def isLogin(self):          
        return True
    
    def login(self):
        """
            Method to login
        """        
        pass   
            
    
    def getMoviesItemFromContent(self,content,filter=False):
        """
            Method to get movie list
            @param content: the html content
            @return the StreamItem list
        """ 
        elementList = []  
        
        itemsPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
        match = itemsPattern.match(content)
        if match is not None:
            jsonEl = json.loads(match.group(3))
            
            if not filter or filter == StreamItem.TYPE_MOVIE:
                
                for item in jsonEl['data'][0]['films']:
                    title = item['name']
                            
                    href = '/films/'+strUtil.remove_special_char(title).replace(' ','-').lower()+'-'+str(item['customID'])+'.html'
                    year = item['releaseYear']
                    quality = item['quality']
                    langClass = item['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)  
                    element.setSourceId(self.ID)  
                    element.setId(str(item['customID']))
                    element.setIconImage(item['poster'])
                    type = StreamItem.TYPE_MOVIE
                    elementList.append(element)
                    
            elif filter == StreamItem.TYPE_TVSHOW:
                for item in jsonEl['data'][0]['series']:
                    title = item['name']
                            
                    href = '/series/'+strUtil.remove_special_char(title).replace(' ','-').lower()+'-'+str(item['customID'])+'.html'
                    year = item['releaseYear']
                    quality = item['quality']
                    langClass = item['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    element.setSourceId(self.ID)  
                    element.setId(str(item['customID']))
                    element.setIconImage(item['poster'])                    
                    element.setTvShowName(title)   
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)   
                    type = StreamItem.TYPE_TVSHOW  
                    elementList.append(element)
                    
        # For every post, get title and topicLink   
        """       
        movies = soup.findAll('div',{ 'class':'column is-one-quarter-desktop is-half-mobile'})
                
        
        for index in range(0,len(movies)):
            
            movie = movies[index]
            
            title = movie.find('img',{'class':'image-fix'})['alt'].encode('UTF-8')
            title = strUtil.unescapeHtml(str(title))
                    
            self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
            href = movie.find('a')['href']
            year = strUtil.getYearFromTitle(title) 
            quality = movie.find('div',{'class':re.compile('(media-content)(.*)')}).text.encode('UTF-8')
            langClass = movie.find('img',{'class':'language-image'})['src']
            lang = None
            subtitle = None
            if langClass == '/vf.png':
                lang = 'FR'
            else:
                lang = 'VO'
                subtitle = 'FR'
            title = strUtil.cleanTitle(title)                
            self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
            
            # __ Create the element
            element = StreamItem(title)
            element.setHref(href)                
            element.setYear(year)             
            element.setQuality(quality)             
            element.setLang(lang)
            element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
            element.setType(StreamItem.TYPE_MOVIE)  
            element.setSourceId(self.ID)  
            element.setIconImage(movie.find('img')['src'])
            type = StreamItem.TYPE_MOVIE
            
            tvshowPattern = re.compile("(/series/)(.*)")
            print href
            match = tvshowPattern.match(href)
            if match is not None: 
                element.setTvShowName(title)   
                element.setType(StreamItem.TYPE_TVSHOW)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)   
                type = StreamItem.TYPE_TVSHOW  
                            
            # __ Add the element to the list
            if not filter:
                elementList.append(element)
            elif type == int(filter):
                elementList.append(element)
        """
        return elementList
    
    def getMovieContent(self,streamItem,page,response):
        """
            Generic method to get movie content
            @param response: the html response
            @param subtype: the subtype for streamItem 
        """
        elementList = []
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.find('section',{'class':'box'}).findAll('div',{ 'class':'column is-one-quarter-desktop is-half-mobile'})
                
                for movie in movies:
                                                   
                    title = movie.find('img',{'class':'image-fix'})['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a')['href']
                    year = strUtil.getYearFromTitle(title) 
                    quality = movie.find('div',{'class':re.compile('(media-content)(.*)')}).text.encode('UTF-8')
                    langClass = movie.find('img',{'class':'language-image'})['src']
                    lang = None
                    subtitle = None
                    if langClass == '/vf.png':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)
                    element.setQuality(quality)                         
                    element.setLang(lang)
                    element.setSubTitle(subtitle)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img',{'class':'image-fix'})['src'])                    
                                                            
                    # __ Add the element to the list
                    elementList.append(element)      
            
            nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
            nextPage.setIconImage(icons.getIcon('nextpage'))
            nextPage.setType(StreamItem.TYPE_MOVIE)
            nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            nextPage.setSubType(streamItem.getSubType())
            nextPage.setPage(int(page)+1)
            elementList.append(nextPage)
            
                    
        return elementList
    
    
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        get_href = 'search/'+title
        response = self.openPage(get_href)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()            
            elementList = self.getMoviesItemFromContent(content,StreamItem.TYPE_MOVIE)            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(get_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        
        get_href = 'search/'+title
        response = self.openPage(get_href)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()            
            elementList = self.getMoviesItemFromContent(content,StreamItem.TYPE_TVSHOW)            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(get_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
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
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(tvShowStreamItem.getHref())
        if response and response.getcode() == 200:    
            content = response.read()
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for season in jsonEl['data'][0]['data']['seasons']:                    
                
                    # __ Create the element
                    href = '/series/'+strUtil.remove_special_char(tvShowStreamItem.getTvShowName()).replace(' ','-').lower()+'-saison-'+str(season['number'])+'-'+str(tvShowStreamItem.getId())+'.html'
                    element = tvShowStreamItem.copy()
                    element.setSeason(season['number'])             
                    element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                    element.setHref(href)
                    element.determineSeasonTitle()
                    elementList.append(element)
        
        return elementList    
    
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
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(episodeStreamItem.getHref())
        if response and response.getcode() == 200:    
            content = response.read()
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for episode in jsonEl['data'][0]['data']['currentSeason']['episodes']:     
                    
                    # __ Create the element
                    href = '/series/'+strUtil.remove_special_char(episodeStreamItem.getTvShowName()).replace(' ','-').lower()+'-saison-'+str(jsonEl['data'][0]['season'])+'-episode-'+str(episode['number'])+'-'+str(episodeStreamItem.getId())+'.html'
                    element = episodeStreamItem.copy()
                    element.setEpisode(episode['number'])
                    element.setType(StreamItem.TYPE_TVSHOW_EPISODE)             
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setHref(href)
                    element.determineEpisodeTitle()
                    elementList.append(element)
        
        return elementList  
    
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
        
        # ___ Get the response        
        response = self.openPage(streamItem.getHref())
        if response and response.getcode() == 200:    
            content = response.read()
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                if streamItem.getType() == StreamItem.TYPE_MOVIE:
                    for link in jsonEl['data'][0]['data']['videos']:
                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setHref(link['link'])                
                        element.setQuality(link['quality'])                                      
                        element.setLang(link['language'])                                                     
                        element.setHostname(link['provider'])      
                        element.regenerateKodiTitle()              
                        # __ Add the element to the list
                        elementList.append(element)  
                        
                elif streamItem.getType() == StreamItem.TYPE_TVSHOW_EPISODE:
                    for link in jsonEl['data'][0]['data']['episode'][0]['videos']:
                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setHref(link['link'])                
                        element.setQuality(link['quality'])                                      
                        element.setLang(link['language'])                                                     
                        element.setHostname(link['provider'])      
                        element.regenerateKodiTitle()              
                        # __ Add the element to the list
                        elementList.append(element) 
                
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
        return self.getLinks(episodeStreamItem)
    
    def getAnimeEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        pass
    
    
   
    def getTvShowContent(self,streamItem,page,response):
        """
            Generic method to get movie content
            @param response: the html response
            @param subtype: the subtype for streamItem 
        """
        elementList = []
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.find('div',{'class':'filmcontent'}).findAll('div',{ 'class':'moviefilm'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a')['href']
                    
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                                                            
                    # __ Add the element to the list
                    elementList.append(element)      
            
            nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
            nextPage.setIconImage(icons.getIcon('nextpage'))
            nextPage.setType(StreamItem.TYPE_TVSHOW)
            nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            nextPage.setSubType(streamItem.getSubType())
            nextPage.setPage(int(page)+1)
            elementList.append(nextPage)
            
                    
        return elementList
    
    def getLastMovie(self,streamItem=False):
        """
            Method to get all last movie
            @return a list of StreamItem
        """  
        
        href = '/'              
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['nouveaux']['films']:
                
                    href = '/films/'+strUtil.remove_special_char(movie['name']).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(movie['name'] ) 
                    title = strUtil.deleteAccent(title)   
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)  
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])
                    elementList.append(element)
                
        return elementList
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        href = '/'
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['nouveaux']['series']:
                
                    title = movie['name']
                            
                    href = '/series/'+strUtil.remove_special_char(title).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(title)                 
                    title = strUtil.deleteAccent(title)   
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])                    
                    element.setTvShowName(title)   
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)  
                    elementList.append(element)
                    
        return elementList
    
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
        href = '/'   
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['box']['films']:
                
                    href = '/films/'+strUtil.remove_special_char(movie['name']).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(movie['name'])         
                    title = strUtil.deleteAccent(title)           
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)  
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])
                    elementList.append(element)
    
    
        return elementList
    
    def getTopTvShow(self,streamItem=False):
        """
            Method to get top tv show
            @return a list of StreamItem
        """
        
        href = '/'
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['box']['series']:
                
                    title = movie['name']
                            
                    href = '/series/'+strUtil.remove_special_char(title).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(title)       
                    title = strUtil.deleteAccent(title)             
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])                    
                    element.setTvShowName(title)   
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)  
                    elementList.append(element)
                    
        return elementList
    
    
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
    
    def getMovieList(self,streamItem=False):
        """
            Method to get a list of movie
            @return a list of StreamItem        
        """
        href = '/categories/films/page/1'
        page = 1
        if streamItem and streamItem.isPage():
            page = streamItem.getPage()
            href = streamItem.getHref()
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['elements']:
                
                    href = '/films/'+strUtil.remove_special_char(movie['name']).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(movie['name'])         
                    title = strUtil.deleteAccent(title)           
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)  
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])
                    elementList.append(element)
                
                if streamItem:
                    element = streamItem.copy()
                    page = page + 1
                    element.setType(StreamItem.TYPE_PAGE)
                    element.setPage(page)
                    element.setTitle('Page '+str(element.getPage()))
                    element.setHref('/categories/films/page/' + str(page))                    
                    elementList.append(element)
                else:
                    page = page + 1
                    element = StreamItem('Page '+str(element.getPage()))
                    element.setType(StreamItem.TYPE_PAGE)
                    element.setPage(page)
                    element.setTitle('Page '+str(element.getPage()))   
                    element.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
                    element.setSubType(StreamItem.SUBTYPE_LIST)  
                    element.setHref('/categories/films/page/' + str(page))              
                    elementList.append(element)
    
        return elementList
    
    def getTvShowList(self,streamItem=False):
        """
            Method to get a list of tvshow
            @return a list of StreamItem        
        """
        
        href = '/categories/series-tv/page/1'
        page = 1
        if streamItem and streamItem.isPage():
            page = streamItem.getPage()
            href = streamItem.getHref()
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the response        
        response = self.openPage(href)
        if response and response.getcode() == 200:    
            content = response.read()
            
            linksPattern = re.compile('(.*)(window\.__NUXT__=)(.*?)(;</script>)(.*)',re.DOTALL)
            match = linksPattern.match(content)
            if match is not None:
                jsonEl = json.loads(match.group(3))
                
                for movie in jsonEl['data'][0]['elements']:
                
                    title = movie['name']
                                                
                    href = '/series/'+strUtil.remove_special_char(title).replace(' ','-').lower()+'-'+str(movie['customID'])+'.html'
                    year = movie['releaseYear']
                    quality = movie['quality']
                    langClass = movie['language']
                    lang = None
                    subtitle = None
                    if langClass == 'vf':
                        lang = 'FR'
                    else:
                        lang = 'VO'
                        subtitle = 'FR'
                        
                    title = strUtil.cleanTitle(title)       
                    title = strUtil.deleteAccent(title)             
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)     
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    element.setQuality(quality)             
                    element.setLang(lang)
                    if subtitle is not None:
                        element.setSubTitle(subtitle)
                    element.setSourceId(self.ID)  
                    element.setId(str(movie['customID']))
                    element.setIconImage(movie['poster'])                    
                    element.setTvShowName(title)   
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)  
                    elementList.append(element)
                
                if streamItem:
                    element = streamItem.copy()
                    page = page + 1
                    element.setType(StreamItem.TYPE_PAGE)
                    element.setPage(page)
                    element.setTitle('Page '+str(element.getPage()))
                    element.setHref('/categories/series-tv//page/' + str(page))                    
                    elementList.append(element)
                else:
                    page = page + 1
                    element = StreamItem('Page '+str(element.getPage()))
                    element.setType(StreamItem.TYPE_PAGE)
                    element.setPage(page)
                    element.setTitle('Page '+str(element.getPage()))   
                    element.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
                    element.setSubType(StreamItem.SUBTYPE_LIST)  
                    element.setHref('/categories/series-tv//page/' + str(page))              
                    elementList.append(element)
    
        return elementList
    
    def getSettingsXml(self):
        """
            Method to get the xml settings of the current source
        """
        xmlSettingStr = ''
        xmlSettingStr += '<setting label="Sokrostream" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_sokrostream_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr