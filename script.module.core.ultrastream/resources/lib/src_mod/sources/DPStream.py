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
import webUtil
import strUtil
import re
import constant
from BeautifulSoup import BeautifulSoup
from pydoc import synopsis
from src_mod.sourceTemplate import streamingSourceTemplate as Source
from item import StreamItem
from logger import Logger

if sys.argv[0].endswith('test.py'):
    import resources.lib.test.dummyMiscFunctions as miscFunctions
else:
    import miscFunctions as miscFunctions



# ____________________        C L A S S          ____________________
class DPStream(Source):
    
    
    # ___ The source ID
    ID = 1
    
    # ___ The name of the source
    NAME = 'DPStream'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://www.dpstream.net/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','DPStream')
    
    # MENU
    
    MAIN_MENU_OPT = [#Source.MAIN_MENU_MOVIE_HD,
                     Source.MAIN_MENU_MOVIE,
                     Source.MAIN_MENU_TVSHOW,
                     Source.MAIN_MENU_ANIME,
                     Source.MAIN_MENU_SHOW,
                     Source.MAIN_MENU_DOCUMENTARY
                     ]
  
    MENU_MOVIE_OPT = [Source.MENU_MOVIE_SEARCH,
                     Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     Source.MENU_MOVIE_TOPWEEK,
                     Source.MENU_MOVIE_TOPRATE,
                     Source.MENU_MOVIE_CATEGORY_ALPHA,
                     Source.MENU_MOVIE_CATEGORY_GENRE
                     ]   
    
    MENU_MOVIE_HD_OPT = [Source.MENU_MOVIE_HD_SEARCH,
                    # Source.MENU_MOVIE_HD_LAST,
                     #Source.MENU_MOVIE_HD_TOPVIEW,
                     #Source.MENU_MOVIE_HD_TOPWEEK,
                    # Source.MENU_MOVIE_HD_TOPRATE,
                     Source.MENU_MOVIE_HD_CATEGORY_ALPHA,
                     #Source.MENU_ANIME_CATEGORY_GENRE
                     ]    
    
    MENU_TVSHOW_OPT = [Source.MENU_TVSHOW_SEARCH,
                     Source.MENU_TVSHOW_LAST,
                     #Source.MENU_TVSHOW_TOPVIEW,
                     Source.MENU_TVSHOW_TOPWEEK,
                     Source.MENU_TVSHOW_TOPRATE,
                     Source.MENU_TVSHOW_CATEGORY_ALPHA,
                     #Source.MENU_ANIME_CATEGORY_GENRE
                     ]
    
    MENU_ANIME_OPT = [Source.MENU_ANIME_SEARCH,
                     Source.MENU_ANIME_LAST,
                     #Source.MENU_ANIME_TOPVIEW,
                     Source.MENU_ANIME_TOPWEEK,
                     Source.MENU_ANIME_TOPRATE,
                     Source.MENU_ANIME_CATEGORY_ALPHA,
                     #Source.MENU_ANIME_CATEGORY_GENRE
                     ]
    
    
    MENU_SHOW_OPT = [Source.MENU_SHOW_CATEGORY_ALPHA]
    
    
    MENU_DOCUMENTARY_OPT = [Source.MENU_DOCUMENTARY_CATEGORY_ALPHA]
    
    # ____ C U S T O M     V A R I A B L E S _____
    
    # LIST TYPE
    LIST_TYPE_LAST = 'dernier'
    LIST_TYPE_TOPWEEK = 'tophebdo'      
    LIST_TYPE_MOSTVIEW = 'top'
    LIST_TYPE_TOPRATED = 'topnotefilm'
    
    # CONFIG HTTP POST
    DPSTREAM_POST_HEADER_CFG = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
               'Accept-Encoding': 'none',
               'Accept-Language': 'en-US,en;q=0.8',
               'Connection': 'keep-alive',
               'X-Requested-With':'XMLHttpRequest'}
    
    def isLogin(self):
        return True
    
    def login(self):
        pass
            
    def appendLinkInList(self,streamItem,elementList):
        """
            Method to append a link in a list if the link is not already in the list
            @param streamItem : the StreaItem to add
            @param elementList: the list to append
        """
        for el in elementList:
            # ___ If the link is in the list, return the list as it is.
            if int(streamItem.getType()) == StreamItem.TYPE_STREAMING_LINK and el.getPlayableUrl() == streamItem.getPlayableUrl():
                if el.getQuality() == 'All' and streamItem.getQuality() != 'All':
                        el.setQuality(streamItem.getQuality())
                        el.regenerateKodiTitle()
                if streamItem.getLang() is not None and streamItem.getLang() != '':
                        el.setLang(streamItem.getLang())
                        el.regenerateKodiTitle()
                if streamItem.getSubTitle() is not None and streamItem.getSubTitle() != '' :
                        el.setSubTitle(streamItem.getSubTitle())
                        el.regenerateKodiTitle()
                return elementList
            elif int(streamItem.getType()) != StreamItem.TYPE_STREAMING_LINK and el.getTitle() == streamItem.getTitle():
                return elementList
        # ___ Else add the link       
        elementList.append(streamItem)
        return elementList  
 
    def removeDuplicatesInList(self,elementList):
        """
            Method to remove duplicates in list
            @param elementList: the list
            @return: the list without duplicates
        """
        result = []
        for el in elementList:
            result = self.appendLinkInList(el, result)
        return result  
 
    
    def searchMovie(self,title):
        """
            Method to search a movie
            @return a list of StreamItem
        """
        # http://www.dpstream.net/films-recherche?q=300
        # keyword=300
        href = 'films-recherche?q='+webUtil.encodeStr(title)        
        response = self.openPage(href)
        elementList = []
        
        if response and response.getcode() == 200:    
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
            
            # For every movie            
            movies = soup.findAll('div',{'class':'resultHeader'})
            for index in range(0, len(movies)):
                
                
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # ___ Get the id of the movie
                patternIdMovie = re.compile('(/film-)(\d*)(-.*)(\.html)')
                match = patternIdMovie.match(href)
                if match is not None:
                    movieId=match.group(2)
                else:
                    movieId=0
                    
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                element.setType(StreamItem.TYPE_MOVIE)  
                element.setId(movieId) 
                element.setSourceId(self.ID)
                
                elementList.append(element)  
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to search movie '+title)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)                       
                        
        # ___ Reverse result
        elementList = list(reversed(elementList))
        
        return elementList      
            
    def searchHdMovie(self, title):
        """
            Method to search a hd movie
            @return a list of StreamItem
        """
        return self.searchMovie(title)
           
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """    
        # http://www.dpstream.net/films-recherche?q=300
        # keyword=300
        href = '/series-recherche?q='+webUtil.encodeStr(title)      
        response = self.openPage(href)
        elementList = []
        
        if response and response.getcode() == 200:    
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
                           
            # For every tvshow            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_TVSHOW)
                element.setSourceId(self.ID)
                
                elementList.append(element)  
                
            
            # ___ Close the connection
            response.close()
            
        else:  
            miscFunctions.displayNotification('Unable to search TvShow ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(href) + ')', xbmc.LOGERROR)
        
        # ___ Reverse result
        elementList = list(reversed(elementList))
        
        return elementList 
             
    def searchAnime(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """    
        # http://www.dpstream.net/animes-recherche?q=Naruto
        href = '/animes-recherche?q='+webUtil.encodeStr(title)
        response = self.openPage(href)
        elementList = []
        
        if response and response.getcode() == 200:    
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
                           
            # For every tvshow            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_ANIME)
                element.setSourceId(self.ID)
                
                elementList.append(element)  
                
            
            # ___ Close the connection
            response.close()
            
        else:  
            miscFunctions.displayNotification('Unable to search Anime ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(href) + ')', xbmc.LOGERROR)
        
        # ___ Reverse result
        elementList = list(reversed(elementList))
        
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
            
            titles = soup.find("div", {"id" : "myContent"}).findAll('div', {'class':'season-tit col-md-6'})
            
            # __ For each link on the left div
            for index in range(0, len(titles)):
                
                # ___ Get title and season with UTF-8 encoding
                title = titles[index].text.encode('UTF-8')
                season = -1
                if 'Saison ' in title:
                    season = title.replace("Saison ","")
                    try:
                        season = int(season)
                    except:
                        pass
                
                # ___ Unscape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log('Season find : '+title,xbmc.LOGDEBUG)
                
                # __ Create the element
                element = StreamItem(title)
                element.setHref(tvShowStreamItem.getHref())         
                element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                element.setType(StreamItem.TYPE_TVSHOW_SEASON)                    
                element.setTvShowName(tvShowStreamItem.getTvShowName())                
                if season > 0:
                    element.setSeason(season)
                    element.determineSeasonTitle()
                
               
                elementList.append(element)
        
        
        return elementList;    
    
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
            
            titles = soup.find("aside", {"id" : "episodeSidebarNav"}).findAll('h4', {'class':'panel-title'})
            #titles = soup.find("div", {"id" : "myContent"}).findAll('div', {'class':'season-tit col-md-6'})
            # __ For each link on the left div
            for index in range(0, len(titles)):
                
                # ___ Get title and season with UTF-8 encoding                
                title = titles[index].text.encode('UTF-8')
                season = -1
                if 'Saison ' in title:
                    season = title.replace("Saison ","")
                    try:
                        season = int(season)
                    except:
                        pass
                
                # ___ Unscape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log('Season find : '+title,xbmc.LOGDEBUG)
                
                # __ Create the element
                element = StreamItem(title)
                element.setHref(tvShowStreamItem.getHref())         
                element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)
                element.setType(StreamItem.TYPE_ANIME_SEASON)                    
                element.setTvShowName(tvShowStreamItem.getTvShowName())
                if season > 0:
                    element.setSeason(season)
                    element.determineSeasonTitle()
               
                elementList.append(element)        
        
        
        return elementList;
    
    def getTvShowEpisodes(self, seasonStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(seasonStreamItem)
        if soup is not None:
            
            #titles = soup.find("aside", {"id" : "episodeSidebarNav"}).findAll('h4', {'class':'panel-title'})
            #episodes = soup.find("aside", {"id" : "episodeSidebarNav"}).findAll('div', {'id':'accordion'})            
            titles = soup.find("div", {"id" : "myContent"}).findAll('div', {'class':'season-tit col-md-6'})
            episodes = soup.find("div", {"id" : "myContent"}).findAll('div', {'class':'table-responsive '})
            # __ For each link on the left div           
            self.__LOGGER__.log('Get episodes for season '+str(seasonStreamItem.getSeason()),xbmc.LOGINFO) 
                       
            # __ For each link on the left div
            for index in range(0, len(titles)):
                
                # ___ Get title and season with UTF-8 encoding
                title = titles[index].text.encode('UTF-8')            
                season = title.replace("Saison ","") 
                # ___ Unescape htm on title
                title = strUtil.unescapeHtml(title) 
                
                if int(season) == int(seasonStreamItem.getSeason()) or title == seasonStreamItem.getTitle():  
                     
                    # __ Add the episode
                    #for ahref in episodes[index].find('ul',{'class':'episode_number_right'}).findAll('a'):  
                    episodeNames = episodes[index].findAll('td',{'class':'col-name'})   
                    episodeIds = episodes[index].findAll('td',{'class':'col-name'})                       
                    for indexEp in range(0,len(episodeNames)):
                        
                        td = episodeNames[indexEp]
                        ahref = td.find('a')
                        # __ Add the episode
                        if "onclick" in ahref and ahref["onclick"].startswith("showepisodeLinks("):
                            patternJS = re.compile('(showepisodeLinks\()(\d*)?(,)(\d*)?(,\')(.*)?(\',)(,)(\d*)?(,)(\d*)?(,)(\d*)?(,)(\d*)?(,\'.*\',\'.*\',)(\'.*\')(\).*)')
                            match = patternJS.match(ahref["onclick"].encode('UTF-8').strip())
                            if match is not None:
                                
                                # ___ Get id of tvshow, season, and episode
                                idEpisode = match.group(2)
                                saison = match.group(9)
                                episode = match.group(11)
                                idSerie = match.group(13)
                               
                                # ___ Get title
                                title = ahref.text.encode('utf-8')[12:]                     
                                # ___ Unscape html on title
                                title = strUtil.unescapeHtml(title) 
                                # ___ Clean title
                                title = strUtil.cleanTitle(title)
                                # ___ Build url
                                url = ahref['href'].encode('utf-8')
                                                                
                                # __ Create the element                        
                                element = StreamItem(title)
                                element.setHref(url)         
                                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                                element.setType(StreamItem.TYPE_TVSHOW_EPISODE) 
                                element.setTvShowName(seasonStreamItem.getTvShowName())
                                element.setSeason(seasonStreamItem.getSeason())
                                element.addEpisode(int(episode))
                        
                                element.determineEpisodeTitle()                               
                                elementList.append(element)
                                
                       
                                
                        else:   
                            # ___ Get the href
                            href = ahref['href'].encode('UTF-8')  
                            # ___ Get the id
                            id = None
                            if 'id' in ahref:
                                id = ahref['id'][4:]
                            else:
                                idLink = episodeIds[indexEp].find('a')
                                if 'id' in idLink:
                                    id = idLink['id'][10:]
                                    self.__LOGGER__.log(id)
                                    
                            # ___ Get the title
                            title = ahref.text.encode('utf-8')   
                            # ___ Unscape html on title
                            title = strUtil.unescapeHtml(title) 
                            # __Remove "Episode  n°"
                            
                            self.__LOGGER__.log('Find episode :'+title,xbmc.LOGINFO)                         
                                                        
                            if title.startswith('Episode n'):
                                title = title[11:]
                            elif title.startswith('Episode'):                                
                                title = title[8:]
                            else:
                                patternEpisode = re.compile('(S)(\d{1,2})?( E)(\d{1,2})')
                                match = patternEpisode.match(title)
                                if match is not None:
                                    title = match.group(4)
                                    
                            episodes = []
                            episodes.append(int(title))
                            
                            # ___ Clean title
                            title = strUtil.cleanTitle(title) 
                            
                            # __ Create the element
                            element = StreamItem(title)
                            element.setHref(href)         
                            element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                            element.setType(StreamItem.TYPE_TVSHOW_EPISODE) 
                            element.setTvShowName(seasonStreamItem.getTvShowName())
                            element.setSeason(seasonStreamItem.getSeason())
                            element.setId(id)
                            if len(episodes) > 0:
                                for index in range(0,len(episodes)):
                                    element.addEpisode(episodes[index])
                            
                            element.determineEpisodeTitle()                               
                            elementList.append(element)     
        
        return elementList;
    
    def getAnimeEpisodes(self, seasonStreamItem):
        """
            Method to get the episodes list of a season
            @return a list of StreamItem
        """        
        # ___ Initialize the list to return
        elementList = []
        
        # ___ Get the soup
        soup = self._initOpenPage(seasonStreamItem)
        if soup is not None:
            
            titles = soup.find("aside", {"id" : "episodeSidebarNav"}).findAll('h4', {'class':'panel-title'})
            episodes = soup.find("aside", {"id" : "episodeSidebarNav"}).findAll('div', {'id':'accordion'})
            
            # __ For each link on the left div           
            self.__LOGGER__.log('Get episodes for season '+str(seasonStreamItem.getSeason()),xbmc.LOGINFO) 
                       
            # __ For each link on the left div
            for index in range(0, len(titles)):
                
                # ___ Get title and season with UTF-8 encoding
                title = titles[index].text.encode('UTF-8')            
                season = title.replace("Saison ","") 
                # ___ Unescape htm on title
                title = strUtil.unescapeHtml(title) 
                
                if str(season) == str(seasonStreamItem.getSeason()) or title == seasonStreamItem.getTitle():   
                     
                    # __ Add the episode
                    for ahref in episodes[index].find('ul',{'class':'episode_number_right'}).findAll('a'):                        
                        
                        # __ Add the episode
                        if "onclick" in ahref and ahref["onclick"].startswith("showepisodeLinks("):
                            patternJS = re.compile('(showepisodeLinks\()(\d*)?(,)(\d*)?(,\')(.*)?(\',)(,)(\d*)?(,)(\d*)?(,)(\d*)?(,)(\d*)?(,\'.*\',\'.*\',)(\'.*\')(\).*)')
                            match = patternJS.match(ahref["onclick"].encode('UTF-8').strip())
                            if match is not None:
                                
                                # ___ Get id of tvshow, season, and episode
                                idEpisode = match.group(2)
                                saison = match.group(9)
                                episode = match.group(11)
                                idSerie = match.group(13)
                               
                                # ___ Get title
                                title = ahref.text.encode('utf-8')[12:]                     
                                # ___ Unscape html on title
                                title = strUtil.unescapeHtml(title) 
                                # ___ Clean title
                                title = strUtil.cleanTitle(title)
                                # ___ Build url
                                url = ahref['href'].encode('utf-8')
                                                                
                                # __ Create the element                        
                                element = StreamItem(title)
                                element.setHref(url)         
                                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                                element.setType(StreamItem.TYPE_TVSHOW_EPISODE) 
                                element.setTvShowName(seasonStreamItem.getTvShowName())
                                element.setSeason(seasonStreamItem.getSeason())
                                element.addEpisode(int(episode))
                        
                                element.determineEpisodeTitle()                               
                                elementList.append(element)
                                
                       
                                
                        else:   
                            # ___ Get the href
                            href = ahref['href'].encode('UTF-8')  
                            # ___ Get the id
                            id = ahref['id'][4:]
                            # ___ Get the title
                            title = ahref.text.encode('utf-8')   
                            # ___ Unscape html on title
                            title = strUtil.unescapeHtml(title) 
                            # __Remove "Episode  n°"
                            
                            self.__LOGGER__.log('Find episode :'+title,xbmc.LOGINFO)                         
                            
                            if title.startswith('Episode N'):
                                title = title[11:]
                            elif title.startswith('Episode'):                                
                                title = title[8:]
                                
                            episodes = []
                            if '-' in title:
                                episodes = title.split('-')
                            else:
                                episodes.append(int(title))
                            
                            # ___ Clean title
                            title = strUtil.cleanTitle(title) 
                            
                            # __ Create the element
                            element = StreamItem(title)
                            element.setHref(href)         
                            element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                            element.setType(StreamItem.TYPE_TVSHOW_EPISODE) 
                            element.setTvShowName(seasonStreamItem.getTvShowName())
                            element.setSeason(seasonStreamItem.getSeason())
                            element.setId(id)
                            if len(episodes) > 0:
                                for index in range(0,len(episodes)):
                                    element.addEpisode(episodes[index])
                            
                            element.determineEpisodeTitle()                               
                            elementList.append(element)     
        
        return elementList;
        
    def getMovieLink(self,movieStreamItem):
        """
            Method to get all links of a movie
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        
        # Get all link from movies/filter_player_data
        post_href = 'movies/filter_player_data'
        data = {'movie_id':movieStreamItem.getId(),'player_id':0,'quality_id':0}
        response = self.postPage(post_href, data, headers=self.DPSTREAM_POST_HEADER_CFG)
       
        if response and response.getcode() == 200: 
            content = response.read()
            soup = BeautifulSoup(content)
            
            #lignes = soup.find('tbody',{'id':'show_more_player_result'}).findAll('tr')
            lignes = soup.findAll('tr',attrs = {'id' : True})
            for ligne in lignes:
              
                colonnes = ligne.findAll('td')
                hostname = colonnes[0].text.encode('UTF-8').replace('&nbsp;\n','')
                version = colonnes[1].text.encode('UTF-8')
                qualite = colonnes[2].text.encode('UTF-8')
                href = colonnes[5].find('a')['href'].encode('UTF-8')

                if href !='javascript:void(0)':
                    href = self.formatLink(href) 
                    # __ Create the element                       
                    element = movieStreamItem.copy()
                    element.setAction(StreamItem.ACTION_PLAY)
                    element.setType(StreamItem.TYPE_STREAMING_LINK)
                    if len(qualite) > 1:
                        element.setQuality(qualite)
                    if len(version) > 1:
                        element.setLang(strUtil.getLangFromTitle(version))
                        element.setSubTitle(strUtil.getSubtitleFromTitle(version))
                    element.setHref(href)
                    element.setPlayableUrl(href)
                    if len(hostname) > 1:
                        element.setHostname(hostname.title())
                    element.regenerateKodiTitle()   
                    elementList = self.appendLinkInList(element, elementList)
                     
        elementList = self.getDPStreamLink(elementList)
                                  
        return elementList
    
    def getDPStreamLink(self,elementList):
        """
            Method to get real link from DPStream
            @param elementList: the list of links
            @param the elementList with the real link
        """
        for el in elementList:
            response = self.openPage(el.getHref()[:len(el.getHref())-1])
            if response is not None and response.getcode() == 200:
                content = response.read()
                indexId = content.find('sessionId: "')
                if indexId > 0:                
                    print el.getHref()[:len(el.getHref())-1]
                    print response.info()
                    print content
                    print content[indexId+12:indexId+52]
                    sessionPattern = re.compile('(.*)(sessionId: ")(.*)(",)(.*)',re.DOTALL)
                    match = sessionPattern.match(content)
                    if match is not None:
                        id1 = match.group(3)
                        print id1
                
                else:
                    hostname = el.getHostname()
                    url = response.geturl()
                    el.setHref(url)
                    el.setPlayableUrl(url)
                    el.setHostname(hostname)
                    
        return elementList
    
    def getTvShowEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """        
        # ___ Initialize the list to return
        elementList = []
        
        if episodeStreamItem.getId() is None or len(episodeStreamItem.getId()) == 0:
            responsePage = self.openPage(episodeStreamItem.getHref())
            
            if responsePage and responsePage.getcode() == 200:   
                contentPage = responsePage.read()
                soup = BeautifulSoup(contentPage) 
                activeLink = soup.find('a',{'class':re.compile('(.*)active_episode(.*)')})
                if activeLink is not None:
                    id = activeLink['id'].encode('UTF-8')
                    id = id[4:]
                    episodeStreamItem.setId(id)
                else:
                    return elementList
            else:
                return elementList
        
        # Get all link tvshows/showepisodeLinks/34674/0
        #post_href = 'tvshows/showepisodeLinks/'+str(episodeStreamItem.getId())+'/0'
        #data = {'episode_id':episodeStreamItem.getId()}
        post_href = 'tvshows/filter_player_data'
        data = {'tvshow_episode_id':str(episodeStreamItem.getId()),'player_id':0,'quality_id':0}
        self.__LOGGER__.log(post_href)
        self.__LOGGER__.log(data)
        response = self.postPage(post_href, data, headers=self.DPSTREAM_POST_HEADER_CFG)
                
        if response and response.getcode() == 200:   
            content = response.read()
            soup = BeautifulSoup(content)
            #lignes = soup.find('tbody',{'id':'show_more_result'}).findAll('tr')
            lignes = soup.findAll('tr',attrs = {'id' : True})
            
            
            self.__LOGGER__.log(content)
            for ligne in lignes:
              
                colonnes = ligne.findAll('td')
                hostname = colonnes[0].text.encode('UTF-8').replace('&nbsp;\n','')
                version = colonnes[1].text.encode('UTF-8')
                qualite = colonnes[2].text.encode('UTF-8')
                href = colonnes[5].find('a')['href'].encode('UTF-8')
                self.__LOGGER__.log(ligne)
                
                if href !='javascript:void(0)':
                    href = self.formatLink(href) 
                    # __ Create the element                       
                    element = episodeStreamItem.copy()
                    element.setAction(StreamItem.ACTION_PLAY)
                    element.setType(StreamItem.TYPE_STREAMING_LINK)
                    if len(qualite) > 1:
                        element.setQuality(qualite)
                    if len(version) > 1:
                        element.setLang(strUtil.getLangFromTitle(version))
                        element.setSubTitle(strUtil.getSubtitleFromTitle(version))
                    element.setHref(href)
                    if len(hostname) > 1:
                        element.setHostname(hostname.title())
                    element.regenerateKodiTitle()   
                    elementList = self.appendLinkInList(element, elementList) 
                     
        elementList = self.getDPStreamLink(elementList)
                                       
        return elementList
    
    def getAnimeEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        
        # ___ Initialize the list to return
        elementList = []
        
        if episodeStreamItem.getId() is None or len(episodeStreamItem.getId()) == 0:
            responsePage = self.openPage(episodeStreamItem.getHref())
            
            if responsePage and responsePage.getcode() == 200:   
                contentPage = responsePage.read()
                soup = BeautifulSoup(contentPage) 
                activeLink = soup.find('a',{'class':'active_episode'})
                activeLink2 = soup.find('a',{'class':'episode_anchor active_episode'})
                if activeLink is not None:
                    id = activeLink['id'].encode('UTF-8')
                    id = id[4:]
                    episodeStreamItem.setId(id)
                elif activeLink2 is not None:
                    id = activeLink2['id'].encode('UTF-8')
                    id = id[4:]
                    episodeStreamItem.setId(id)
                else:
                    return elementList
            else:
                return elementList
        
        idAnime = None
        idAnimePattern = re.compile('(http://www.dpstream.net//anime-)(.*)(-.*/.*.html)')
        
        match = idAnimePattern.match(episodeStreamItem.getHref())
        if match is not None:
            idAnime = match.group(2)
        
        # Get all link from animes/get_anime_episode_links
        post_href = 'animes/get_anime_episode_links'
        data = None
        if idAnime is not None:
            data = {'anime_id':idAnime,'episode_id':episodeStreamItem.getId(),'specific_chat':0}
        else:
            data = {'episode_id':episodeStreamItem.getId(),'specific_chat':0}
            
        response = self.postPage(post_href, data, headers=self.DPSTREAM_POST_HEADER_CFG)
        
        if response and response.getcode() == 200:   
            content = response.read()
            soup = BeautifulSoup(content)
            
            #lignes = soup.find('tbody',{'id':'show_more_result'}).findAll('tr')
            lignes = soup.findAll('tr',attrs = {'id' : True})
            
            for ligne in lignes:
              
                colonnes = ligne.findAll('td')
                hostname = colonnes[0].text.encode('UTF-8').replace('&nbsp;\n','')
                version = colonnes[1].text.encode('UTF-8')
                qualite = colonnes[2].text.encode('UTF-8')
                href = colonnes[5].find('a')['href'].encode('UTF-8')
                
                
                if href !='javascript:void(0)':
                    href = self.formatLink(href) 
                    # __ Create the element                       
                    element = episodeStreamItem.copy()
                    element.setAction(StreamItem.ACTION_PLAY)
                    element.setType(StreamItem.TYPE_STREAMING_LINK)
                    if len(qualite) > 1:
                        element.setQuality(qualite)
                    if len(version) > 1:
                        element.setLang(strUtil.getLangFromTitle(version))
                        element.setSubTitle(strUtil.getSubtitleFromTitle(version))
                    element.setHref(href)
                    if len(hostname) > 1:
                        element.setHostname(hostname.title())
                    element.regenerateKodiTitle()   
                    elementList = self.appendLinkInList(element, elementList) 
                     
        elementList = self.getDPStreamLink(elementList)
                                       
        return elementList
    
    def getHundredElementsList(self, type, listeType, limit=0, resultList=[]):
        """
            Method to get a list of hundred element
            @param type : the type of elements
            @param listeType : last, top rated, most view
            
            @return a list of dictionnary element
                    A dictionnary has the format :  
                    {'mode': '<the mode associated of the type of element>', 'name': '<the name of the element>', 'href': '<the link>', 'type': '<the type of the element>', 'info': '<Dictionnary : info of the element>'}
        """
        # ___ Initialize the list to return
        elementList = []
        if len(resultList) > 0:
            elementList = resultList   
         
        if listeType == DPStream.LIST_TYPE_LAST:
            href_type = 'ajax_latest_add'
        elif listeType == DPStream.LIST_TYPE_TOPWEEK:
            href_type = 'ajax_most_view_week'
        elif listeType == DPStream.LIST_TYPE_TOPRATED:
            href_type = 'ajax_most_view_all_time'
        
        # 
        if int(type) == StreamItem.TYPE_MOVIE:
            href = 'movies/'+href_type+'/?limit='+str(limit)
        elif int(type) == StreamItem.TYPE_TVSHOW:            
            href = 'tvshows/'+href_type+'/?limit='+str(limit)
        elif int(type) == StreamItem.TYPE_ANIME:            
            href = 'animes/'+href_type+'/?limit='+str(limit)
            
        # ____ Open a one hundred elements page for the selected type
        response = self.openPage(href)
        
        if response and response.getcode() == 200:
            
            # ___ Get the content
            content = response.read()            
            # ___ Get the soup
            soup = BeautifulSoup(content)        
            # ___ Get all tag <a></a>
            ahrefs = soup.findAll("a")                        
                                 
            # ___ For each link
            for link in ahrefs:
                
                # ___ Get the href
                title = link.text.encode('UTF-8')
                href = link['href'].encode('UTF-8')
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title) 

                
                # ___ Try to get the seaon and the episode
                season=''
                episode=''
                
                patternTvShow = re.compile('(.*)( S)(\d.*)(E)(\d.*)( .*)')
                match = patternTvShow.match(title)
                if match is not None:  
                    season = match.group(3) 
                    episode = match.group(5)
                    title = match.group(1)  
                else:
                    
                    patternTvShow = re.compile('(.*)( )(E|Episode)(\d.*)( .*)')
                    match = patternTvShow.match(title)
                    if match is not None:                          
                        episode = match.group(4)
                        title = match.group(1)     
                    else:
                        patternTvShow = re.compile('(.*)( - )(.*)()')
                        match = patternTvShow.match(title)
                        if match is not None:                          
                            episode = match.group(3)
                            if 'Episode' in episode:
                                episode = episode[11:13].strip()  
                            title = match.group(1)
                
                       
                # ___ Clean title  
                title = strUtil.cleanTitle(title)    
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)   
               
                
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                
                if int(type) == StreamItem.TYPE_MOVIE:
                    # ___ Get the id of the movie
                    patternIdMovie = re.compile('(/film-)(\d.*)(-.*)(\.html)')
                    match = patternIdMovie.match(href)
                    if match is not None:
                        movieId=match.group(2)
                    else:
                        movieId=0
                    element.setId(movieId)
                    element.setType(StreamItem.TYPE_MOVIE)  
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                elif int(type) == StreamItem.TYPE_TVSHOW:                               
                    element.setTvShowName(title)    
                    if season!= '':  
                        element.setType(StreamItem.TYPE_TVSHOW_SEASON) 
                        element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)           
                        element.setSeason(season) 
                        element.determineSeasonTitle()
                        
                    if episode != '':         
                        element.setType(StreamItem.TYPE_TVSHOW_EPISODE) 
                        element.setAction(StreamItem.ACTION_DISPLAY_LINKS)  
                        element.setEpisode(episode)    
                        element.determineEpisodeTitle() 
                        
                    if episode == '' and season == '':
                        element.setType(StreamItem.TYPE_TVSHOW) 
                        element.setAction(StreamItem.ACTION_DISPLAY_SEASONS) 
                         
                elif int(type) == StreamItem.TYPE_ANIME:                        
                    element.setTvShowName(title)     
                    if season!= '':  
                        element.setType(StreamItem.TYPE_ANIME_SEASON) 
                        element.setAction(StreamItem.ACTION_DISPLAY_EPISODES)           
                        element.setSeason(season) 
                        element.determineSeasonTitle()
                        
                    if episode != '':         
                        element.setType(StreamItem.TYPE_ANIME_EPISODE) 
                        element.setAction(StreamItem.ACTION_DISPLAY_LINKS)  
                        element.setEpisode(episode)    
                        element.determineEpisodeTitle() 
                        
                    if episode == '' and season == '':
                        element.setType(StreamItem.TYPE_ANIME) 
                        element.setAction(StreamItem.ACTION_DISPLAY_SEASONS) 
                                
                # __ Add the element to the list                
                elementList.append(element)      
                
                            
            # ___ Close the connection
            response.close()
            
            # ___ Get 100 results
            #if len(elementList) < 100:
                #elementList = self.getHundredElementsList(type,listeType, limit=len(elementList), resultList=elementList) 
                
            if limit < 90:
                
         
                if listeType == DPStream.LIST_TYPE_LAST:
                    subtype = StreamItem.SUBTYPE_LAST
                elif listeType == DPStream.LIST_TYPE_TOPWEEK:
                    subtype = StreamItem.SUBTYPE_TOP_WEEK
                elif listeType == DPStream.LIST_TYPE_TOPRATED:
                    subtype = StreamItem.SUBTYPE_TOP_RATE
                nextPage = StreamItem(constant.__addon__.getLocalizedString(70010))
                nextPage.setType(type)
                nextPage.setAction(StreamItem.ACTION_DISPLAY_TYPE_LIST)
                nextPage.setSubType(subtype)
                nextPage.setPage(len(elementList)+limit)
                elementList.append(nextPage)
                
            elementList = self.removeDuplicatesInList(elementList)  
            
            
            
        else:
            miscFunctions.displayNotification('Unable to open the page ' + self.buildHref(href))           
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(href), xbmc.LOGERROR)
        
       
            
        return elementList
    
    def getLastMovie(self,streamItem=False):
        """
            Method to get all last movie
            @return a list of StreamItem
        """
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_LAST,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_LAST)
    
    def getLastTvShow(self,streamItem=False):
        """
            Method to get all last tv show
            @return a list of StreamItem
        """
        
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_LAST,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_LAST)
        
    
    def getLastAnime(self,streamItem=False):
        """
            Method to get all last anime
            @return a list of StreamItem
        """        
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_LAST,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_LAST)  
    
    def getTopMovie(self,streamItem=False):
        """
            Method to get top movie
            @return a list of StreamItem
        """        
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_TOPRATED,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_TOPRATED)
    
    
    def getTopTvShow(self,streamItem=False):
        """
            Method to get top tv show
            @return a list of StreamItem
        """        
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_TOPRATED,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_TOPRATED)
    
    
    def getTopAnime(self,streamItem=False):
        """
            Method to get top anime
            @return a list of StreamItem
        """        
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_TOPRATED,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_TOPRATED)
    
    def getTopWeekMovie(self,streamItem=False):
        """
            Method to get top week movie
            @return a list of StreamItem
        """
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_TOPWEEK,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_MOVIE, DPStream.LIST_TYPE_TOPWEEK)
    
    
    def getTopWeekTvShow(self,streamItem=False):
        """
            Method to get top week tv show
            @return a list of StreamItem
        """
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_TOPWEEK,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_TVSHOW, DPStream.LIST_TYPE_TOPWEEK)
        
    
    
    def getTopWeekAnime(self,streamItem=False):
        """
            Method to get top week anime
            @return a list of StreamItem
        """
        if streamItem and streamItem.getPage() is not None and len(streamItem.getPage()) > 0:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_TOPWEEK,limit=int(streamItem.getPage()))
        else:
            return self.getHundredElementsList(StreamItem.TYPE_ANIME, DPStream.LIST_TYPE_TOPWEEK)
    
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
    
    def getAlphabeticMovieHDList(self,streamItem):
        
        """
            Method to get an alphabatic list of movie hd
            @return a list of StreamItem
        """
        pass
    
    def getAlphabeticMovieList(self,streamItem):
        
        """
            Method to get an alphabatic list of movie
            @return a list of StreamItem
        """
        page = streamItem.getPage()
        letter = streamItem.getSubTypeValue()
        
        # ___ Calculate href
        if letter == '0..9':
            href_opt = 'title_by_num:0'
        else:
            href_opt = 'lettre:'+letter
                   
        hrefPage = 'movies/films_ajax/' + href_opt + '/page:' + str(page)
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
                
            # For every movie            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # ___ Get the id of the movie
                patternIdMovie = re.compile('(/film-)(\d*)(-.*)(\.html)')
                match = patternIdMovie.match(href)
                if match is not None:
                    movieId=match.group(2)
                else:
                    movieId=0
                    
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                element.setType(StreamItem.TYPE_MOVIE)  
                element.setId(movieId) 
                
                elementList.append(element)  
                
            
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList      
    
    def getAlphabeticTvShowList(self,streamItem):        
        """
            Method to get an alphabatic list of tv show
            @return a list of StreamItem
        """
        
        
        page = streamItem.getPage()
        letter = streamItem.getSubTypeValue()
        
        # ___ Calculate href
        if letter == '0..9':
            href_opt = 'title_by_num:0'
        else:
            href_opt = 'lettre:'+letter
                   
        hrefPage = 'tvshows/series_ajax/' + href_opt + '/page:' + str(page)
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
                
            # For every tvshow            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_TVSHOW)
                
                elementList.append(element)  
                
            
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList    
    
    def getAlphabeticAnimeList(self,streamItem):
        
        """
            Method to get an alphabatic list of anime
            @return a list of StreamItem
        """
        page = streamItem.getPage()
        letter = streamItem.getSubTypeValue()
        
        # ___ Calculate href
        if letter == '0..9':
            href_opt = 'title_by_num:0'
        else:
            href_opt = 'lettre:'+letter
                   
        hrefPage = 'tvshows/series_ajax/' + href_opt + '/page:' + str(page)
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
                
            # For every tvshow            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # __ Create the element
                element = StreamItem(title)
                element.setTvShowName(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                element.setType(StreamItem.TYPE_ANIME)
                
                elementList.append(element)  
                
            
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList    

    def getAlphabeticShowList(self,streamItem):
        
        """
            Method to get an alphabatic list of show
            @return a list of StreamItem
        """
        page = streamItem.getPage()
        letter = streamItem.getSubTypeValue()
        
        # ___ Calculate href
        if letter == '0..9':
            hrefPage = 'films-recherche?title_by_num=0&lettre=' +  letter + '&categorie=Spectacle'
        else:
            hrefPage = 'films-recherche?page=' + str(page) + '&lettre=' +  letter + '&categorie=Spectacle'       
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
                
            # For every movie            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # ___ Get the id of the movie
                patternIdMovie = re.compile('(/film-)(\d*)(-.*)(\.html)')
                match = patternIdMovie.match(href)
                if match is not None:
                    movieId=match.group(2)
                else:
                    movieId=0
                    
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                element.setType(StreamItem.TYPE_MOVIE)  
                element.setId(movieId) 
                
                elementList.append(element)  
                
            
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList 

    def getAlphabeticDocumentaryList(self,streamItem):
        
        """
            Method to get an alphabatic list of documentary
            @return a list of StreamItem
        """
        page = streamItem.getPage()
        letter = streamItem.getSubTypeValue()
        
        # ___ Calculate href
        if letter == '0..9':
            hrefPage = 'films-recherche?title_by_num=0&lettre=' +  letter + '&categorie=Documentaire'
        else:
            hrefPage = 'films-recherche?page=' + str(page) + '&lettre=' +  letter + '&categorie=Documentaire'       
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            # ___ Read the source
            content = response.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)
           
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
                
            # For every movie            
            movies = soup.findAll('div',{"class":"resultHeader"})
            for index in range(0, len(movies)):
                movie = movies[index]
                link = movie.find("a")
                                
                href = link['href'].encode('UTF-8')
                title = link.text.encode('UTF-8')
                
                # ___ Unescape html on title
                title = strUtil.unescapeHtml(title)
                self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                # ___ Get  year, quality and lang
                year = strUtil.getYearFromTitle(title) 
                quality = strUtil.getQualityFromTitle(title)  
                lang = strUtil.getLangFromTitle(title) 
                subtitle = strUtil.getSubtitleFromTitle(title)  
                # ___ Clean title
                title = strUtil.cleanTitle(title)                
                self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
                
                # ___ Get the id of the movie
                patternIdMovie = re.compile('(/film-)(\d*)(-.*)(\.html)')
                match = patternIdMovie.match(href)
                if match is not None:
                    movieId=match.group(2)
                else:
                    movieId=0
                    
                # __ Create the element
                element = StreamItem(title)
                element.setHref(href)                
                element.setYear(year)             
                element.setQuality(quality)             
                element.setLang(lang)
                element.setSubTitle(subtitle)
                element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                element.setType(StreamItem.TYPE_MOVIE)  
                element.setId(movieId) 
                
                elementList.append(element)  
                
            
            # Get All Page
            pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
            for index in range(0, len(pages)):
                page = pages[index]
                
                if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                    
                    element = streamItem.copy()
                    element.setPage(page.text.encode('UTF-8'))
                    element.setTitle('Page '+element.getPage())                  
                    elementList.append(element)
            
            # ___ Close the connection
            response.close()
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList 
    
    def getContentMovieList(self,response,streamItem):
        """
        
        """
        elementList = []
        # ___ Read the source
        content = response.read()
        # ___ Initialize BeautifulSoup       
        soup = BeautifulSoup(content)
       
        # Get All Page
        pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
        for index in range(0, len(pages)):
            page = pages[index]
            
            if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                
                element = streamItem.copy()
                element.setPage(page.text.encode('UTF-8'))
                element.setTitle('Page '+element.getPage())                  
                elementList.append(element)
            
        # For every movie            
        movies = soup.findAll('li',{"class":"item"})
        for index in range(0, len(movies)):
            
            movie = movies[index].find('div',{"class":"resultHeader"})
            link = movie.find("a")
                            
            href = link['href'].encode('UTF-8')
            title = link.text.encode('UTF-8')
            
            # ___ Unescape html on title
            title = strUtil.unescapeHtml(title)
            self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
            # ___ Get  year, quality and lang
            year = strUtil.getYearFromTitle(title) 
            quality = strUtil.getQualityFromTitle(title)  
            lang = strUtil.getLangFromTitle(title) 
            subtitle = strUtil.getSubtitleFromTitle(title)  
            # ___ Clean title
            title = strUtil.cleanTitle(title)                
            self.__LOGGER__.log("Clean title: "+title,xbmc.LOGDEBUG)    
            
            # ___ Get the id of the movie
            patternIdMovie = re.compile('(/film-)(\d*)(-.*)(\.html)')
            match = patternIdMovie.match(href)
            if match is not None:
                movieId=match.group(2)
            else:
                movieId=0
                
            icon = 'http:'+movies[index].find('img',{'class':'thumbImg'})['src'].encode('utf-8')
            synopsis = None
            for index2 in range(0,len( movies[index].findAll('div',{'class':'flt-left'}) )):
                info = movies[index].findAll('div',{'class':'flt-left'})[index2]
                text = info.text.encode('utf-8')
                if text == 'Genre':
                    genre = movies[index].findAll('div',{'class':'flt-left'})[index2+1].find('span',{'class':'itemIntroInfo'}).text.encode('utf-8')
                elif text == 'Année':
                    year = movies[index].findAll('div',{'class':'flt-left'})[index2+1].find('span',{'class':'itemIntroInfo'}).text.encode('utf-8')
                elif text == 'Acteurs':
                    synopsis = movies[index].findAll('div',{'class':'flt-left'})[index2-1].find('span',{'class':'itemIntroInfo'}).text.encode('utf-8')
            
            
            # __ Create the element
            element = StreamItem(title)
            element.setHref(href)                
            element.setYear(year)   
            element.setMetadataGenre(genre) 
            element.setMetadataOverview(synopsis) 
            element.setIconImage(icon)       
            element.setQuality(quality)             
            element.setLang(lang)
            element.setSubTitle(subtitle)
            element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
            element.setType(StreamItem.TYPE_MOVIE)  
            element.setId(movieId)
            
            elementList.append(element)  
            
        
        # Get All Page
        pages = soup.findAll('ul',{'class':'pagination ajax-pagination'})[0].findAll("li")
        for index in range(0, len(pages)):
            page = pages[index]
            
            if page.has_key("class") == False and page.text.encode('UTF-8') != ">" and page.text.encode('UTF-8') != ">>" and page.text.encode('UTF-8') != "<" and page.text.encode('UTF-8') != "<<":
                
                element = streamItem.copy()
                element.setPage(page.text.encode('UTF-8'))
                element.setTitle('Page '+element.getPage())                  
                elementList.append(element)
        
        # ___ Close the connection
        response.close()
        
        return elementList
    
    def getMovieListByGenre(self,streamItem):        
        """
            Method to get an alphabatic list of movie
            @return a list of StreamItem
        """
        page = streamItem.getPage()
        categorie = streamItem.getSubTypeValue()
                   
        hrefPage = 'movies/films_ajax/categorie:' + categorie + '/page:' + str(page)
    
        # ___ Initialize the list to return
        elementList = []
            
        # ___ Try to open the link
        response = self.openPage(hrefPage)
        if response and response.getcode() == 200:
            
            elementList = self.getContentMovieList(response, streamItem)
            
        else:            
            miscFunctions.displayNotification('Unable to open the page '+hrefPage)           
            self.__LOGGER__.log('Connection ERROR : Failed to open page ', xbmc.LOGERROR)
                       
                        
       
        return elementList  
    
    def build_genre_category(self,type):
        """
            Method to display genre menu
        """
        kodiUtil.beginContentDirectory()       
        listGenre = [
                    {'value':'4','label':'Action'},
                    {'value':'41','label':'Animation'},
                    {'value':'42','label':'Aventure'},
                    {'value':'43','label':'Biopic'},
                    {'value':'44','label':'Catastrophe'},
                    {'value':'45','label':'Comédie'},
                    {'value':'46','label':'Court-métrage'},
                    {'value':'106','label':'Divertissement '},
                    {'value':'47','label':'Documentaire'},
                    {'value':'48','label':'Drame'},
                    {'value':'49','label':'En cours de classement'},
                    {'value':'53','label':'Epouvante-horreur'},
                    {'value':'140','label':'Erotique'},
                    {'value':'142','label':'Espionnage'},
                    {'value':'61','label':'Famille'},
                    {'value':'50','label':'Fantastique'},
                    {'value':'51','label':'Guerre'},
                    {'value':'52','label':'Histoire'},
                    {'value':'107','label':'Humour'},
                    {'value':'108','label':'Infos'},
                    {'value':'109','label':'Judiciaire'},
                    {'value':'54','label':'Musical'},
                    {'value':'112','label':'Mystère'},
                    {'value':'110','label':'Médical'},
                    {'value':'113','label':'Paranormal'},
                    {'value':'55','label':'Policier'},
                    {'value':'56','label':'Romance'},
                    {'value':'57','label':'Science-fiction'},
                    {'value':'58','label':'Spectacle'},
                    {'value':'59','label':'Sport'},
                    {'value':'62','label':'Thriller'},
                    {'value':'60','label':'Téléréalité'},
                    {'value':'111','label':'Ufologie'},
                    {'value':'63','label':'Western'},
                    ]
        for genre in listGenre:
            item = StreamItem(genre['label'])
            item.setType(type)
            item.setAction(StreamItem.ACTION_DISPLAY_CATEGORIE_LIST)
            item.setSubType(StreamItem.SUBTYPE_GENRE)
            item.setPage(1)
            item.setSubTypeValue(genre['value'])
            item.addListItemToDirectory()
            
        kodiUtil.endOfDirectory()  
         
    def getSettingsXml(self):
        """
            Method to get the xml settings of the current source
        """
        xmlSettingStr = ''
        xmlSettingStr += '<setting label="DPStream" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_dpstream_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr