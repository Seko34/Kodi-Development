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
import base64
import webUtil
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
class LibertyLand(Source):
    
    
    # ___ The source ID
    ID = 5
    
    # ___ The name of the source
    NAME = 'LibertyLand'
    
    # WEB PAGE BASE
    WEB_PAGE_BASE = "http://libertyvf.com/"
    
    # LOGGER    
    __LOGGER__ = Logger('UltraStream','LibertyLand')
    
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
                     #Source.MENU_MOVIE_LAST,
                     #Source.MENU_MOVIE_TOPVIEW,
                     #Source.MENU_MOVIE_TOPWEEK,
                     #Source.MENU_MOVIE_TOPRATE,
                     #Source.MENU_MOVIE_LIST
                     #Source.MENU_MOVIE_CATEGORY_ALPHA,
                     #Source.MENU_MOVIE_CATEGORY_GENRE
                     ]    
    
    MENU_MOVIE_HD_OPT = []    
    
    MENU_TVSHOW_OPT = [Source.MENU_TVSHOW_SEARCH,
                       #Source.MENU_TVSHOW_LAST,
                       #Source.MENU_TVSHOW_TOPWEEK,
                       #Source.MENU_TVSHOW_TOPRATE,
                       #Source.MENU_TVSHOW_LIST
                       ] 
    
    MENU_ANIME_OPT = [
                      #Source.MENU_ANIME_SEARCH,
                      #Source.MENU_ANIME_LAST,
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
        # Use get http://libertyvf.com/v2/search?q=
        
        href = '/v2/search?q='+webUtil.encodeStr(title)
        response = self.openPage(href)
        
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            soup = BeautifulSoup(content)      
            
            # ___ Get the div for movie       
            moviesDiv = soup.find('div',{'id':'films-search'})
            
            if moviesDiv is not None:
                
                movies = moviesDiv.findAll('div',{'class':'col-lg-3 col-md-3 col-sm-3 col-xs-6'})
                
                for movie in movies:
                    title = movie.find('figcaption').find('a').text.encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)  
                    # __ Create the element
                    element = StreamItem(title)
                    element.setHref( movie.find('figcaption').find('a')['href'].replace('/films/','/films/streaming/').replace('-telecharger-','-'))        
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_MOVIE)
                    element.setIconImage(movie.find('img')['src'])                       
                    element.setSourceId(self.ID)               
                                
                
                    # __ Add the element to the list
                    elementList.append(element)            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(href) + ')', xbmc.LOGERROR)
    
        return elementList
    
    def searchTvShow(self, title):
        """
            Method to search a tv show
            @return a list of StreamItem
        """
        #
        # Use get http://libertyvf.com/v2/search?q=
        
        href = '/v2/search?q='+webUtil.encodeStr(title)
        response = self.openPage(href)
        
        elementList = []
        
        if response and response.getcode() == 200:    
            content = response.read()
            soup = BeautifulSoup(content)      
            
            # ___ Get the div for movie       
            moviesDiv = soup.find('div',{'id':'series-search'})
            
            if moviesDiv is not None:
                
                movies = moviesDiv.findAll('div',{'class':'col-lg-3 col-md-3 col-sm-3 col-xs-6'})
                
                for movie in movies:
                    if movie.find('div',{'class':'titre_stream'}) is None:
                        continue
                    
                    title = movie.find('figcaption').find('a').text.encode('UTF-8')
                    title = strUtil.unescapeHtml(str(title))
                    
                    self.__LOGGER__.log("Finded title: "+title,xbmc.LOGDEBUG)
                    title = strUtil.cleanTitle(title)                
                    self.__LOGGER__.log("Clean title: "+str(title),xbmc.LOGDEBUG)  
                    
                    # __ Create the element
                    element = StreamItem(title)
                    element.setTvShowName(title)
                    element.setHref(movie.find('div',{'class':'titre_stream'}).find('a')['href'])        
                    element.setAction(StreamItem.ACTION_DISPLAY_SEASONS)
                    element.setType(StreamItem.TYPE_TVSHOW)
                    element.setIconImage(movie.find('img')['src'])                  
                    element.setSourceId(self.ID)
                
                    # __ Add the element to the list
                    elementList.append(element)            
            
        # ___ Error during search the movie
        else:
            miscFunctions.displayNotification('Unable to search Movie ' + title)                   
            self.__LOGGER__.log('Connection ERROR : Failed to open page (' + self.buildHref(href) + ')', xbmc.LOGERROR)
    
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
        
        # ___ Get the soup
        soup = self._initOpenPage(tvShowStreamItem)
        
        if soup is not None:
            seasons = soup.find('select',{'id':'saison'}).findAll('option')
            
            for season in seasons:
                seasonNum = season['value']
                title = season.text.encode('UTF-8')
                
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
        pass
    
    
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
            seasons = soup.find('select',{'id':'saison'})
            recupepiPattern = re.compile('(recupepis\(\$\(\'#saison\'\)\.val\(\),\')(\d+)(\',\')(.*?)(\',\'streaming\'\))')
            match = recupepiPattern.match(seasons['onchange'])
            if match is not None:
                id = match.group(2)
                title = match.group(4)
            else:
                return elementList
            
            post_href = '/v2/ajaxepisode.php'
            data = {
                'saison':episodeStreamItem.getSeason(),
                'idserie':id,
                'title':title,
                'typeserie':'streaming'
                }
            response = self.postPage(post_href,data)
            if response and response.getcode() == 200:
                content = response.read()
                # ___ Initialize BeautifulSoup       
                soup = BeautifulSoup(content)                
                # ___ Close the connection
                response.close() 
                
                episodes = soup.findAll('option')
                for episode in episodes:
                    title = episode.text.encode('utf-8')
                    href = episodeStreamItem.getHref()+episode['value']    
                    # __ Create the element                       
                    element = episodeStreamItem.copy()
                    element.setAction(StreamItem.ACTION_DISPLAY_LINKS)
                    element.setType(StreamItem.TYPE_TVSHOW_EPISODE)
                    element.setHref(href)
                    element.determineEpisodeTitle()
                    episodePattern = re.compile('(.*)(Episode )(.*)')
                    match = episodePattern.match(title)
                    if match is not None:  
                        episodeNum = match.group(3)
                        arrayEp = episodeNum.split('-')
                        for ep in arrayEp:
                            element.addEpisode(ep)    
                    
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
        pass
       
    
    def getMovieLink(self,movieStreamItem):
        """
            Method to get all links of a movie
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        soup = None
        id = None
        
        # ___ Extract the id from the link
        idPattern = re.compile('(.*)(films/streaming/)(\d*)?(-)(.*)(\.html)')
        match = idPattern.match(movieStreamItem.getHref())
        if match is not None:  
            id = match.group(3) 
            movieStreamItem.setId(id)
            
        # ___ Get the soup
        soup = self._initOpenPage(movieStreamItem)                        
         
        hosters = soup.findAll('div',{'class':re.compile('(stream hebergeur)(.*)')})   
        
        # ___ For each hoster
        for hoster in hosters:
            # ___ Post http://linkcaptcha.com/getStreamingMovie.php for getting hoster link 
            hosterId = hoster['streaming']
            post_href = 'http://linkcaptcha.com/getStreamingMovie.php'
            data = {'id':hosterId,'id_movie':id,'type':'films'}     
            response = self.postPage(post_href,data,buildHref=False) 
            if response and  response.getcode() ==200:
                content = response.read()
                results = json.loads(content)
                response.close()
                
                hrefPattern = re.compile('<iframe.+?src="(.+?)"(.*)')
                matchHref = hrefPattern.match(results['bande'])
                if matchHref is not None:
                    href = matchHref.group(1)
                    # __ Create the element                       
                    element = movieStreamItem.copy()
                    element.setAction(StreamItem.ACTION_PLAY)
                    element.setType(StreamItem.TYPE_STREAMING_LINK)
                    element.setLang(results['lang'])
                    element.setQuality(results['qualite'])
                    element.setHref(href)               
                    element.regenerateKodiTitle()
                                        
                    self.appendLinkInList(element, elementList)                     
        
        # ___ Find direct download link
        """              
        othersQuality = soup.findAll('a',{'class':'btn btn-info quality_dispo_btn_streaming'})
        for dlQuality in othersQuality:            
            href = dlQuality['href']
            qlty = dlQuality.text.encode('utf-8')
            
            response = self.openPage(href,buildHref=False)
            if response and response.getcode()==200:
                content = response.read()
                # ___ Initialize BeautifulSoup       
                soupQlty = BeautifulSoup(content)  
                response.close()
                
                links = soupQlty.findAll('a',{'class':'ddl_link'})
                for link in links:
                    print link['href']
                    
                    responseLinkCaptacha = self.openPage(link['href'],buildHref=False)
                    if responseLinkCaptacha and responseLinkCaptacha.getcode()==200:
                        contentCaptcha = responseLinkCaptacha.read()
                        # ___ Initialize BeautifulSoup       
                        soupCaptcha = BeautifulSoup(contentCaptcha)  
                        responseLinkCaptacha.close()
                        
                        
                        kPattern = re.compile('(.*)(\'sitekey\': \')(.*?)(\',)(.*)',re.DOTALL)
                        match = kPattern.match(contentCaptcha)
                        if match is not None:
                            kParam = match.group(3);
                            
                            self.processCaptcha(kParam)
                                                           
                            # ___ Refresh the page
                            responseLinkCaptacha = self.openPage(link['href']+'&refresh=1',buildHref=False)
                            if responseLinkCaptacha and responseLinkCaptacha.getcode()==200:
                                contentCaptcha = responseLinkCaptacha.read()
                                # ___ Initialize BeautifulSoup       
                                soupCaptcha = BeautifulSoup(contentCaptcha)  
                                responseLinkCaptacha.close()
                                
                                if soupCaptcha.find('span',{'class':'hidden-links'}) is None:
                                    continue
                                
                                link = soupCaptcha.find('span',{'class':'hidden-links'}).find('a')
                                
                                print link['href']
                                # __ Create the element                       
                                element = movieStreamItem.copy()
                                element.setAction(StreamItem.ACTION_PLAY)
                                element.setType(StreamItem.TYPE_STREAMING_LINK)
                                element.setQuality(qlty)
                                element.setHref(link['href'])               
                                element.regenerateKodiTitle()
        """
        return elementList
    
    def processCaptcha(self,kParam):
        
        vers, language, jsh, questionfile = self._collect_api_info()
                
        
        responseQFile = self.openPage(questionfile,buildHref=False)
        if responseQFile is None or responseQFile.getcode()!=200:
            return
        
        
        # ___ https://www.google.com/recaptcha/api2/anchor?k=
        gurl = 'https://www.google.com/recaptcha/api2/anchor?k='+kParam+'&co=aHR0cDovL2xpbmtjYXB0Y2hhLmNvbTo4MA..&hl='+language+'&v='+vers+'&size=normal&cb=z6ubp1ln1ecg'
                            
        responseAnchor = self.openPage(gurl,buildHref=False)
        if responseAnchor is None or responseAnchor.getcode()!=200:
            return
        
        contentAnchor = responseAnchor.read()
        
        # ___ Initialize BeautifulSoup       
        soupAnchor = BeautifulSoup(contentAnchor)  
        soupAnchor.close()
        
        # ___ Get the captcha token
        token = soupAnchor.find('input', {'id':'recaptcha-token'})
        if token is None:
            return
        
        recaptchaToken = token['value']
        print contentAnchor
        
        return   
        userverifyUrl = 'https://www.google.com/recaptcha/api2/userverify?k='+kParam
        data = {
            'v':'r20171212152908',
            'c':recaptchaToken,
            'response':'eyJyZXNwb25zZSI6IiIsInMiOiI2ZTVhIn0',
            't':771,
            'ct':771,
            'bg':'!QUegR2ZHqovVLlrzLJxBBzBhg5mRh1oHAAAAY1cAAAB-nAOGhu4fgbzGrh0Of91RdQt0tdbJYOeKtFu1_y_v_N4nuCILtj4Cm8f605XqMDHhXJE-k6u9R1qmmgMUX3WJ8wmU439ZzqnyxvMFYewQW02z_gCxsxAUPkMzGaqOat8zy1a48JSgdMe1Bd5QXdJxABqcjfltK52rYsJ8ZePokzTjOZSiNRSm8fI_cU9FOJnjiBjZfLtE8y-a5rUnpAkimAPDXbcwybbu_4J5nvfStYXv4jfI2mFOBKkuNfSNrhrtoXUX83Qv5JbxDNdytuSfzRmq126a46jP-jZIsarKP-Mh9lJTIX4rgE6hxvXWzXBQKF0gwbafsM7yWRfn8_-f_Fv9Y60KV5y7JQK8PfrU546MAGpOmgKhs5nMOPkwwfCKk31IL6rc3deFBG_0TtVG4rGP7ZcDM3w6C0Dd3wIdeEJYpA4yEpgCswaotgnkMpvnoCNgVABLasxkFIOSEzxRpOvNBdo-2z6vLwkNZNOAoMTdL8VWfW5fSbr9qMUJihl5cVHyJm8km3b8HCmI-wkIQXPOVVnFu_tIdHqvKux-InVPGsLgg8eCm8mG7ZphYfsOtezccmYnne9kpduSHRLTUm0tgZqmvEIT0QpyhyYB7RpYzPE2MY43tPoDl0Ap3VsDH_gEvFPpLR0ZLoKZGwmsywLW4NOZxbIPYjWB13i8xdSI3uGrmcYp16jt_-au8TWCkz7eDSc6O77uVw6moB_KbmGmFxNcO-Ob6UhgUHZP3g8dOFcz30SXIeVTiVl8fgsxb6LPuhdf5_x9gE0oYv-91q75TFlB3lC4NIq802g2SouWK72J8S5taQwLY2eVy-Qc4Q5P2q_dV3WraHFBvUeL8kiFwAzOypOfzD3-AEZnKxF3i2MTh7kaTO2cYdmjhhpWMO74YcJYB5ZCQKX8t8JawFZ0pdjFgfTPRK8de9TRM0bI8azbIUNnBtzrKrxrPeP6U8-6NsALgifqhP1PetFc40K0CSPqb-jRDZKT_MrQ66ugTKHyknTRrI0Zqr3uv59g5U7-LBQAh5Yx0iJGdwJU9p0_j_LOilV4GOH0-GDyhTyDzOgMiK9Lml4ErJitZ99bZfZHrjeJXaahhfoTBilxZmf6xMvwCZg_MlXwoGupo4GkEhd9s33SBJ653oRdCpvbQMRIkj77rYBE_ANGIPGtgnnxrl_RIV4ZSCz2MiWIKkF5YjQIHWm_uTM'
            }
        responseVerifyUser = self.postPage(userverifyUrl,data,buildHref=False)
        print responseVerifyUser.read()
        
        print '------'
        
        post_captcha_href = 'http://linkcaptcha.com/verifyCaptchaNew.php'
        data = {'g-recaptcha-response':token['value']}
        responseToken = self.postPage(post_captcha_href,data,buildHref=False)
        print responseToken
        if responseToken and responseToken.getcode()==200:
            print responseToken.read()
            responseToken.close()
   
    def _collect_api_info(self):
        
        #html = self.openPage("http://www.google.com/recaptcha/api.js",buildHref=False).read()
        html = self.openPage('https://www.google.com/recaptcha/api.js?onload=onloadCallback&render=explicit',buildHref=False).read()
        a    = re.search(r'po.src = \'(.*?)\';', html).group(1)
        vers = a.split("/")[5]
        
        questionfile = a
        print ("Fichier questions: %s" % questionfile)

        print ("API version: %s" % vers)

        language = a.split("__")[1].split(".")[0]

        xbmc.log ("API language: %s" % language)

        html = self.openPage("https://apis.google.com/js/api.js",buildHref=False).read()
        b    = re.search(r'"h":"(.*?)","', html).group(1)
        jsh  = b.decode('unicode-escape')

        print ("API jsh-string: %s" % jsh)
        
        return vers, language, jsh, questionfile
    
    def getTvShowEpisodeLink(self,episodeStreamItem):
        """
            Method to get all links of an episode
            @return a list of StreamItem
        """
        # ___ Initialize the list to return
        elementList = []
        soup = None
                    
        # ___ Get the soup
        soup = self._initOpenPage(episodeStreamItem)                        
         
        hosters = soup.findAll('div',{'class':re.compile('(stream hebergeur)(.*)')})   
        
        # ___ For each hoster
        for hoster in hosters:
            # ___ Post http://linkcaptcha.com/getStreamingMovie.php for getting hoster link 
            hosterId = hoster['streaming']
            post_href = 'http://linkcaptcha.com/getStreamingEpisode.php'
            data = {'id':hosterId,'type':'series'}     
            response = self.postPage(post_href,data,buildHref=False) 
            if response and  response.getcode() ==200:
                content = response.read()
                results = json.loads(content)
                response.close()
                
                hrefPattern = re.compile('<iframe.+?src="(.+?)"(.*)')
                matchHref = hrefPattern.match(results['bande'])
                if matchHref is not None:
                    href = matchHref.group(1)
                    # __ Create the element                       
                    element = episodeStreamItem.copy()
                    element.setAction(StreamItem.ACTION_PLAY)
                    element.setType(StreamItem.TYPE_STREAMING_LINK)
                    element.setLang(results['lang'])
                    element.setQuality(results['qualite'])
                    element.setHref(href)               
                    element.regenerateKodiTitle()
                                        
                    self.appendLinkInList(element, elementList)
                    
        return elementList   
    
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
        return []
    
    
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
        xmlSettingStr += '<setting label="LibertyLand" type="lsep"/>\n'
        xmlSettingStr += '<setting id="src_libertyland_activated" type="bool" label="52001" default="true"/>\n'
        return xmlSettingStr