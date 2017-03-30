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
import urllib2
import traceback
import webUtil
import sys 
import urllib
import cookielib
import kodiUtil
import re
import icons
import constant as constant
from item import StreamItem
from logger import Logger
from BeautifulSoup import BeautifulSoup

if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:    
    import miscFunctions as miscFunctions
    

class SmartRedirectHandler(urllib2.HTTPRedirectHandler):     
    def http_error_301(self, req, fp, code, msg, headers):
        result = urllib2.HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)      
        result.status = code                           
        return result                                       

    def http_error_302(self, req, fp, code, msg, headers):   
        result = urllib2.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)              
        result.status = code                                
        return result 
            
            
# ____________________        C L A S S          ____________________
class streamingSourceTemplate(object):
    
    
    # ___ The source ID
    ID = -1
    
    # ___ The name of the source
    NAME = ''
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://www.dpstream.net/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','Source')
       
    
    # MAIN MENU
    MAIN_MENU_MOVIE_HD        = 10
    MAIN_MENU_MOVIE           = 11
    MAIN_MENU_TVSHOW          = 12
    MAIN_MENU_ANIME           = 13
    MAIN_MENU_SHOW            = 14
    MAIN_MENU_DOCUMENTARY     = 15
    MAIN_MENU_OPT = [MAIN_MENU_MOVIE_HD,
                     MAIN_MENU_MOVIE,
                     MAIN_MENU_TVSHOW,
                     MAIN_MENU_ANIME,
                     MAIN_MENU_SHOW,
                     MAIN_MENU_DOCUMENTARY]
    
    # MOVIE MENU
    MENU_MOVIE_SEARCH         = 20
    MENU_MOVIE_LAST           = 21
    MENU_MOVIE_TOPVIEW        = 22
    MENU_MOVIE_TOPWEEK        = 23
    MENU_MOVIE_TOPRATE        = 24
    MENU_MOVIE_EXCLUE         = 25
    MENU_MOVIE_LIST           = 26
    MENU_MOVIE_CATEGORY_ALPHA = 27
    MENU_MOVIE_CATEGORY_GENRE = 28
    MENU_MOVIE_SRCH_WATAMOVIE = 29
    MENU_MOVIE_OPT = [MENU_MOVIE_SEARCH,
                     MENU_MOVIE_SRCH_WATAMOVIE,
                     MENU_MOVIE_LAST,
                     MENU_MOVIE_TOPVIEW,
                     MENU_MOVIE_TOPWEEK,
                     MENU_MOVIE_TOPRATE,
                     MENU_MOVIE_EXCLUE,
                     MENU_MOVIE_LIST,
                     MENU_MOVIE_CATEGORY_ALPHA,
                     MENU_MOVIE_CATEGORY_GENRE]
    
    # MOVIE HD MENU
    MENU_MOVIE_HD_SEARCH         = 30
    MENU_MOVIE_HD_LAST           = 31
    MENU_MOVIE_HD_TOPVIEW        = 32
    MENU_MOVIE_HD_TOPWEEK        = 33
    MENU_MOVIE_HD_TOPRATE        = 34
    MENU_MOVIE_HD_EXCLUE         = 35
    MENU_MOVIE_HD_LIST           = 36
    MENU_MOVIE_HD_CATEGORY_ALPHA = 37
    MENU_MOVIE_HD_CATEGORY_GENRE = 38
    MENU_MOVIE_HD_OPT = [MENU_MOVIE_HD_SEARCH,
                     MENU_MOVIE_HD_LAST,
                     MENU_MOVIE_HD_TOPVIEW,
                     MENU_MOVIE_HD_TOPWEEK,
                     MENU_MOVIE_HD_TOPRATE,
                     MENU_MOVIE_HD_EXCLUE,
                     MENU_MOVIE_HD_LIST,
                     MENU_MOVIE_HD_CATEGORY_ALPHA,
                     MENU_MOVIE_HD_CATEGORY_GENRE]
        
    # TV SHOW MENU
    MENU_TVSHOW_SEARCH         = 40
    MENU_TVSHOW_LAST           = 41
    MENU_TVSHOW_TOPVIEW        = 42
    MENU_TVSHOW_TOPWEEK        = 43
    MENU_TVSHOW_TOPRATE        = 44
    MENU_TVSHOW_TOPRATE        = 45
    MENU_TVSHOW_LIST           = 46
    MENU_TVSHOW_CATEGORY_ALPHA = 47
    MENU_TVSHOW_CATEGORY_GENRE = 48
    MENU_TVSHOW_OPT = [MENU_TVSHOW_SEARCH,
                     MENU_TVSHOW_LAST,
                     MENU_TVSHOW_TOPVIEW,
                     MENU_TVSHOW_TOPWEEK,
                     MENU_TVSHOW_TOPRATE,
                     MENU_TVSHOW_LIST,
                     MENU_TVSHOW_CATEGORY_ALPHA,
                     MENU_TVSHOW_CATEGORY_GENRE]
    
    # ANIME MENU    
    MENU_ANIME_SEARCH         = 50
    MENU_ANIME_LAST           = 51
    MENU_ANIME_TOPVIEW        = 52
    MENU_ANIME_TOPWEEK        = 53
    MENU_ANIME_TOPRATE        = 54
    MENU_ANIME_LIST           = 55
    MENU_ANIME_CATEGORY_ALPHA = 56
    MENU_ANIME_CATEGORY_GENRE = 57
    MENU_ANIME_OPT = [MENU_ANIME_SEARCH,
                     MENU_ANIME_LAST,
                     MENU_ANIME_TOPVIEW,
                     MENU_ANIME_TOPWEEK,
                     MENU_ANIME_TOPRATE,
                     MENU_ANIME_LIST,
                     MENU_ANIME_CATEGORY_ALPHA,
                     MENU_ANIME_CATEGORY_GENRE]
    
     
    # SHOW MENU
    MENU_SHOW_SEARCH         = 60
    MENU_SHOW_LAST           = 61
    MENU_SHOW_TOPVIEW        = 62
    MENU_SHOW_TOPWEEK        = 63
    MENU_SHOW_TOPRATE        = 64
    MENU_SHOW_CATEGORY_ALPHA = 65
    MENU_SHOW_CATEGORY_GENRE = 66
    MENU_SHOW_OPT = [MENU_SHOW_SEARCH,
                     MENU_SHOW_LAST,
                     MENU_SHOW_TOPVIEW,
                     MENU_SHOW_TOPWEEK,
                     MENU_SHOW_TOPRATE,
                     MENU_SHOW_CATEGORY_ALPHA,
                     MENU_SHOW_CATEGORY_GENRE]
    
    # DOCUMENTARY MENU
    MENU_DOCUMENTARY_SEARCH         = 70
    MENU_DOCUMENTARY_LAST           = 71
    MENU_DOCUMENTARY_TOPVIEW        = 72
    MENU_DOCUMENTARY_TOPWEEK        = 73
    MENU_DOCUMENTARY_TOPRATE        = 74
    MENU_DOCUMENTARY_CATEGORY_ALPHA = 75
    MENU_DOCUMENTARY_CATEGORY_GENRE = 76
    MENU_DOCUMENTARY_OPT = [MENU_DOCUMENTARY_SEARCH,
                     MENU_DOCUMENTARY_LAST,
                     MENU_DOCUMENTARY_TOPVIEW,
                     MENU_DOCUMENTARY_TOPWEEK,
                     MENU_DOCUMENTARY_TOPRATE,
                     MENU_DOCUMENTARY_CATEGORY_ALPHA,
                     MENU_DOCUMENTARY_CATEGORY_GENRE]
    """
        Template class for streaming source
    """
    def __init__(self):
        """
            Constructor
        """        
        # ___ We active cookies support for urllib2
        self.cookiejar = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar),SmartRedirectHandler())
        
        # ___ Init service values        
        self.serviceMovieValues = []
        if self.MENU_MOVIE_LAST in self.MENU_MOVIE_OPT:
            self.serviceMovieValues.append(self.MENU_MOVIE_LAST)
        if self.MENU_MOVIE_TOPVIEW in self.MENU_MOVIE_OPT:
            self.serviceMovieValues.append(self.MENU_MOVIE_TOPVIEW)
        if self.MENU_MOVIE_TOPWEEK in self.MENU_MOVIE_OPT:
            self.serviceMovieValues.append(self.MENU_MOVIE_TOPWEEK)
        if self.MENU_MOVIE_TOPRATE in self.MENU_MOVIE_OPT:
            self.serviceMovieValues.append(self.MENU_MOVIE_TOPRATE)
        if self.MENU_MOVIE_EXCLUE in self.MENU_MOVIE_OPT:
            self.serviceMovieValues.append(self.MENU_MOVIE_EXCLUE)
            
        
        self.serviceTvShowValues = []
        if self.MENU_TVSHOW_LAST in self.MENU_TVSHOW_OPT:
            self.serviceTvShowValues.append(self.MENU_TVSHOW_LAST)
        if self.MENU_TVSHOW_TOPVIEW in self.MENU_TVSHOW_OPT:
            self.serviceTvShowValues.append(self.MENU_TVSHOW_TOPVIEW)
        if self.MENU_TVSHOW_TOPWEEK in self.MENU_TVSHOW_OPT:
            self.serviceTvShowValues.append(self.MENU_TVSHOW_TOPWEEK)
        if self.MENU_TVSHOW_TOPRATE in self.MENU_TVSHOW_OPT:
            self.serviceTvShowValues.append(self.MENU_TVSHOW_TOPRATE)
        if self.MENU_MOVIE_EXCLUE in self.MENU_TVSHOW_OPT:
            self.serviceTvShowValues.append(self.MENU_MOVIE_EXCLUE)
    
    def getId(self):
        return self.ID
    
    def getName(self):
        return self.NAME
        
    def buildHref(self, href=None):
        """
            Method to build the url of a page
            href will be concatenated with 'WEB_PAGE_BASE'
            
            @param href: href value of a link
            @return the complete URL with 'http://www.dpstream.net/'
                    If the href is null, the method return only http://www.dpstream.net/
        """
        if href is None :
            url = self.WEB_PAGE_BASE
        else:
            if not href.startswith(self.WEB_PAGE_BASE):
                if href.startswith('/'):
                    url = self.WEB_PAGE_BASE + href[1:]                    
                else:
                    url = self.WEB_PAGE_BASE + href
            else:
                url = href     
                
        self.__LOGGER__.log("The build url is: " + url, xbmc.LOGINFO)
        return url
    
    def isLogin(self):
        return True
    
    def login(self):
        pass
    
    def openPage(self, href=None, byPassLogin=False, buildHref=True, cHeaders=webUtil.HEADER_CFG):
        """
            Method to open a page 
            @param href: href value of a link
            @param byPassLogin: If byPassLogin is equal to "True", we just open page without verification of login
            @return the response of the request
        """ 
        
        # ___ If it's necessary, login in the web site
        if not byPassLogin and not self.isLogin():
            self.login()
            
        if buildHref:
            request = urllib2.Request(self.buildHref(href), headers=cHeaders)
        else:            
            request = urllib2.Request(href, headers=cHeaders)
        response = None
        
        try: 
            response = self.urlOpener.open(request)
        except urllib2.HTTPError as e:
            response = e 
        except:
            traceback.print_exc()
            self.__LOGGER__.log('Error during opening a web page on '+self.NAME,xbmc.LOGERROR)
            #miscFunctions.displayNotification('Error during opening a web page on '+self.NAME)
            
        return response
     
    def postPage(self, href=None, data=None, byPassLogin=False, headers=False):
        """
            Method to open a page 
            @param href: href value of a link
            @param data: data to post
            @param byPassLogin: If byPassLogin is equal to "True", we just open page without verification of login
            @return the response of the request
        """  
        # ___ If it's necessary, login in the web site
        if not byPassLogin and not self.isLogin():
            self.login()
            
        if not headers:
            request = urllib2.Request(self.buildHref(href), urllib.urlencode(data), headers=webUtil.HEADER_CFG)
        else:           
            request = urllib2.Request(self.buildHref(href), urllib.urlencode(data), headers=headers)
        response = None
        
        try: 
            response = self.urlOpener.open(request)            
        except:
            self.__LOGGER__.log('Error during POST message on '+self.NAME,xbmc.LOGERROR)
            self.__LOGGER__.log('POST DATA : '+str(data),xbmc.LOGERROR)
            traceback.print_exc()
            #miscFunctions.displayNotification('Error during POST message on '+self.NAME)
        return response
    
    def _initOpenPage(self,streamItem):       
        # ___ Init soup
        soup = None
        # ___ Open the page
        response = self.openPage(streamItem.getHref())
        
        if response:           
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)                
            # ___ Close the connection
            response.close() 
                          
        else:
            #miscFunctions.displayNotification('Unable to open page in ' + self.getName())                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(streamItem.getHref()) + ')', xbmc.LOGERROR)
        
        
        return soup
     
    def formatLink(self,url):
        """
            Format streaming link for urlresovler
            
            @param url: the url to format
            @return the url formatted 
        """
        if url.startswith('//'):
            url = 'http:'+url
        # ___ Case of Exashare
        patternExashare = re.compile('(http://www.exashare.com/)(embed-)(.*)(-)(.*\.html)')
        match = patternExashare.match(url)
        if match is not None:      
            url = match.group(1).encode('UTF-8')+match.group(3).encode('UTF-8')            
        
        # ___ Case of Purevid
        patternPurevid = re.compile('(http://www.purevid.com/)(\\?m=embed&id=)(.*)')
        match = patternPurevid.match(url)
        if match is not None:      
            url = match.group(1).encode('UTF-8')+'v/'+match.group(3).encode('UTF-8')+'/'
                
        # ___ Others cases
        else:
            if not url.endswith("/"):
                url = url + '/'
            
        return url
            
    def appendLinkInList(self,streamItem,elementList):
        """
            Method to append a link in a list if the link is not already in the list
            @param streamItem : the StreaItem to add
            @param elementList: the list to append
        """
        for el in elementList:
            # ___ If the link is in the list, return the list as it is.
            if  int(streamItem.getType()) == StreamItem.TYPE_STREAMING_LINK and el.getPlayableUrl() == streamItem.getPlayableUrl():
                return elementList 
            elif el.getHref() == streamItem.getHref():
                return elementList
        # ___ Else add the link       
        elementList.append(streamItem)
        return elementList    
    
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        return []
    
    def searchHdMovie(self, title):
        """
            Method to search a hd movie
            @return a list of StreamItem
        """
        return []
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        return []
    
    def searchAnime(self, title):
        """
            Method to search a anime
            @return a list of StreamItem
        """
        return []
    
    def searchShow(self, title):
        """
            Method to search a show
            @return a list of StreamItem
        """
        return []
    
    def searchDocumentary(self, title):
        """
            Method to search a documentary
            @return a list of StreamItem
        """
        return []
    
    def getTvShowSeasons(self, tvShowStreamItem):
        """
            Method to get the seasons list of a tv show
            @return a list of StreamItem
        """
        return []    
    
    def getAnimeSeasons(self, tvShowStreamItem):
        """
            Method to get the seasons list of an anime
            @return a list of StreamItem
        """
        return []
    
    def getTvShowEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        return []
    
    def getAnimeEpisodes(self, episodeStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        return []
    
    def getMovieLink(self,movieStreamItem):
        """
            Method to get all links of a movie
            @return a list of StreamItem
        """
        return []
    
    def getTvShowEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        return []    
    
    def getAnimeEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        return []   
     
    def getShowLink(self,movieStreamItem):
        """
            Method to get all links of a show
            @return a list of StreamItem
        """
        return []   
     
    def getDocumentaryLink(self,movieStreamItem):
        """
            Method to get all links of a documentary
            @return a list of StreamItem
        """
        return []
    
    def getLastMovie(self,streamItem=False):
        """
            Method to get all last movie
            @return a list of StreamItem
        """
        return []
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        return []
    
    def getLastAnime(self,streamItem=False):
        """
            Method to get all last anime
            @return a list of StreamItem
        """
        return []  
    
    def getLastShow(self,streamItem=False):
        """
            Method to get all last show
            @return a list of StreamItem
        """
        return []  
    
    def getLastDocumentary(self,streamItem=False):
        """
            Method to get all last documentary
            @return a list of StreamItem
        """
        return []  
    
    def getTopMovie(self,streamItem=False):
        """
            Method to get top movie
            @return a list of StreamItem
        """
        return []
    
    
    def getTopTvShow(self,streamItem=False):
        """
            Method to get top tv show
            @return a list of StreamItem
        """
        return []
    
    
    def getTopAnime(self,streamItem=False):
        """
            Method to get top anime
            @return a list of StreamItem
        """
        return []
    
    def getTopShow(self,streamItem=False):
        """
            Method to get top show
            @return a list of StreamItem
        """
        return []
    
    def getTopDocumentary(self,streamItem=False):
        """
            Method to get top documentary
            @return a list of StreamItem
        """
        return []
    
    def getTopWeekMovie(self,streamItem=False):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        return []
    
    
    def getTopWeekTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        return []
    
    
    def getTopWeekAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        return []
        
    def getTopWeekShow(self,streamItem=False):
        """
            Method to get top week show
            @return a list of StreamItem
        """
        return []   
     
    def getTopWeekDocumentary(self,streamItem=False):
        """
            Method to get top week documentary
            @return a list of StreamItem
        """
        return []
    
    def getMostViewMovie(self,streamItem=False):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        return []
    
    
    def getMostViewTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        return []
    
    
    def getMostViewAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        return []
    
    def getMostViewShow(self,streamItem=False):
        """
            Method to get top week show
            @return a list of StreamItem
        """
        return []    
    
    def getExclueMovie(self,streamItem=False):
        """
            Method to get exclu movie
            @return a list of StreamItem
        """
        return []    
    
    def getMostViewDocumentary(self,streamItem=False):
        """
            Method to get top week Documentary
            @return a list of StreamItem
        """
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
    
    def getAlphabeticMovieHDList(self,streamItem):
        
        """
            Method to get an alphabatic list of movie hd
            @return a list of StreamItem
        """
        return []
    
    def getAlphabeticMovieList(self,streamItem):
        
        """
            Method to get an alphabatic list of movie
            @return a list of StreamItem
        """
        return []
    def getAlphabeticTvShowList(self,streamItem):
        
        """
            Method to get an alphabatic list of tv show
            @return a list of StreamItem
        """
        return []
    
    def getAlphabeticAnimeList(self,streamItem):
        
        """
            Method to get an alphabatic list of anime
            @return a list of StreamItem
        """
        return []
    
    
    
    def getAlphabeticShowList(self,streamItem):
        
        """
            Method to get an alphabatic list of show
            @return a list of StreamItem
        """
        return []
    
    def getAlphabeticDocumentaryList(self,streamItem):
        
        """
            Method to get an alphabatic list of documentary
            @return a list of StreamItem
        """
        return []
    
    def getMovieListByGenre(self,streamItem):
        
        """
            Method to get a list of movie by genre
            @return a list of StreamItem
        """
        return []
    
    def build_menu(self):
        """
            Method to display the main menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Movies HD
        if self.MAIN_MENU_MOVIE_HD in self.MAIN_MENU_OPT:  
            movieHD = StreamItem(constant.__addon__.getLocalizedString(40030))
            movieHD.setIconImage(icons.getIcon('movie',True)) 
            movieHD.setType(StreamItem.TYPE_MOVIE_HD)
            movieHD.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            movieHD.addListItemToDirectory()
        
       
        # Movie
        if self.MAIN_MENU_MOVIE in self.MAIN_MENU_OPT:  
            movie = StreamItem(constant.__addon__.getLocalizedString(40031))
            movie.setIconImage(icons.getIcon('movie')) 
            movie.setType(StreamItem.TYPE_MOVIE)
            movie.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            movie.addListItemToDirectory()
        
        # TV Show
        if self.MAIN_MENU_TVSHOW in self.MAIN_MENU_OPT:  
            tvshow = StreamItem(constant.__addon__.getLocalizedString(40032))
            tvshow.setIconImage(icons.getIcon('tvshow')) 
            tvshow.setType(StreamItem.TYPE_TVSHOW)
            tvshow.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            tvshow.addListItemToDirectory()
        
        # Show
        if self.MAIN_MENU_SHOW in self.MAIN_MENU_OPT:  
            show = StreamItem(constant.__addon__.getLocalizedString(40033))
            show.setIconImage(icons.getIcon('show')) 
            show.setType(StreamItem.TYPE_SHOW)
            show.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            show.addListItemToDirectory()
        
        # Documentary 
        
        if self.MAIN_MENU_DOCUMENTARY in self.MAIN_MENU_OPT:     
            documentary = StreamItem(constant.__addon__.getLocalizedString(40034))
            documentary.setIconImage(icons.getIcon('documentary')) 
            documentary.setType(StreamItem.TYPE_DOCUMENTARY)
            documentary.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            documentary.addListItemToDirectory()
         
        # Anime
        if self.MAIN_MENU_ANIME in self.MAIN_MENU_OPT:  
            anime = StreamItem(constant.__addon__.getLocalizedString(40035))
            anime.setIconImage(icons.getIcon('animes')) 
            anime.setType(StreamItem.TYPE_ANIME)
            anime.setAction(StreamItem.ACTION_DISPLAY_TYPE_MENU)
            anime.addListItemToDirectory()
        
        # Download Manager
        if( constant.__addon__.getSetting('downloader_module') == '2'):        
            dlmanager = StreamItem(constant.__addon__.getLocalizedString(40038))
            dlmanager.setIconImage(icons.getIcon('downloads')) 
            dlmanager.setType(StreamItem.TYPE_MENU)
            dlmanager.setAction(StreamItem.ACTION_DISPLAY_DOWNLOAD_MANAGER)
            dlmanager.addListItemToDirectory()
         
        
        # Menu Settings
        menuSettings = StreamItem(constant.__addon__.getLocalizedString(40039))
        menuSettings.setIconImage(icons.getIcon('settings')) 
        menuSettings.setType(StreamItem.TYPE_MENU)
        menuSettings.setAction(StreamItem.ACTION_DISPLAY_MENU_SETTINGS)
        menuSettings.addListItemToDirectory()
        
        
        # Resolver Settings
        #resolverSettings = StreamItem(constant.__addon__.getLocalizedString(40037))
        #resolverSettings.setIconImage(constant.__coreAddonDir__+'/resources/media/urlresolver.png') 
        #resolverSettings.setType(StreamItem.TYPE_SETTINGS)
        #resolverSettings.setAction(StreamItem.ACTION_DISPLAY_URLRESOLVER_SETTINGS)
        #resolverSettings.addListItemToDirectory()
            
        # Settings
        #menuSettings = StreamItem(constant.__addon__.getLocalizedString(40039))
        #menuSettings.setIconImage(constant.__coreAddonDir__+'/resources/media/urlresolver.png') 
        #menuSettings.setType(StreamItem.TYPE_SETTINGS)
        #menuSettings.setAction(StreamItem.ACTION_DISPLAY_SETTINGS)
        #menuSettings.addListItemToDirectory()
        
    
        # Test
        #menuTest = StreamItem("TEST")
        #menuTest.setType(StreamItem.TYPE_DEFAULT)
        #menuTest.setAction(StreamItem.ACTION_TEST)
        #menuTest.addListItemToDirectory() 
       
        kodiUtil.endOfDirectory()
        
        
    
        
    def build_movie_menu(self):
        """
            Method to display the default movie menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search movie
        if self.MENU_MOVIE_SEARCH in self.MENU_MOVIE_OPT and constant.__addon__.getSetting('only_global_search') == 'false':  
            search = StreamItem(constant.__addon__.getLocalizedString(60061))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_MOVIE)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
            
        # Global Search movie
        if constant.__addon__.getSetting('use_global_search') == 'true':  
            search = StreamItem(constant.__addon__.getLocalizedString(60062))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_MOVIE)
            search.setAction(StreamItem.ACTION_GLOBAL_SEARCH)
            search.addListItemToDirectory()
        
        # Watamovie search
        if constant.__addon__.getSetting('use_watamovie') == 'true':  
            search = StreamItem(constant.__addon__.getLocalizedString(60100))
            search.setIconImage(icons.getIcon('watamovie')) 
            search.setType(StreamItem.TYPE_MOVIE)
            search.setAction(StreamItem.ACTION_SEARCH_WATAMOVIE)
            search.addListItemToDirectory()
            
        # Exclue Movie
        if self.MENU_MOVIE_EXCLUE in self.MENU_MOVIE_OPT:  
            lastMovie = StreamItem(constant.__addon__.getLocalizedString(60080))
            lastMovie.setIconImage(icons.getIcon('exclues')) 
            lastMovie.setType(StreamItem.TYPE_MOVIE)
            lastMovie.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            lastMovie.setSubType(StreamItem.SUBTYPE_EXCLUE)
            lastMovie.addListItemToDirectory()
           
        # Last Movie
        if self.MENU_MOVIE_LAST in self.MENU_MOVIE_OPT:  
            lastMovie = StreamItem(constant.__addon__.getLocalizedString(60010))
            lastMovie.setIconImage(icons.getIcon('news')) 
            lastMovie.setType(StreamItem.TYPE_MOVIE)
            lastMovie.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            lastMovie.setSubType(StreamItem.SUBTYPE_LAST)
            lastMovie.addListItemToDirectory()
            
        # Most view
        if self.MENU_MOVIE_TOPVIEW in self.MENU_MOVIE_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(60020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_MOVIE)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top week
        if self.MENU_MOVIE_TOPWEEK in self.MENU_MOVIE_OPT: 
            topWeek = StreamItem(constant.__addon__.getLocalizedString(60030))
            topWeek.setIconImage(icons.getIcon('topweek')) 
            topWeek.setType(StreamItem.TYPE_MOVIE)
            topWeek.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topWeek.setSubType(StreamItem.SUBTYPE_TOP_WEEK)
            topWeek.addListItemToDirectory()
        
        # Top rate
        if self.MENU_MOVIE_TOPRATE in self.MENU_MOVIE_OPT: 
            topRate = StreamItem(constant.__addon__.getLocalizedString(60040))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_MOVIE)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # List
        if self.MENU_MOVIE_LIST in self.MENU_MOVIE_OPT: 
            topRate = StreamItem(constant.__addon__.getLocalizedString(60090))
            topRate.setIconImage(icons.getIcon('news')) 
            topRate.setType(StreamItem.TYPE_MOVIE)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_LIST)
            topRate.addListItemToDirectory()
        
        # Categorie alphabetics
        if self.MENU_MOVIE_CATEGORY_ALPHA in self.MENU_MOVIE_OPT: 
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(60051))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_MOVIE)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
        
        # Categorie genre
        if self.MENU_MOVIE_CATEGORY_GENRE in self.MENU_MOVIE_OPT: 
            genreCat = StreamItem(constant.__addon__.getLocalizedString(60070))
            genreCat.setIconImage(icons.getIcon('bygenre')) 
            genreCat.setType(StreamItem.TYPE_MOVIE)
            genreCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            genreCat.setSubType(StreamItem.SUBTYPE_GENRE)
            genreCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()
        
    def build_movie_hd_menu(self):
        """
            Method to display the default movie hd menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search hd movie
        if self.MENU_MOVIE_HD_SEARCH in self.MENU_MOVIE_HD_OPT and constant.__addon__.getSetting('only_global_search') == 'false':   
            search = StreamItem(constant.__addon__.getLocalizedString(60060))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_MOVIE_HD)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
            
        # Global search
        if constant.__addon__.getSetting('use_global_search') == 'true':  
            search = StreamItem(constant.__addon__.getLocalizedString(60062))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_MOVIE_HD)
            search.setAction(StreamItem.ACTION_GLOBAL_SEARCH)
            search.addListItemToDirectory()
            
        # Exclue Movie
        if self.MENU_MOVIE_HD_EXCLUE in self.MENU_MOVIE_OPT:  
            lastMovie = StreamItem(constant.__addon__.getLocalizedString(60080))
            lastMovie.setIconImage(icons.getIcon('exclues')) 
            lastMovie.setType(StreamItem.TYPE_MOVIE_HD)
            lastMovie.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            lastMovie.setSubType(StreamItem.SUBTYPE_EXCLUE)
            lastMovie.addListItemToDirectory()
           
        # Last Movie
        if self.MENU_MOVIE_HD_LAST in self.MENU_MOVIE_HD_OPT:  
            lastMovie = StreamItem(constant.__addon__.getLocalizedString(60010))
            lastMovie.setIconImage(icons.getIcon('news')) 
            lastMovie.setType(StreamItem.TYPE_MOVIE_HD)
            lastMovie.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            lastMovie.setSubType(StreamItem.SUBTYPE_LAST)
            lastMovie.addListItemToDirectory()
            
        # Most view
        if self.MENU_MOVIE_HD_TOPVIEW in self.MENU_MOVIE_HD_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(60020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_MOVIE_HD)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top week
        if self.MENU_MOVIE_HD_TOPWEEK in self.MENU_MOVIE_HD_OPT:  
            topWeek = StreamItem(constant.__addon__.getLocalizedString(60030))
            topWeek.setIconImage(icons.getIcon('topweek')) 
            topWeek.setType(StreamItem.TYPE_MOVIE_HD)
            topWeek.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topWeek.setSubType(StreamItem.SUBTYPE_TOP_WEEK)
            topWeek.addListItemToDirectory()
        
        # Top rate
        if self.MENU_MOVIE_HD_TOPRATE in self.MENU_MOVIE_HD_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(60040))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_MOVIE_HD)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # List
        if self.MENU_MOVIE_HD_LIST in self.MENU_MOVIE_HD_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(60090))
            topRate.setIconImage(icons.getIcon('news')) 
            topRate.setType(StreamItem.TYPE_MOVIE_HD)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_LIST)
            topRate.addListItemToDirectory()
        
        # Categorie alphabetics
        if self.MENU_MOVIE_HD_CATEGORY_ALPHA in self.MENU_MOVIE_HD_OPT:  
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(60050))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_MOVIE_HD)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
        
        # Categorie genre
        if self.MENU_MOVIE_HD_CATEGORY_GENRE in self.MENU_MOVIE_HD_OPT:  
            genreCat = StreamItem(constant.__addon__.getLocalizedString(60070))
            genreCat.setIconImage(icons.getIcon('bygenre')) 
            genreCat.setType(StreamItem.TYPE_MOVIE_HD)
            genreCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            genreCat.setSubType(StreamItem.SUBTYPE_GENRE)
            genreCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()
        
    def build_anime_menu(self):
        """
            Method to display the default anime menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search anime
        if self.MENU_ANIME_SEARCH in self.MENU_ANIME_OPT and constant.__addon__.getSetting('only_global_search') == 'false':  
            search = StreamItem(constant.__addon__.getLocalizedString(62050))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_ANIME)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
            
        # Global Search anime
        if constant.__addon__.getSetting('use_global_search') == 'true':   
            search = StreamItem(constant.__addon__.getLocalizedString(62051))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_ANIME)
            search.setAction(StreamItem.ACTION_GLOBAL_SEARCH)
            search.addListItemToDirectory()
           
        # Last anime
        if self.MENU_ANIME_LAST in self.MENU_ANIME_OPT:  
            last = StreamItem(constant.__addon__.getLocalizedString(62010))
            last.setIconImage(icons.getIcon('news')) 
            last.setType(StreamItem.TYPE_ANIME)
            last.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            last.setSubType(StreamItem.SUBTYPE_LAST)
            last.addListItemToDirectory()
            
        # Most view
        if self.MENU_ANIME_TOPVIEW in self.MENU_ANIME_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(62020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_ANIME)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top rate
        if self.MENU_ANIME_TOPRATE in self.MENU_ANIME_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(62060))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_ANIME)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # Top week
        if self.MENU_ANIME_TOPWEEK in self.MENU_ANIME_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(62030))
            topRate.setType(StreamItem.TYPE_ANIME)
            topRate.setIconImage(icons.getIcon('topweek')) 
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_WEEK)
            topRate.addListItemToDirectory()
            
        # List
        if self.MENU_ANIME_LIST in self.MENU_ANIME_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(62070))
            topRate.setIconImage(icons.getIcon('news')) 
            topRate.setType(StreamItem.TYPE_ANIME)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_LIST)
            topRate.addListItemToDirectory()
            
        # Categorie alphabetics
        if self.MENU_ANIME_CATEGORY_ALPHA in self.MENU_ANIME_OPT:  
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(62040))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_ANIME)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()        
    
    def build_tv_show_menu(self):
        """
            Method to display the default tv show menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search tv show
        if self.MENU_TVSHOW_SEARCH in self.MENU_TVSHOW_OPT and constant.__addon__.getSetting('only_global_search') == 'false':  
            search = StreamItem(constant.__addon__.getLocalizedString(61050))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_TVSHOW)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
           
        # Global search tv show
        if constant.__addon__.getSetting('use_global_search') == 'true': 
            search = StreamItem(constant.__addon__.getLocalizedString(61051))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_TVSHOW)
            search.setAction(StreamItem.ACTION_GLOBAL_SEARCH)
            search.addListItemToDirectory()
           
        # Last Tv show
        if self.MENU_TVSHOW_LAST in self.MENU_TVSHOW_OPT:  
            last = StreamItem(constant.__addon__.getLocalizedString(61010))
            last.setIconImage(icons.getIcon('news')) 
            last.setType(StreamItem.TYPE_TVSHOW)
            last.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            last.setSubType(StreamItem.SUBTYPE_LAST)
            last.addListItemToDirectory()
            
        # Most view
        if self.MENU_TVSHOW_TOPVIEW in self.MENU_TVSHOW_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(61020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_TVSHOW)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top week
        if self.MENU_TVSHOW_TOPWEEK in self.MENU_TVSHOW_OPT:  
            topWeek = StreamItem(constant.__addon__.getLocalizedString(61030))
            topWeek.setIconImage(icons.getIcon('topweek')) 
            topWeek.setType(StreamItem.TYPE_TVSHOW)
            topWeek.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topWeek.setSubType(StreamItem.SUBTYPE_TOP_WEEK)
            topWeek.addListItemToDirectory()
        
        # Top rate
        if self.MENU_TVSHOW_TOPRATE in self.MENU_TVSHOW_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(61070))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_TVSHOW)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # List
        if self.MENU_TVSHOW_LIST in self.MENU_TVSHOW_OPT:  
            list = StreamItem(constant.__addon__.getLocalizedString(61060))
            list.setIconImage(icons.getIcon('news')) 
            list.setType(StreamItem.TYPE_TVSHOW)
            list.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            list.setSubType(StreamItem.SUBTYPE_LIST)
            list.addListItemToDirectory()
        
        # Categorie alphabetics
        if self.MENU_TVSHOW_CATEGORY_ALPHA in self.MENU_TVSHOW_OPT:  
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(61040))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_TVSHOW)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()
       
    def build_show_menu(self):
        """
            Method to display the default show menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search show
        if self.MENU_SHOW_SEARCH in self.MENU_SHOW_OPT:  
            search = StreamItem(constant.__addon__.getLocalizedString(63050))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_SHOW)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
           
        # Last show
        if self.MENU_SHOW_LAST in self.MENU_SHOW_OPT:  
            last = StreamItem(constant.__addon__.getLocalizedString(63010))
            last.setIconImage(icons.getIcon('news')) 
            last.setType(StreamItem.TYPE_SHOW)
            last.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            last.setSubType(StreamItem.SUBTYPE_LAST)
            last.addListItemToDirectory()
            
        # Most view
        if self.MENU_SHOW_TOPVIEW in self.MENU_SHOW_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(63020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_SHOW)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top rate
        if self.MENU_SHOW_TOPRATE in self.MENU_SHOW_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(63030))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_SHOW)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # Categorie alphabetics
        if self.MENU_SHOW_CATEGORY_ALPHA in self.MENU_SHOW_OPT:  
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(63040))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_SHOW)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()

    def build_documentary_menu(self):
        """
            Method to display the default documentary menu.
        """
        kodiUtil.beginContentDirectory()
           
        # Search show
        if self.MENU_DOCUMENTARY_SEARCH in self.MENU_DOCUMENTARY_OPT:  
            search = StreamItem(constant.__addon__.getLocalizedString(64050))
            search.setIconImage(icons.getIcon('search')) 
            search.setType(StreamItem.TYPE_DOCUMENTARY)
            search.setAction(StreamItem.ACTION_SEARCH)
            search.addListItemToDirectory()
           
        # Last show
        if self.MENU_DOCUMENTARY_LAST in self.MENU_DOCUMENTARY_OPT:  
            last = StreamItem(constant.__addon__.getLocalizedString(64010))
            last.setIconImage(icons.getIcon('news')) 
            last.setType(StreamItem.TYPE_DOCUMENTARY)
            last.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            last.setSubType(StreamItem.SUBTYPE_LAST)
            last.addListItemToDirectory()
            
        # Most view
        if self.MENU_DOCUMENTARY_TOPVIEW in self.MENU_DOCUMENTARY_OPT:  
            mostView = StreamItem(constant.__addon__.getLocalizedString(64020))
            mostView.setIconImage(icons.getIcon('topview')) 
            mostView.setType(StreamItem.TYPE_DOCUMENTARY)
            mostView.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            mostView.setSubType(StreamItem.SUBTYPE_MOST_VIEW)
            mostView.addListItemToDirectory()
        
        # Top rate
        if self.MENU_DOCUMENTARY_TOPRATE in self.MENU_DOCUMENTARY_OPT:  
            topRate = StreamItem(constant.__addon__.getLocalizedString(64030))
            topRate.setIconImage(icons.getIcon('toprate')) 
            topRate.setType(StreamItem.TYPE_DOCUMENTARY)
            topRate.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
            topRate.setSubType(StreamItem.SUBTYPE_TOP_RATE)
            topRate.addListItemToDirectory()
        
        # Categorie alphabetics
        if self.MENU_DOCUMENTARY_CATEGORY_ALPHA in self.MENU_DOCUMENTARY_OPT:  
            alphaCat = StreamItem(constant.__addon__.getLocalizedString(64040))
            alphaCat.setIconImage(icons.getIcon('alphabetics')) 
            alphaCat.setType(StreamItem.TYPE_DOCUMENTARY)
            alphaCat.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_MENU)
            alphaCat.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            alphaCat.addListItemToDirectory()
           
        kodiUtil.endOfDirectory()
            
    def build_alphabetic_category(self,type):
        kodiUtil.beginContentDirectory()
        
        item = StreamItem('0..9')
        item.setType(type)
        item.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_LIST)
        item.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
        item.setPage(1)
        item.setSubTypeValue('0..9')
        item.addListItemToDirectory()
            
        for alpha in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            item = StreamItem(alpha)
            item.setType(type)
            item.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_LIST)
            item.setSubType(StreamItem.SUBTYPE_ALPHABETICS)
            item.setPage(1)
            item.setSubTypeValue(alpha)
            item.addListItemToDirectory()
            
        kodiUtil.endOfDirectory()
        
    def build_genre_category(self,type):
        pass
    

    def build_settings_menu(self):
        """
            Method to display the main menu.
        """
        kodiUtil.beginContentDirectory()  
         
        # Resolver Settings
        resolverSettings = StreamItem(constant.__addon__.getLocalizedString(40037))
        resolverSettings.setIconImage(constant.__coreAddonDir__+'/resources/media/urlresolver.png') 
        resolverSettings.setType(StreamItem.TYPE_SETTINGS)
        resolverSettings.setAction(StreamItem.ACTION_DISPLAY_URLRESOLVER_SETTINGS)
        resolverSettings.addListItemToDirectory()
        
        # Metahandler Settings
        if( constant.__addon__.getSetting('getdetails') == '2'):        
            dlmanager = StreamItem(constant.__addon__.getLocalizedString(40040))
            dlmanager.setIconImage(constant.__coreAddonDir__+'/resources/media/urlresolver.png') 
            dlmanager.setType(StreamItem.TYPE_SETTINGS)
            dlmanager.setAction(StreamItem.ACTION_DISPLAY_METAHANDLER_SETTINGS)
            dlmanager.addListItemToDirectory()
            
        # Settings
        resolverSettings = StreamItem(constant.__addon__.getLocalizedString(40041))
        resolverSettings.setIconImage(constant.__coreAddonDir__+'/resources/media/urlresolver.png') 
        resolverSettings.setType(StreamItem.TYPE_SETTINGS)
        resolverSettings.setAction(StreamItem.ACTION_DISPLAY_SETTINGS)
        resolverSettings.addListItemToDirectory()        
       
        kodiUtil.endOfDirectory(False)
    
    def getSettingsXml(self):
        """
            Method to get the xml settings of the current source
            Format: 
            
            <setting label="XXXX" type="lsep"/>
            <setting id="src_xxxx_activated" type="bool" label="52001" default="true"/>        
            <setting id="src_xxxx_user" label="52002" type="text" default="" enable="eq(1,1)" visible="eq(-1,1)"/>
            <setting id="src_xxxx_pwd" label="52003" type="text" option="hidden" default="" enable="eq(-2,1)" visible="eq(-2,1)"/>
        """
        return ''

    def getSettingValue(self,settingName):
        """
            Method to get the value of a setting parameter
            @param settingName: the name of the parameter
            
            @return the value of the parameter
        """
        id = "src_"+self.getName().lower()+"_"+settingName
        return constant.__addon__.getSetting(id)
    
    def getServiceSettingValue(self):
        """
            Method to get the xml value for the service settings
            @return: the xml value for the service settings
        """            
        service_mod_str = '<setting id="service_movie_mod" type="enum" label="54004"  default="0" values="' 
    
        if self.MENU_MOVIE_LAST in self.MENU_MOVIE_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(60010)+'|'
            
        if self.MENU_MOVIE_TOPVIEW in self.MENU_MOVIE_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(60020)+'|'
            
        if self.MENU_MOVIE_TOPWEEK in self.MENU_MOVIE_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(60030)+'|'
            
        if self.MENU_MOVIE_TOPRATE in self.MENU_MOVIE_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(60040)+'|'
            
        if self.MENU_MOVIE_EXCLUE in self.MENU_MOVIE_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(60080)
            
        service_mod_str += '" enable="eq(-4,true)" visible="eq(-4,true)"/>\n'
        
        service_mod_str += '<setting id="service_tvshow_mod" type="enum" label="54005"  default="0" values="' 
        if self.MENU_TVSHOW_LAST in self.MENU_TVSHOW_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(61010)+'|'
            
        if self.MENU_TVSHOW_TOPVIEW in self.MENU_TVSHOW_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(61020)+'|'
            
        if self.MENU_TVSHOW_TOPWEEK in self.MENU_TVSHOW_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(61030)+'|'
            
        if self.MENU_TVSHOW_TOPRATE in self.MENU_TVSHOW_OPT:
            service_mod_str += constant.__addon__.getLocalizedString(61070)
            
        service_mod_str += '" enable="eq(-3,true)" visible="eq(-3,true)"/>\n'
        return service_mod_str
        
    def getMovieListService(self):
        """
            Method to get the movie list for service
            @return the movie list
        """
        index = int(constant.__addon__.getSetting('service_movie_mod'))
        
        if self.MENU_MOVIE_LAST == self.serviceMovieValues[index]:
            return self.getLastMovie()
            
        if self.MENU_MOVIE_TOPVIEW == self.serviceMovieValues[index]:
            return self.getMostViewMovie()
            
        if self.MENU_MOVIE_TOPWEEK == self.serviceMovieValues[index]:
            return self.getTopWeekMovie()
            
        if self.MENU_MOVIE_TOPRATE == self.serviceMovieValues[index]:
            return self.getTopMovie()
            
        if self.MENU_MOVIE_EXCLUE == self.serviceMovieValues[index]:
            return self.getExclueMovie()
        
        
    def getTvShowListService(self):
        """
            Method to get the tvshow list for service
            @return the tvshow list
        """
        index = int(constant.__addon__.getSetting('service_tvshow_mod'))
        
        if self.MENU_TVSHOW_LAST == self.serviceTvShowValues[index]:
            return self.getLastTvShow()
            
        if self.MENU_TVSHOW_TOPVIEW == self.serviceTvShowValues[index]:
            return self.getMostViewTvShow()
            
        if self.MENU_TVSHOW_TOPWEEK == self.serviceTvShowValues[index]:
            return self.getTopWeekTvShow()
            
        if self.MENU_TVSHOW_TOPRATE == self.serviceTvShowValues[index]:
            return self.getTopTvShow()
            
        
        
        
    def isActivated(self):
        """
            Method to know if the source is activated
            @return true if the source is activated, else return false
        """
        if sys.argv[0].endswith('test.py'):
            return True
        
        if int(constant.__addon__.getSetting('default_stream_src')) == self.getId() or self.getSettingValue("activated") == "true":
            return True
        else:
            return False