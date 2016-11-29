# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 Sept 2014

@author: Seko
@summary: themoviedb.org scrapper
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import urllib
import urllib2
import json
import xbmc
import re
from scraperModule.pluginScraperTpl import Scraper


class TMDBScraper(Scraper):
    
    # ____________________     OVERRIDE VARIABLES    ____________________
    name = "The Movie DB Scraper"
    id = 1
            
    # ____________________     V A R I A B L E S     ____________________
            
    # WEB PAGE BASE
    API_PAGE_BASE = "https://api.themoviedb.org/3/"
    
    # WEB PAGE BASE
    IMAGE_PAGE_BASE = "http://image.tmdb.org/t/p/"
    
    # API KEY FOR THEMOVIEDB
    API_KEY = "47565088b22296f33e76445d59403e15"
    
    # self.LANGUAGE
    LANGUAGE = "fr"
    
    # IMAGE SIZE
    IMAGE_SIZE = ['w92', 'w154', 'w185', 'w342', 'w500', 'original']
    
    # DEFAULT IMAGE SIZE
    DEFAULT_IMAGE_SIZE ='w342'
    
    # DEFAULT FANART SIZE
    DEFAULT_FANART_IMAGE_SIZE ='original'
    
    # Header configuration
    HEADER_CFG = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-self.LANGUAGE': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
    
    
    def openPage(self,url):
        """
            Method to open a page
            @param url: url of the page
            @return the response of the request
        """
        
        try:    
            request = urllib2.Request(url, headers=self.HEADER_CFG)
            response = urllib2.urlopen(request)
        except:
            response = None
            
        return response
    
    def movieNameTreatment(self,movieName):
        """
            Method to change the movie name
                -Remove the date in the movie name
            @param movieName: the name to process
            
            @param the processed name
        """
        
        # ___ Remove the date in the name
        patternDate = re.compile('.*\\(\d{4}\\)')
        match = patternDate.match(movieName.strip())
            
        if match is not None:
            movieName = movieName[0:movieName.rfind('(')]
        
        return movieName.strip()
            
    def getYearFromName(self,movieName):
        """
            Method to get the year in the name
            @param movieName: the name
            
            @return the year
        """
        patternDate = re.compile('.*\\(\d{4}\\)')
        match = patternDate.match(movieName.strip())
        if match is not None:        
            year = movieName[movieName.rfind(')')-4:movieName.rfind(')')]
        else:
            year = None
        
        return year
    
    def searchMovie(self,movie):
        """
            Method to search a movie
            Example of url : https://api.themoviedb.org/3/search/movie?api_key=47565088b22296f33e76445d59403e15&query=300&language=fr&page=1
            
            @param movie: the name of the movie
            
            @return the movie element (JSON) from themoviedb.org
            
            @warning: the returned element could be null
        """ 
        
        url = self.API_PAGE_BASE+"search/movie?api_key="+self.API_KEY+"&language="+self.LANGUAGE+"&query="+urllib.quote_plus(self.movieNameTreatment(movie))+"&page=1"
        
        if self.getYearFromName(movie) is not None:
            url+="&year="+self.getYearFromName(movie)
            
          
        xbmc.log("Search URL in themoviedb.org : "+url,xbmc.LOGINFO)
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get the first element
            if len(jsonResponse['results']) > 0:
                firstElement = jsonResponse['results'][0]
    
                return firstElement
            else:
                xbmc.log('Search ERROR : Failed to search the movie "'+movie+'" on TheMovieDb.org', xbmc.LOGERROR) 
        else:                              
            xbmc.log('Connection ERROR : Failed to search the movie "'+movie+'" on TheMovieDb.org', xbmc.LOGERROR)  
        
        return None 
        
    def searchSerie(self,serie):
        """
            Method to search a serie
            Example of url : https://api.themoviedb.org/3/search/tv?api_key=47565088b22296f33e76445d59403e15&query=Friends&language=fr&page=1
            
            @param serie: the name of the serie
            
            @return the serie element (JSON) from themoviedb.org
            
            @warning: the returned element could be null
        """ 
        
        url = self.API_PAGE_BASE+"search/tv?api_key="+self.API_KEY+"&language="+self.LANGUAGE+"&query="+urllib.quote_plus(self.movieNameTreatment(serie))+"&page=1"
        
        if self.getYearFromName(serie) is not None:
            url+="&first_air_date_year="+self.getYearFromName(serie)
            
        
        xbmc.log("Search URL in themoviedb.org : "+url,xbmc.LOGINFO)
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get the first element
            if len(jsonResponse['results']) > 0:
                firstElement = jsonResponse['results'][0]
    
                return firstElement
            else:
                xbmc.log('Search ERROR : Failed to search the movie "'+serie+'" on TheMovieDb.org', xbmc.LOGERROR) 
        else:                              
            xbmc.log('Connection ERROR : Failed to search the movie "'+serie+'" on TheMovieDb.org', xbmc.LOGERROR)  
        
        return None 
        
    def getMovie(self,movieId):
        """
            Method to get the details of a movie
            Example: https://api.themoviedb.org/3/movie/1271?api_key=47565088b22296f33e76445d59403e15&query=300&language=fr&append_to_response=images,credits,videos&include_image_language=fr,en
            
            @param the movie id in themoviedb.org
            
            @return a Dictionnary with the format:
                {'info': info ,'iconImage': iconImage,'thumbnailImage': thumbnailImage}
        """
        url = self.API_PAGE_BASE+"movie/"+str(movieId)+"?api_key="+self.API_KEY+"&language="+self.LANGUAGE+"&append_to_response=images,credits,videos&include_image_language='"+self.LANGUAGE+",en"
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get genres        
            genreStr=""
            for genre in jsonResponse['genres']:
                if genreStr=="":
                    genreStr+=genre['name']
                else:
                    genreStr+=', '+genre['name']
                
            # Get cast       
            castStr=list()
            for cast in jsonResponse['credits']['cast']:
                castStr.append(cast['name'])
           
            # Get cast and roles
            castRoleStr=list()
            for cast in jsonResponse['credits']['cast']:                    
                    castRoleStr.append(cast['name']+"|"+cast['character'])           
                    
            # Studio
            studioStr=""
            for studio in jsonResponse['production_companies']:
                if studioStr=="":
                    studioStr+=studio['name']
                else:
                    studioStr+=', '+studio['name']
            # Trailer
            trailerurl=''
            if len(jsonResponse['videos']['results'])>0:
                trailerurl=jsonResponse['videos']['results'][0]['key']
            
            # Image
            if jsonResponse['poster_path'] is not None:
                image = self.IMAGE_PAGE_BASE+self.DEFAULT_IMAGE_SIZE+jsonResponse['poster_path']
            else:
                image=""  
            
            #print "Title : "+jsonResponse['title']+" - Id : "+str(jsonResponse['id'])+" - Overview : "+jsonResponse['overview']
            xbmcInfo = {
                         'genre':genreStr
                        ,'year':jsonResponse['release_date'][0:4]
                        ,'episode':''
                        ,'season':''
                        ,'top250':''
                        ,'tracknumber':''
                        ,'rating':jsonResponse['vote_average']
                        #,'watched':''
                        #,'playcount played':''
                        #,'overlayfor values':''
                        ,'cast':castStr
                        ,'castandrole':castRoleStr
                        #,'director':''
                        #,'mpaa':''
                        ,'plot':jsonResponse['overview']
                        #,'plotoutline':''
                        ,'title':jsonResponse['title']
                        ,'originaltitle':jsonResponse['original_title']
                        ,'duration':jsonResponse['runtime']
                        ,'studio':studioStr
                        ,'tagline movie':jsonResponse['tagline']
                        #,'writer':''
                        #,'tvshowtitle':''
                        ,'premiered':jsonResponse['release_date']
                        ,'status':jsonResponse['status']
                        ,'code':jsonResponse['imdb_id']
                        #,'aired':''
                        #,'credits':''
                        #,'lastplayed':''
                        #,'album':''
                        ,'votes':jsonResponse['vote_count']
                        ,'trailer':trailerurl
                        ,'picturepath':image
                        ,'fanart_image':self.IMAGE_PAGE_BASE+self.DEFAULT_FANART_IMAGE_SIZE+jsonResponse['backdrop_path'] if jsonResponse['backdrop_path'] is not None else ''
                        ,'seriesName' : ''
                       }
            
            iconImage=image
            thumbnailImage=iconImage
            
            return {'info':xbmcInfo,'iconImage':iconImage,'thumbnailImage':thumbnailImage}
        
        else:                              
            xbmc.log('Connection ERROR : Failed to get the details of the movie with id "'+movieId+'" on TheMovieDb.org', xbmc.LOGERROR)
        
        return None
       
    
    def getSerie(self,serieId):
        """
            Method to get the details of a serie
            Example: https://api.themoviedb.org/3/tv/1668?api_key=47565088b22296f33e76445d59403e15&query=300&language=fr&append_to_response=images,credits,videos&include_image_language=fr,en
            
            @param the serie id in themoviedb.org
            
            @return a Dictionnary with the format:
                {'info': info ,'iconImage': iconImage,'thumbnailImage': thumbnailImage}
        """
        url = self.API_PAGE_BASE+"tv/"+str(serieId)+"?api_key="+self.API_KEY+"&language="+self.LANGUAGE+"&append_to_response=images,credits,videos&include_image_language='"+self.LANGUAGE+",en"
       
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get genres        
            genreStr=""
            for genre in jsonResponse['genres']:
                if genreStr=="":
                    genreStr+=genre['name']
                else:
                    genreStr+=', '+genre['name']
                
            # Get cast       
            castStr=list()
            for cast in jsonResponse['credits']['cast']:
                castStr.append(cast['name'])
           
            # Get cast and roles
            castRoleStr=list()
            for cast in jsonResponse['credits']['cast']:                    
                    castRoleStr.append(cast['name']+"|"+cast['character'])           
                    
            # Studio
            studioStr=""
    
            # Trailer
            trailerurl=''
            if len(jsonResponse['videos']['results'])>0:
                trailerurl=jsonResponse['videos']['results'][0]['key']
                
            # Director
            director = ''
            if dir in jsonResponse['created_by']:
                if director == '':
                    director+=dir['name']
                else:
                    director+=', '+dir['name']                
            
            # Image
            if jsonResponse['poster_path'] is not None:
                image = self.IMAGE_PAGE_BASE+self.DEFAULT_IMAGE_SIZE+jsonResponse['poster_path']
            else:
                image=""  
            
            #print "Title : "+jsonResponse['title']+" - Id : "+str(jsonResponse['id'])+" - Overview : "+jsonResponse['overview']
            xbmcInfo = {
                         'genre':genreStr
                        ,'year':jsonResponse['first_air_date'][0:4] if jsonResponse['first_air_date'] is not None else ''
                        ,'episode':jsonResponse['number_of_episodes']
                        ,'season':jsonResponse['number_of_seasons']
                        ,'top250':''
                        ,'tracknumber':''
                        ,'rating':jsonResponse['vote_average']
                        #,'watched':''
                        #,'playcount played':''
                        #,'overlayfor values':''
                        ,'cast':castStr
                        ,'castandrole':castRoleStr
                        ,'director':director
                        #,'mpaa':''
                        ,'plot':jsonResponse['overview']
                        #,'plotoutline':''
                        ,'title':jsonResponse['name']
                        ,'originaltitle':jsonResponse['original_name']
                        #,'duration':jsonResponse['runtime']
                        ,'studio':studioStr
                        #,'tagline movie':jsonResponse['tagline']
                        #,'writer':''
                        ,'tvshowtitle':jsonResponse['original_name']
                        ,'premiered':jsonResponse['first_air_date']
                        ,'status':jsonResponse['status']
                        ,'code':jsonResponse['id']
                        #,'aired':''
                        #,'credits':''
                        #,'lastplayed':''
                        #,'album':''
                        ,'votes':jsonResponse['vote_count']
                        ,'trailer':trailerurl
                        ,'picturepath':image
                        ,'fanart_image':self.IMAGE_PAGE_BASE+self.DEFAULT_FANART_IMAGE_SIZE+jsonResponse['backdrop_path'] if jsonResponse['backdrop_path'] is not None else ''
                        ,'seriesName' : ''
                       }
            
            iconImage=image
            thumbnailImage=iconImage
            
            return {'info':xbmcInfo,'iconImage':iconImage,'thumbnailImage':thumbnailImage}
        
        else:                              
            xbmc.log('Connection ERROR : Failed to get the details of the movie with id "'+serieId+'" on TheMovieDb.org', xbmc.LOGERROR)
        
        return None
    
    def getSaison(self, serieId, season, serieName=False):
        """
            Method to get the details of a serie
            Example: https://api.themoviedb.org/3/tv/1668/season/2?api_key=47565088b22296f33e76445d59403e15&query=300&language=en&append_to_response=images,credits,videos&include_image_language=fr,en
            
            @note : All details are in English
            
            @param the serie id in themoviedb.org
            
            @return a Dictionnary with the format:
                {'info': info ,'iconImage': iconImage,'thumbnailImage': thumbnailImage}
        """
        url = self.API_PAGE_BASE+"tv/"+str(serieId)+"/season/"+str(season)+"?api_key="+self.API_KEY+"&language=en&append_to_response=images,credits,videos&include_image_language="+self.LANGUAGE+",en"
        xbmc.log("Search URL in themoviedb.org : "+url,xbmc.LOGINFO)
       
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get genres        
            genreStr=""
            if 'genres' in jsonResponse:
                for genre in jsonResponse['genres']:
                    if genreStr=="":
                        genreStr+=genre['name']
                    else:
                        genreStr+=', '+genre['name']
                
            # Get cast       
            castStr=list()
            for cast in jsonResponse['credits']['cast']:
                castStr.append(cast['name'])
           
            # Get cast and roles
            castRoleStr=list()
            for cast in jsonResponse['credits']['cast']:                    
                    castRoleStr.append(cast['name']+"|"+cast['character'])           
                    
            # Studio
            studioStr=""
    
            # Trailer
            trailerurl=''
            if len(jsonResponse['videos']['results'])>0:
                trailerurl=jsonResponse['videos']['results'][0]['key']
                
            # Director
            director = ''         
            
            # Image
            if jsonResponse['poster_path'] is not None:
                image = self.IMAGE_PAGE_BASE+self.DEFAULT_IMAGE_SIZE+jsonResponse['poster_path']
            else:
                image=""
     
            # Serie's name
            if not serieName:
                serieName = ''
                
            xbmcInfo = {
                         'genre':genreStr
                        ,'year':jsonResponse['air_date'][0:4] if jsonResponse['air_date'] is not None else ''
                        ,'episode':''
                        ,'season':season
                        ,'top250':''
                        ,'tracknumber':''
                        ,'rating':''
                        #,'watched':''
                        #,'playcount played':''
                        #,'overlayfor values':''
                        ,'cast':castStr
                        ,'castandrole':castRoleStr
                        ,'director':director
                        #,'mpaa':''
                        ,'plot':jsonResponse['overview']
                        #,'plotoutline':''
                        ,'title':jsonResponse['name']
                        ,'originaltitle':jsonResponse['name']
                        #,'duration':jsonResponse['runtime']
                        ,'studio':studioStr
                        #,'tagline movie':jsonResponse['tagline']
                        #,'writer':''
                        ,'tvshowtitle':jsonResponse['name']
                        ,'premiered':jsonResponse['air_date']
                        ,'status':''
                        ,'code':jsonResponse['id']
                        #,'aired':''
                        #,'credits':''
                        #,'lastplayed':''
                        #,'album':''
                        ,'votes':''
                        ,'trailer':trailerurl
                        ,'picturepath':image
                        ,'fanart_image':self.IMAGE_PAGE_BASE+self.DEFAULT_FANART_IMAGE_SIZE+jsonResponse['backdrop_path'] if 'backdrop_path' in jsonResponse and jsonResponse['backdrop_path'] is not None else ''
                        ,'seriesName' : serieName
                       }
            
            iconImage=image
            thumbnailImage=iconImage
            
            return {'info':xbmcInfo,'iconImage':iconImage,'thumbnailImage':thumbnailImage}
        
        else:                              
            xbmc.log('Connection ERROR : Failed to get the details of the movie with id "'+serieId+'" on TheMovieDb.org', xbmc.LOGERROR)
        
        return None
    
    
    def getEpisode(self, serieId, season, episode, serieName=False):
        """
            Method to get the details of an episode
            Example: https://api.themoviedb.org/3/tv/1668/season/2/episode/15?api_key=47565088b22296f33e76445d59403e15&query=300&language=fr&append_to_response=images,credits,videos&include_image_language=fr,en
            
            @note : All details are in English
            
            @param the serie id in themoviedb.org
            
            @return a Dictionnary with the format:
                {'info': info ,'iconImage': iconImage,'thumbnailImage': thumbnailImage}
        """
        url = self.API_PAGE_BASE+"tv/"+str(serieId)+"/season/"+str(season)+"/episode/"+str(episode)+"?api_key="+self.API_KEY+"&language=en&append_to_response=images,credits,videos&include_image_language="+self.LANGUAGE+",en"
        xbmc.log("Search URL in themoviedb.org : "+url,xbmc.LOGINFO)
       
        response = self.openPage(url)
        
        if response and response.getcode() == 200:
            # Read the response
            jsonResponse = json.loads(response.read())
            
            # Get genres        
            genreStr=""
            if 'genres' in jsonResponse:
                for genre in jsonResponse['genres']:
                    if genreStr=="":
                        genreStr+=genre['name']
                    else:
                        genreStr+=', '+genre['name']
                
            # Get cast       
            castStr=list()
            for cast in jsonResponse['credits']['cast']:
                castStr.append(cast['name'])
           
            # Get cast and roles
            castRoleStr=list()
            for cast in jsonResponse['credits']['cast']:                    
                    castRoleStr.append(cast['name']+"|"+cast['character'])           
                    
            # Studio
            studioStr=""
    
            # Trailer
            trailerurl=''
            if len(jsonResponse['videos']['results'])>0:
                trailerurl=jsonResponse['videos']['results'][0]['key']
                
            # Director
            director = ''
            
            # Image
            if 'still_path' in jsonResponse and jsonResponse['still_path'] is not None:
                image = self.IMAGE_PAGE_BASE+self.DEFAULT_IMAGE_SIZE+jsonResponse['still_path']
            else:
                image=""  
            
            # Serie's name
            if not serieName:
                serieName = '' 
                
            xbmcInfo = {
                         'genre':genreStr
                        ,'year':jsonResponse['air_date'][0:4] if jsonResponse['air_date'] is not None else ''
                        ,'episode':episode
                        ,'season':season
                        ,'top250':''
                        ,'tracknumber':''
                        ,'rating':''
                        #,'watched':''
                        #,'playcount played':''
                        #,'overlayfor values':''
                        ,'cast':castStr
                        ,'castandrole':castRoleStr
                        ,'director':director
                        #,'mpaa':''
                        ,'plot':jsonResponse['overview']
                        #,'plotoutline':''
                        ,'title':jsonResponse['name']
                        ,'originaltitle':jsonResponse['name']
                        #,'duration':jsonResponse['runtime']
                        ,'studio':studioStr
                        #,'tagline movie':jsonResponse['tagline']
                        #,'writer':''
                        ,'tvshowtitle':jsonResponse['name']
                        ,'premiered':jsonResponse['air_date']
                        ,'status':''
                        ,'code':jsonResponse['id']
                        #,'aired':''
                        #,'credits':''
                        #,'lastplayed':''
                        #,'album':''
                        ,'votes':''
                        ,'trailer':trailerurl
                        ,'picturepath':image
                        ,'fanart_image':self.IMAGE_PAGE_BASE+self.DEFAULT_FANART_IMAGE_SIZE+jsonResponse['backdrop_path'] if 'backdrop_path' in jsonResponse and jsonResponse['backdrop_path'] is not None else ''
                        ,'seriesName' : serieName
                       }
            
            iconImage=image
            thumbnailImage=iconImage
            
            return {'info':xbmcInfo,'iconImage':iconImage,'thumbnailImage':thumbnailImage}
        
        else:                              
            xbmc.log('Connection ERROR : Failed to get the details of the movie with id "'+str(serieId)+'" on TheMovieDb.org', xbmc.LOGERROR)
        
        return None



    def getMovieMeta(self, title, params=None):
        """
            Override getMovieMeta
        """
        movieEl = self.searchMovie(title)
        if movieEl is not None:
            return self.getMovie(movieEl['id'])
        else:   
            return None
        
    def getTvShowMeta(self, title, params=None):
        """
            Override getTvShowMeta
        """
        tvShowEl = self.searchSerie(title)
        if tvShowEl is not None:
            return self.getSerie(tvShowEl['id'])
        else:   
            return None
    
    def getTvShowDetailsMeta(self, title, season, episode=False, params=None):
        """
            Override getTvShowDetailsMeta
        """
        tvShowEl = self.searchSerie(title)
        if tvShowEl is not None:
            if not episode or episode == '':
                return self.getSaison(tvShowEl['id'], season, title)
            else:
                return self.getEpisode(tvShowEl['id'], season, episode, title)
        else:   
            return None
    
   
