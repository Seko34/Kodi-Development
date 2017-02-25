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
    ID = 6
    
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
                     Source.MENU_MOVIE_TOPVIEW,
                     Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     #Source.MENU_MOVIE_CATEGORY_GENRE
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [
                       Source.MENU_TVSHOW_SEARCH,
                       Source.MENU_TVSHOW_LAST
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
        soup = BeautifulSoup(content)      
                  
        # For every post, get title and topicLink          
        movies = soup.find('div',{'class':'filmcontent'}).findAll('div',{'class':'moviefilm'})
        
        for index in range(0,len(movies)):
            
            movie = movies[index]
            
            title = movie.find('div',{'class':'movief'}).text.encode('UTF-8')
            title = strUtil.unescapeHtml(str(title))
            self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
            href = movie.find('div',{'class':'movief'}).find('a')['href']
            year = strUtil.getYearFromTitle(title) 
            quality = strUtil.getQualityFromTitle(title)  
            lang = strUtil.getLangFromTitle(title)
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
            
            tvshowPattern = re.compile("(http://sokrostream.biz/series)(.*)")
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
        
        return elementList
    
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        get_href = 'search.php?slug='+title
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
        
        get_href = 'search.php?slug='+title
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
        
        elementList = []
        response = self.openPage(tvShowStreamItem.getHref())
        
        if response and response.getcode() == 200:    
            content = response.read()   
            soup = BeautifulSoup(content)  

            # For every post, get title and topicLink          
            movies = soup.findAll('div',{'class':'filmcontent'})[1].findAll('div',{'class':'moviefilm'})
            
            for index in range(0,len(movies)):
                
                movie = movies[index]                
                seasonText = movie.find('div',{'class':'movief'}).text.encode('UTF-8')
                
                seasonPattern = re.compile("(.*)(Saison )(.*)")
                match = seasonPattern.match(seasonText)
                if match is not None:                    
                
                    # __ Create the element
                    href = movie.find('div',{'class':'movief'}).find('a')['href'].encode('UTF-8')
                    element = tvShowStreamItem.copy()
                    element.setSeason(match.group(3))             
                    element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                    element.setHref(href)
                    element.determineSeasonTitle()
                    element.setIconImage(movie.find('img')['src'])
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
        
        
        elementList = []
        response = self.openPage(episodeStreamItem.getHref())
        
        if response and response.getcode() == 200:    
            content = response.read()   
            soup = BeautifulSoup(content)      

            # For every post, get title and topicLink          
            movies = soup.findAll('div',{'class':'filmcontent'})[1].findAll('div',{'class':'moviefilm2'})
            
            for index in range(0,len(movies)):
                
                movie = movies[index]
                
                episodeText = movie.find('div',{'class':'movief2'}).text.encode('UTF-8')
                episodePattern = re.compile("(Episode )(.*)")
                match = episodePattern.match(episodeText)
                if match is not None:                    
                
                    # __ Create the element
                    href = movie.find('div',{'class':'movief2'}).find('a')['href'].encode('UTF-8')
                    element = episodeStreamItem.copy()
                    element.setEpisode(match.group(2))             
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
    
    def getLink(self,id,streamItem):    
        """
            Method to get link
            @param id: the id of the link
            @param streamItem : the current StreamItem
            @return a list of StreamItem
        """  
        element = None  
        postHref = streamItem.getHref()
        param = {'levideo':str(id)}
        headers = copy.copy(webUtil.HEADER_CFG)
        headers['Referer'] = streamItem.getHref()
        headers['Host'] = 'sokrostream.biz'
        headers['Origin'] = 'http://sokrostream.biz'
        
        response = self.postPage(postHref, param,headers=headers)
        
        if response and response.getcode() == 200:   
            content = response.read()
            soup = BeautifulSoup(content) 
            
            # __ Case of iFrame
            link = soup.find('div',{'class':'bgvv'}).find('iframe')
            if link is not None and link['src'].startswith('http://sokrostrem.xyz/video.php?p'):
                headers = copy.copy(webUtil.HEADER_CFG)
                headers['Referer'] = streamItem.getHref()
                headers['Host'] = 'sokrostrem.xyz'
                headers['Upgrade-Insecure-Requests'] = '1'
                response2 = self.openPage(link['src'],buildHref=False,cHeaders=headers)
                if response2 and response2.getcode() == 200:   
                    content2 = response2.read()
                    soup2 = BeautifulSoup(content2)
                    content = soup2.find('meta')['content']
                    contentPattern = re.compile('(.*)(url=)(.*)')
                    match = contentPattern.match(content)
                    if match is not None :
                        href = match.group(3)
                        if href is not None and not href.startswith('http://sokrostream'):
                            # __ Create the element                       
                            element = streamItem.copy()
                            element.setAction(StreamItem.ACTION_PLAY)
                            element.setType(StreamItem.TYPE_STREAMING_LINK)
                            element.setHref(href)           
                            element.regenerateKodiTitle()
                            
            elif link is not None and not link['src'].startswith('http://sokrostream'):
                # ___ Case of streaming link
                href = link['src'].encode('UTF-8')
                href = self.formatLink(href)
                # __ Create the element                       
                element = streamItem.copy()
                element.setAction(StreamItem.ACTION_PLAY)
                element.setType(StreamItem.TYPE_STREAMING_LINK)
                element.setHref(href)                 
                element.regenerateKodiTitle()
                
            elif link is not None and link['src'].startswith('http://sokrostream'):
                # ___ Case of download link
                response = self.openPage(link['src'])
                if response and response.getcode() == 200:   
                    content = response.read()
                    soup = BeautifulSoup(content) 
                    link = soup.find('a',{'class':'button_upload green'})  
                    if link is not None:  
                        href = link['href'].encode('UTF-8')
                        href = self.formatLink(href)
                        # __ Create the element                       
                        element = streamItem.copy()
                        element.setAction(StreamItem.ACTION_PLAY)
                        element.setType(StreamItem.TYPE_STREAMING_LINK)
                        element.setHref(href)                 
                        element.regenerateKodiTitle()  
            
            
        return element
    
    def getLinks(self,streamItem):       
        """
            Method to get all links
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        
        soupI = self._initOpenPage(streamItem)
        links = soupI.findAll('input',{'name':'levideo'})
        for link in links:
            id = link['value']
            linkItem = self.getLink(id,streamItem)
            if linkItem is not None:
                elementList.append(linkItem)
                
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
                movies = soup.find('div',{'class':'filmcontent'}).findAll('div',{ 'class':'moviefilm'})
                
                for movie in movies:
                                                   
                    title = movie.find('img')['alt'].encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    href = movie.find('a')['href']
                    year = strUtil.getYearFromTitle(title) 
                    quality = movie.find('div',{'class':re.compile('(movies)(.*)')}).text.encode('UTF-8')
                    langClass = movie.find('span')['class']
                    lang = None
                    subtitle = None
                    if langClass == 'tr-dublaj':
                        lang = 'FR'
                    elif langClass == 'tr-altyazi':
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
                    element.setIconImage(movie.find('img')['src'])                    
                                                            
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
        # ___ Initialize the list to return
        elementList = []
        
        href = '/'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'page/' +streamItem.getPage()
            page = streamItem.getPage()
        else:
            streamItem = StreamItem()
            streamItem.setPage(0)
            streamItem.setType(StreamItem.TYPE_MOVIE)
            streamItem.setSubType(StreamItem.SUBTYPE_LAST)
            
        # ___ Get the response
        response = self.openPage(href)           
                   
        # ___ Return the movie list 
        return self.getMovieContent(streamItem,page,response)
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        href = '/categories/series-tv'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        else:
            streamItem = StreamItem()
            streamItem.setPage(0)
            streamItem.setType(StreamItem.TYPE_TVSHOW)
            streamItem.setSubType(StreamItem.SUBTYPE_LAST)
            
        # ___ Get the response
        response = self.openPage(href)           
                   
        # ___ Return the movie list 
        return self.getTvShowContent(streamItem,page,response)
    
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
        href = '/films-les-mieux-notes-2'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        else:
            streamItem = StreamItem()
            streamItem.setPage(0)
            streamItem.setType(StreamItem.TYPE_MOVIE)
            streamItem.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            
        # ___ Get the response
        response = self.openPage(href)           
                   
        # ___ Return the movie list 
        return self.getMovieContent(streamItem,page,response)
    
    
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
        # ___ Initialize the list to return
        elementList = []
        
        href = '/les-films-les-plus-vues-2'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        else:
            streamItem = StreamItem()
            streamItem.setPage(0)
            streamItem.setType(StreamItem.TYPE_MOVIE)
            streamItem.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            
        # ___ Get the response
        response = self.openPage(href)           
                   
        # ___ Return the movie list 
        return self.getMovieContent(streamItem,page,response)
    
    
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
        
        href = '/les-films-les-plus-commentes-2'
        page = 0
        # ___ Get the page
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            href = href +'/page/' +streamItem.getPage()
            page = streamItem.getPage()
        else:
            streamItem = StreamItem()
            streamItem.setPage(0)
            streamItem.setType(StreamItem.TYPE_MOVIE)
            streamItem.setSubType(StreamItem.SUBTYPE_TOP_WEEK)
            
        # ___ Get the response
        response = self.openPage(href)           
                   
        # ___ Return the movie list 
        return self.getMovieContent(streamItem,page,response)
    
    
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
        xmlSettingStr += '<setting label="Sokrostream" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_sokrostream_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr