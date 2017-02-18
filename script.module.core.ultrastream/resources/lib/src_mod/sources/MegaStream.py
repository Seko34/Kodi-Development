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
import base64
import strUtil
import icons
import constant as constant

from BeautifulSoup import BeautifulSoup
from src_mod.sourceTemplate import streamingSourceTemplate as Source
from item import StreamItem
from logger import Logger

if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:
    import miscFunctions as miscFunctions

# ____________________        C L A S S          ____________________
class MegaStream(Source):
    
    
    # ___ The source ID
    ID = 5
    
    # ___ The name of the source
    NAME = 'MegaStream'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://mega-stream.fr/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','Mega-Stream')
    
    # MENU
    
    MAIN_MENU_OPT = [#Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     Source.MAIN_MENU_TVSHOW,
                     Source.MAIN_MENU_ANIME,
                     #Source.MAIN_MENU_SHOW,
                     #Source.MAIN_MENU_DOCUMENTARY]
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     #Source.MENU_MOVIE_EXCLUE,
                     Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_LIST
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     #Source.MENU_MOVIE_CATEGORY_GENRE
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [Source.MENU_TVSHOW_SEARCH,
                       Source.MENU_TVSHOW_LAST,
                       Source.MENU_TVSHOW_TOPWEEK,
                       Source.MENU_TVSHOW_TOPRATE,
                       #Source.MENU_TVSHOW_LIST
                       ] 
    
    MENU_ANIME_OPT = [
                      Source.MENU_ANIME_SEARCH,
                      Source.MENU_ANIME_LAST,
                      #Source.MENU_ANIME_LIST
                      ]
    
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
        # Use post http://mega-stream.fr/recherche
        #
        # search:3
        #
        
        post_href = '/recherche'
        # Data to post
        data = {'search':title}
        response = self.postPage(post_href, data)
        
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            soup = BeautifulSoup(content)      
            
            # ___ The first sectio is for movie       
            movies = soup.findAll('div',{'class':'section'})[0].findAll('div',{'class':'movie-item ignore-select'})
            
            for index in range(0,len(movies)):
                
                movie = movies[index] 
                               
                title = movie.find('img')['alt'].encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                href = movie.find('div',{'class':'movie-series'}).find('a')['href']
                titleExtract = movie.find('div',{'class':'movie-series'}).find('a').text.encode('UTF-8')
                year = strUtil.getYearFromTitle(titleExtract) 
                quality = strUtil.getQualityFromTitle(titleExtract)  
                lang = strUtil.getLangFromTitle(titleExtract)
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                if movie.find('span') is not None:
                    element.setQuality(movie.find('span').text.encode('UTF-8'))             
                element.setLang(lang)
                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                element.setType(StreamItem.TYPE_MOVIE)
                element.setSourceId(self.ID)  
                element.setIconImage(movie.find('img')['src'])                  
                                
                
                # __ Add the element to the list
                elementList.append(element)
        
            
            
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
        # Use post http://mega-stream.fr/recherche
        #
        # search:3
        #
        
        post_href = '/recherche'
        # Data to post
        data = {'search':title}
        response = self.postPage(post_href, data)
        
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            soup = BeautifulSoup(content)      
            
            # ___ The first sectio is for movie       
            movies = soup.findAll('div',{'class':'section'})[1].findAll('div',{'class':'movie-item ignore-select'})
            for index in range(0,len(movies)):
                
                movie = movies[index] 
                               
                title = movie.find('img')['alt'].encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                href = movie.find('div',{'class':'movie-series'}).find('a')['href']
                titleExtract = movie.find('div',{'class':'movie-series'}).find('a').text.encode('UTF-8')
                year = strUtil.getYearFromTitle(titleExtract) 
                quality = strUtil.getQualityFromTitle(titleExtract)  
                lang = strUtil.getLangFromTitle(titleExtract)
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                if movie.find('span') is not None:
                    element.setQuality(movie.find('span').text.encode('UTF-8'))             
                element.setLang(lang)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_TVSHOW)
                element.setSourceId(self.ID)  
                element.setIconImage(movie.find('img')['src'])                  
                                
                
                # __ Add the element to the list
                elementList.append(element)
        
            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search TvShow ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(post_href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchAnime(self, title):
        """
            Method to search a anime
            @return a list of StreamItem
        """
        
        # Use post http://mega-stream.fr/recherche
        #
        # search:3
        #
        
        post_href = '/recherche'
        # Data to post
        data = {'search':title}
        response = self.postPage(post_href, data)
        
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            soup = BeautifulSoup(content)      
            
            # ___ The first sectio is for movie       
            movies = soup.findAll('div',{'class':'section'})[2].findAll('div',{'class':'movie-item ignore-select'})
            for index in range(0,len(movies)):
                
                movie = movies[index] 
                               
                title = movie.find('img')['alt'].encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                href = movie.find('div',{'class':'movie-series'}).find('a')['href']
                titleExtract = movie.find('div',{'class':'movie-series'}).find('a').text.encode('UTF-8')
                year = strUtil.getYearFromTitle(titleExtract) 
                quality = strUtil.getQualityFromTitle(titleExtract)  
                lang = strUtil.getLangFromTitle(titleExtract)
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                if movie.find('span') is not None:
                    element.setQuality(movie.find('span').text.encode('UTF-8'))             
                element.setLang(lang)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_ANIME)
                element.setSourceId(self.ID)  
                element.setIconImage(movie.find('img')['src'])                  
                                
                
                # __ Add the element to the list
                elementList.append(element)
        
            
            
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
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(tvShowStreamItem)
        
        if soup is not None:
            seasons = soup.find('article',{'class':'full-article'}).find("div",{'class':'mc-left'}).find('div',{'id':'accordian'}).find('ul').findAll('li',recursive=False)
            
            for season in seasons:
                
                title = season.find('a').text.encode('UTF-8')
                seasonPattern = re.compile('(Saison )(.*)')
                match = seasonPattern.match(title)
                if match is not None:  
                    seasonNum = match.group(2) 
                else:
                    seasonNum = title
                # __ Create the element                       
                element = tvShowStreamItem.copy()
                element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                element.setType(StreamItem.TYPE_TVSHOW_SEASON)
                element.setSeason(seasonNum)
                element.determineSeasonTitle()
                
                elementList.append(element)
        
        # ___ Error during getting seasons
        else:
            miscFunctions.displayNotification('Unable to get seasons of ' + tvShowStreamItem.getTitle())                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(tvShowStreamItem.getHref()) + ')', xbmc.LOGERROR)
    
        return elementList
    
    
    def getAnimeSeasons(self, tvShowStreamItem):
        """
            Method to get the seasons list of an anime
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(tvShowStreamItem)
        
        if soup is not None:
            seasons = soup.find('article',{'class':'full-article'}).find("div",{'class':'mc-left'}).find('div',{'id':'accordian'}).find('ul').findAll('li',recursive=False)
            
            for season in seasons:
                
                title = season.find('a').text.encode('UTF-8')
                seasonPattern = re.compile('(Saison )(.*)')
                match = seasonPattern.match(title)
                if match is not None:  
                    seasonNum = match.group(2) 
                else:
                    seasonNum = title
                    
                # __ Create the element               
                element = tvShowStreamItem.copy()
                element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                element.setType(StreamItem.TYPE_ANIME_SEASON)
                element.setSeason(seasonNum)
                element.determineSeasonTitle()
                
                elementList.append(element)
        
        # ___ Error during getting seasons
        else:
            miscFunctions.displayNotification('Unable to get seasons of ' + tvShowStreamItem.getTitle())                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(tvShowStreamItem.getHref()) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def getTvShowEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(episodeStreamItem)
        
        if soup is not None:
            seasons = soup.find('article',{'class':'full-article'}).find("div",{'class':'mc-left'}).find('div',{'id':'accordian'}).find('ul').findAll('li',recursive=False)
            
            for season in seasons:
                
                title = season.find('a').text.encode('UTF-8')
                seasonPattern = re.compile('(Saison )(.*)')
                match = seasonPattern.match(title)
                if match is not None:  
                    seasonNum = match.group(2) 
                else:
                    seasonNum = title

                
                if seasonNum == str(episodeStreamItem.getSeason()):
                    
                    episodeSoup = season.find('ul').findAll('li')                    
                    for li in episodeSoup:
                        text = li.text.encode('UTF-8')                        
                        episodePattern = re.compile('(.*)(pisode )(.*)')
                        match = episodePattern.match(text)
                        if match is not None:  
                            episodeNum = match.group(3) 
                        else:
                            episodeNum = text
                        
                        href = li.find('a')['href']
                        # __ Create the element                       
                        element = episodeStreamItem.copy()
                        element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                        element.setType(StreamItem.TYPE_TVSHOW_EPISODE)
                        element.setEpisode(episodeNum)
                        element.setHref(href)
                        element.determineEpisodeTitle()
                        
                        elementList.append(element)
                
        
        # ___ Error during getting seasons
        else:
            miscFunctions.displayNotification('Unable to get episodes of ' + episodeStreamItem.getTitle())                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(episodeStreamItem.getHref()) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def getAnimeEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """        
        
        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(episodeStreamItem)
        
        if soup is not None:
            seasons = soup.find('article',{'class':'full-article'}).find("div",{'class':'mc-left'}).find('div',{'id':'accordian'}).find('ul').findAll('li',recursive=False)
            
            for season in seasons:
                
                title = season.find('a').text.encode('UTF-8')
                seasonPattern = re.compile('(Saison )(.*)')
                match = seasonPattern.match(title)
                if match is not None:  
                    seasonNum = match.group(2) 
                else:
                    seasonNum = title

                
                if seasonNum == str(episodeStreamItem.getSeason()):
                    
                    episodeSoup = season.find('ul').findAll('li')                    
                    for li in episodeSoup:
                        text = li.text.encode('UTF-8')                        
                        episodePattern = re.compile('(.*)(pisode )(.*)')
                        match = episodePattern.match(text)
                        if match is not None:  
                            episodeNum = match.group(3) 
                        else:
                            episodeNum = text
                        
                        href = li.find('a')['href']
                        # __ Create the element                       
                        element = episodeStreamItem.copy()
                        element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                        element.setType(StreamItem.TYPE_ANIME_EPISODE)
                        element.setEpisode(episodeNum)
                        element.setHref(href)
                        element.determineEpisodeTitle()
                        
                        elementList.append(element)
                
        
        # ___ Error during getting seasons
        else:
            miscFunctions.displayNotification('Unable to get episodes of ' + episodeStreamItem.getTitle())                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(episodeStreamItem.getHref()) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def getLinks(self,streamItem):       
        """
            Method to get all links
            @return a list of StreamItem
        """ # ___ Initialize the list to return
        elementList = []
        soup = None
        
        # ___ Get the soup
        soup = self._initOpenPage(streamItem)
                        
        qualities = soup.findAll('a',{'href':re.compile('(#lecteur_)(.*)')})  
        links = soup.findAll('div',{'id':re.compile('(lecteur_)(.*)')})   
                     
        # ___ For each server
        for link in links:  
            
            lecteurId = link['id'].replace('lecteur_','')
            for quality in qualities:
                lecteurQualityId = quality['href'].replace('#lecteur_','')
                
                if lecteurQualityId == lecteurId:
                    
                    aEl = link.find('a',{'class':'videos-other vo-3 nosel'})
                    if aEl is not None:
                        href = base64.b64decode(aEl['data-tnetnoc-crs'])[::-1]
                        lang = quality.find('img')['title'].encode('UTF-8')
                        qual = quality.text.encode('UTF-8').strip()                
                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setLang(lang)
                        element.setQuality(qual)
                        element.setHref(href)               
                        element.regenerateKodiTitle()
                                            
                        self.appendLinkInList(element, elementList)                     
                      
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
        return self.getLinks(episodeStreamItem) 
    
    def getLastMovie(self,streamItem=False):
        """
            Method to get all last movie
            @return a list of StreamItem
        """  
        # ___ Initialize the list to return
        elementList = []
        
        href = '/accueil-films'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        
            
        # ___ Get the soup
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.find('div',{'id':'dle-content'}).findAll('div',{ 'class':'movie-item ignore-select short-movie clearfix'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a',{'class':'movie-title'})['href']
                    titleExtract = movie.find('a',{'class':'movie-title'}).text.encode('UTF-8')
                    year = strUtil.getYearFromTitle(titleExtract) 
                    quality = strUtil.getQualityFromTitle(titleExtract)  
                    lang = strUtil.getLangFromTitle(titleExtract)
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    if movie.find('span') is not None:
                        element.setQuality(movie.find('span').text.encode('UTF-8'))             
                    element.setLang(lang)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                    # ___ Get metadatas 
                    metadatas = movie.find('div',{'class':'movie-desc'})
                   
                    metas = metadatas.findAll('div',{'class':'movie-director'})
                    if metas is not None:
                        genres = metas[0].text.encode('UTF-8')
                        genres = genres.replace(metas[0].find('b').text.encode('UTF-8'),'').strip()                     
                        element.setMetadataGenre(genres)                        
                        
                        year = metas[1].text.encode('UTF-8')
                        year = year.replace(metas[1].find('b').text.encode('UTF-8'),'')
                        year = year[len(year)-5:len(year)]
                        element.setMetadataYear(year)
                        
                        lang = metas[2].text.encode('UTF-8')
                        lang = lang.replace(metas[2].find('b').text.encode('UTF-8'),'').strip()
                        
                        element.setLang(lang)
                        
                    overview = metadatas.find('div',{'class':'movie-text'})
                    if overview is not None:
                        element.setMetadataOverview(overview.text.encode('UTF-8'))
                                        
                    # __ Add the element to the list
                    elementList.append(element)      
            
            nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
            nextPage.setIconImage(icons.getIcon('nextpage'))
            nextPage.setType(StreamItem.TYPE_MOVIE)
            nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            nextPage.setSubType(StreamItem.SUBTYPE_LAST)
            nextPage.setPage(int(page)+1)
            elementList.append(nextPage)
            
                    
        return elementList
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        href = '/accueil-series'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        
            
        # ___ Get the soup
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.find('div',{'id':'dle-content'}).findAll('div',{ 'class':'movie-item ignore-select short-movie clearfix'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a',{'class':'movie-title'})['href']
                    titleExtract = movie.find('a',{'class':'movie-title'}).text.encode('UTF-8')
                    year = strUtil.getYearFromTitle(titleExtract) 
                    quality = strUtil.getQualityFromTitle(titleExtract)  
                    lang = strUtil.getLangFromTitle(titleExtract)
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setTvShowName(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    if movie.find('span') is not None:
                        element.setQuality(movie.find('span').text.encode('UTF-8'))             
                    element.setLang(lang)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)                    
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                    # ___ Get metadatas 
                    metadatas = movie.find('div',{'class':'movie-desc'})
                   
                    metas = metadatas.findAll('div',{'class':'movie-director'})
                    if metas is not None:
                        genres = metas[0].text.encode('UTF-8')
                        genres = genres.replace(metas[0].find('b').text.encode('UTF-8'),'').strip()                     
                        element.setMetadataGenre(genres)                        
                        
                        year = metas[1].text.encode('UTF-8')
                        year = year.replace(metas[1].find('b').text.encode('UTF-8'),'')
                        year = year[len(year)-5:len(year)]
                        element.setMetadataYear(year)
                        
                    overview = metadatas.find('div',{'class':'movie-text'})
                    if overview is not None:
                        element.setMetadataOverview(overview.text.encode('UTF-8'))
                                        
                    # __ Add the element to the list
                    elementList.append(element)      
            
            nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
            nextPage.setIconImage(icons.getIcon('nextpage'))
            nextPage.setType(StreamItem.TYPE_TVSHOW)
            nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            nextPage.setSubType(StreamItem.SUBTYPE_LAST)
            nextPage.setPage(int(page)+1)
            elementList.append(nextPage)
            
                    
        return elementList
    
    def getLastAnime(self,streamItem=False):
        """
            Method to get all last anime
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        href = '/accueil-mangas'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        
            
        # ___ Get the soup
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.find('div',{'id':'dle-content'}).findAll('div',{ 'class':'movie-item ignore-select short-movie clearfix'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a',{'class':'movie-title'})['href']
                    titleExtract = movie.find('a',{'class':'movie-title'}).text.encode('UTF-8')
                    year = strUtil.getYearFromTitle(titleExtract) 
                    quality = strUtil.getQualityFromTitle(titleExtract)  
                    lang = strUtil.getLangFromTitle(titleExtract)
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setTvShowName(title)
                    element.setHref(href)                
                    element.setYear(year)             
                    if movie.find('span') is not None:
                        element.setQuality(movie.find('span').text.encode('UTF-8'))             
                    element.setLang(lang)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)                    
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                    # ___ Get metadatas 
                    metadatas = movie.find('div',{'class':'movie-desc'})
                   
                    metas = metadatas.findAll('div',{'class':'movie-director'})
                    if metas is not None:
                        genres = metas[0].text.encode('UTF-8')
                        genres = genres.replace(metas[0].find('b').text.encode('UTF-8'),'').strip()                     
                        element.setMetadataGenre(genres)                        
                        
                        year = metas[1].text.encode('UTF-8')
                        year = year.replace(metas[1].find('b').text.encode('UTF-8'),'')
                        year = year[len(year)-5:len(year)]
                        element.setMetadataYear(year)
                        
                    overview = metadatas.find('div',{'class':'movie-text'})
                    if overview is not None:
                        element.setMetadataOverview(overview.text.encode('UTF-8'))
                                        
                    # __ Add the element to the list
                    elementList.append(element)      
            
            nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
            nextPage.setIconImage(icons.getIcon('nextpage'))
            nextPage.setType(StreamItem.TYPE_TVSHOW)
            nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            nextPage.setSubType(StreamItem.SUBTYPE_LAST)
            nextPage.setPage(int(page)+1)
            elementList.append(nextPage)
            
                    
        return elementList  
    
    def getTopMovie(self,streamItem=False):
        """
            Method to get top movie
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        href = '/top-films'
                   
        # ___ Get the soup
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.findAll('li',{ 'class':'tops-item'})
                
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
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                    # __ Add the element to the list
                    elementList.append(element)      
            
        return elementList
    
    def getTopTvShow(self,streamItem=False):
        """
            Method to get top tv show
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        href = '/top-series'
                   
        # ___ Get the soup
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.findAll('li',{ 'class':'tops-item'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a')['href']
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setTvShowName(title)
                    element.setHref(href) 
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                    # __ Add the element to the list
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
        # ___ Initialize the list to return
        elementList = []
        
    
        # ___ Get the soup
        href = '/accueil'
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.findAll('div',{'class':'side-item side-colored'})[0].findAll('a',{'class':'short1-item clearfix'})
                
                for movie in movies:
                                                   
                    title = movie.find('div',{'class':'short1-title'}).text.encode('UTF-8').strip()
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie['href']                    
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref(href)
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                                        
                    # __ Add the element to the list
                    elementList.append(element)      
            
            
                    
        return elementList
    
    
    def getTopWeekTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
    
        # ___ Get the soup
        href = '/accueil'
        response = self.openPage(href)
        
        if response and response.getcode() == 200:        
            content = response.read()
            soup = BeautifulSoup(content)  
            if soup is not None:
                movies = soup.findAll('div',{'class':'side-item side-colored'})[1].findAll('a',{'class':'short1-item clearfix'})
                
                for movie in movies:
                                                   
                    title = movie.find('div',{'class':'short1-title'}).text.encode('UTF-8').strip()
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie['href']                    
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)        
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setTvShowName(title)
                    element.setHref(href)
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setSourceId(self.ID)  
                    element.setIconImage(movie.find('img')['src'])                    
                    
                                        
                    # __ Add the element to the list
                    elementList.append(element)      
            
            
                    
        return elementList
    
    
    def getTopWeekAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        return []
    
    
    def getExclueMovie(self,streamItem=False):
        """
            Method to get exclu movie
            @return a list of StreamItem
        """
        # ___ Initialize the list to return                    
        return []   
    
    def getMovieList(self,streamItem=False):
        """
            Method to get a list of movie
            @return a list of StreamItem        
        """
        return []
        
    def getTvShowList(self,streamItem=False):
        """
            Method to get a list of tvshow
            @return a list of StreamItem        
        """
        return []
     
    def getAnimeList(self,streamItem=False):
        """
            Method to get a list of anime
            @return a list of StreamItem        
        """
        return []
     
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
    
    def getSettingsXml(self):
        """
            Method to get the xml settings of the current source
        """
        xmlSettingStr = ''
        xmlSettingStr += '<setting label="Mega-Stream" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_megastream_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr