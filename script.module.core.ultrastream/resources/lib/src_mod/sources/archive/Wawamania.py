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
from resources.lib.item import StreamItem
from resources.lib.logger import Logger
from resources.lib.src_mod.sourceTemplate import streamingSourceTemplate as Source
from BeautifulSoup import BeautifulSoup
if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:
    import resources.lib.miscFunctions as miscFunctions
import strUtil
from resources.lib.item import StreamItem
import cookielib

# ____________________        C L A S S          ____________________
class Wawamania(Source):
    
    
    # ___ The source ID
    ID = 2
    
    # ___ The name of the source
    NAME = 'Wawa-Mania'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "https://forum.wawa-mania.ec/"
    
    # LOGGER    
    __LOGGER__ = Logger('StreamClub','Wawa-Mania')
    
    # MENU
    
    MAIN_MENU_OPT = [Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     Source.MAIN_MENU_TVSHOW,
                     Source.MAIN_MENU_ANIME,
                     #Source.MAIN_MENU_SHOW,
                     #Source.MAIN_MENU_DOCUMENTARY]
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     Source.MENU_MOVIE_LAST,
                     Source.MENU_MOVIE_TOPVIEW,
                     Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     Source.MENU_MOVIE_CATEGORY_ALPHA,
                     Source.MENU_MOVIE_CATEGORY_GENRE]    
    
    MENU_MOVIE_HD_OPT = [Source.MENU_MOVIE_HD_SEARCH,
                     Source.MENU_MOVIE_HD_LAST,
                     Source.MENU_MOVIE_HD_TOPVIEW,
                     Source.MENU_MOVIE_HD_TOPWEEK,
                     Source.MENU_MOVIE_HD_TOPRATE,
                     Source.MENU_MOVIE_HD_CATEGORY_ALPHA,
                     Source.MENU_MOVIE_HD_CATEGORY_GENRE]    
    
    MENU_TVSHOW_OPT = [Source.MENU_TVSHOW_SEARCH,
                     Source.MENU_TVSHOW_LAST,
                     Source.MENU_TVSHOW_TOPVIEW,
                     Source.MENU_TVSHOW_TOPWEEK,
                     Source.MENU_TVSHOW_TOPRATE,
                     Source.MENU_TVSHOW_CATEGORY_ALPHA,
                     Source.MENU_TVSHOW_CATEGORY_GENRE]
    
    MENU_ANIME_OPT = [Source.MENU_ANIME_SEARCH,
                     Source.MENU_ANIME_LAST,
                     Source.MENU_ANIME_TOPVIEW,
                     Source.MENU_ANIME_TOPWEEK,
                     Source.MENU_ANIME_TOPRATE,
                     Source.MENU_ANIME_CATEGORY_ALPHA,
                     Source.MENU_ANIME_CATEGORY_GENRE]
    
    def isLogin(self):
        # Open page : https://forum.wawa-mania.ec/php/home.php
        
        home_href = 'php/mp.php'
        
        response = self.openPage(home_href,byPassLogin=True)
        
        if response and response.getcode() == 200: 
            content = response.read()
            soup = BeautifulSoup(content)
            notconnectedDiv = soup.find("div", {"id":"notcon"})
            if notconnectedDiv is not None:
                return False       
        else:
            return False  
          
        return True
    
    def login(self):
        """
            Method to login Wawa-mania
        """        
        # Use https://forum.wawa-mania.ec/login
        post_login_href = 'login'
        # Data to post
        data = {'username':'Seko34','password':'soleilune'}
        response = self.postPage(post_login_href, data,byPassLogin=True)
        
        if response is not None:
            response.read()
            response.close()
            
            # Log all cookie value            
            for cookie in self.cookiejar:
                self.__LOGGER__.log(cookie.name)
         
        # ___ If PHPSESSID  is not in cookies, so we are not logged
        if not 'PHPSESSID' in [cookie.name for cookie in self.cookiejar]:
            self.__LOGGER__.log('Error to login on wawa-mania', xbmc.LOGERROR)
            
        # ___ Else we are logged
        else:
            self.__LOGGER__.log('Login on wawa-mania', xbmc.LOGINFO)
            self.isLogin()
            
    def searchMovie(self, title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        # Use post https://forum.wawa-mania.ec/php/search.php
        # Data to post :
        # search:300
        # sub:45 : Exclue, 46 : DVDRIP, 
        # startfrom:0
        # filter:subject
        # by:to_id
        # sort:desc
        post_href = 'php/search.php'
        # Data to post
        data = {'search':title,'sub':46,'startfrom':0,'filter':'subject','by':'to_id','sort':'desc'}
        response = self.postPage(post_href, data)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            
            soup = BeautifulSoup(content)
            
            # For every post, get title and topicLink          
            movies = soup.findAll('span',{'class':'title_sort'})
            topicLink = soup.findAll('a',{'class':'shref viewtopic'})
            for index in range(0,len(movies)):
                
                movie = movies[index]
                title = movie.text.encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                href = topicLink[index]['href']
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
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
                                
                # __ Add the element to the list
                elementList.append(element)
            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.build_dsptream_page(href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        
        # Use post https://forum.wawa-mania.ec/php/search.php
        # Data to post :
        # search: 300 --Valeur de la recherche
        # sub:45 : Exclue, 46 : DVDRIP, 
        # startfrom:0
        # filter:subject
        # by:to_id
        """<optgroup label="Films / Vidéo">
                    <option value="45">Films (exclues)</option>
                    <option value="5">Films (dvdrip)</option>
                    <option value="35">Films (Screener et TS)</option>
                    <option value="42">Films (Vo et VoSt)</option>
                    <option value="46">Full DvD / HD</option>
                    <option value="6">Séries télé</option>
                    <option value="81">Sourds et malentendants</option>
                    <option value="56">Docs, spectacles</option>
                    <option value="58">Dessin animés / Animes / Mangas</option>
        </optgroup>"""
        # sort:desc
        post_href = 'php/search.php'
        # Data to post
        data = {'search':title,'sub':6,'startfrom':0,'filter':'subject','by':'to_id','sort':'desc'}
        response = self.postPage(post_href, data)
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            
            soup = BeautifulSoup(content)
            
            # For every post, get title and topicLink          
            tvshows = soup.findAll('span',{'class':'title_sort'})
            topicLink = soup.findAll('a',{'class':'shref viewtopic'})
            for index in range(0,len(tvshows)):
                
                tvshow = tvshows[index]
                title = tvshow.text.encode('UTF-8')
                title = strUtil.unescapeHtml(str(title))
                href = topicLink[index]['href']
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
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
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_TVSHOW)  
                element.setSourceId(self.ID)              
                                
                # __ Add the element to the list
                elementList.append(element)
            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.build_dsptream_page(href) + ')', xbmc.LOGERROR)
    
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
        pass
    
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
        xmlSettingStr += '<setting label="Wawamania" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_wawamania_activated" type="bool" label="52001" default="true"/>\n'
        xmlSettingStr += '<setting id="src_wawamania_user" label="52002" type="text" default="" enable="eq(1,1)" visible="eq(-1,1)"/>\n'
        xmlSettingStr += '<setting id="src_wawamania_pwd" label="52003" type="text" option="hidden" default="" enable="eq(-2,1)" visible="eq(-2,1)"/>\n'
        return xmlSettingStr