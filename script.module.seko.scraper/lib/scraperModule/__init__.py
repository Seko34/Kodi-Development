# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
    Init class
    Created on 23 aug. 2015
    
    @author: Seko
    @summary: 
'''
#---------------------------------------------------------------------


# ____________________        I M P O R T        ____________________
import os
import xbmc
import xbmcaddon
from pluginScraperTpl import Scraper as PARENT_CLASS

import os
import xbmc
import xbmcgui
from encodings import undefined
from Queue import Queue, Empty
from time import time
import threading
from xbmcgui import DialogProgress

# ____________________     V A R I A B L E S     ____________________
 
# TYPE (and is equal to index of the column in index table)
TYPE_MOVIE = 0
TYPE_SERIE = 1
TYPE_ANIME = 2
TYPE_MOVIE_HD = 3

TYPE_SERIE_DETAILS = 11  
TYPE_ANIME_DETAILS = 12

# The Movie DB Scraper
TMDB_SCRAPER_ID = 2
# The metahandler scraper
METAHANDLER_SCRAPER_ID = 3


# Initialiaze queue
q_in = Queue(0)
q_out = Queue(0)


MODULES_IMPORTED = {}
MODULES_INSTANCES = []

__addon__ = xbmcaddon.Addon(id='script.module.seko.scraper')
__addonDir__ = xbmc.translatePath( __addon__.getAddonInfo('path') )
__pluginPath__ = os.path.join( __addonDir__,'lib','scraperModule','plugins')
__pluginImportPrefix__ = "scraperModule.plugins."


def loadModules():
    """
        Method to load all plugin module
    """
    # ___Get plugins files
    lst = os.listdir(__pluginPath__)
    files = []
    
    for f in lst:
        s = __pluginPath__ + os.sep + f
        if os.path.isfile(s) and os.path.exists(s) and f.endswith('.py') and f != '__init__.py':
            files.append(f[0:len(f)-3])
    # ___ Load the modules
    for file in files:
        MODULES_IMPORTED[file] = __import__(__pluginImportPrefix__ + file, fromlist = ["*"])
    
def createInstances():
    """
        Method to create plugins instance
    """
    for cls in PARENT_CLASS.__subclasses__():
        MODULES_IMPORTED[cls.__name__]
        class_ = getattr(MODULES_IMPORTED[cls.__name__], cls.__name__)
        instance = class_()
        MODULES_INSTANCES.append(instance)
        xbmc.log("[ SCRAPER MODULE ] Load module %s" % (cls.__name__), xbmc.LOGINFO)

def getScraper(scraperId):
    """
        Method to get the selected scraper
        
        @param scraperId: The scraper id
        
        @return the scraper
    """
    scraper = None
    
    for inst in MODULES_INSTANCES:
        if str(inst.getId()) == str(scraperId):
            return inst
        
    return None

def getMetadata(scraperId, type, title, season=False, episode=False):
    """
        Method to get metadata
        
        @param type: the type of element to search
        @param title: the title of the element
        @param season: the season for a tv show or an anime
        @param episode: the episode for a tv show or an anime
        
        @return metadata for the element
        
    """
    scraper = getScraper(scraperId)
    if scraper is not None:
        if type == TYPE_MOVIE or type == TYPE_MOVIE_HD:
            return scraper.getMovieMeta(title)
        
        if type == TYPE_SERIE:        
            return scraper.getTvShowMeta(title)
        
        if type == TYPE_SERIE_DETAILS:        
            if episode and episode !='':
                if isinstance(episode, list):
                    return scraper.getTvShowDetailsMeta(title, season, episode[0])                
                else:
                    return scraper.getTvShowDetailsMeta(title, season, episode)
            else:
                return scraper.getTvShowDetailsMeta(title, season)
        if type == TYPE_ANIME:        
            return scraper.getAnimeMeta(title)
        
        if type == TYPE_ANIME_DETAILS:
            return scraper.getAnimeDetailsMeta(title, season, episode)
    
    return None   


def getMetadatas(scraperId, type,elementList, nbThread=1, dialogProgress=False):
    """
        Method to get all informations for a list of elements
        
        
        @param the scraper id to use
        @param the type of element to get information
        @param the list of elements to update
        
        @return the list of elements updated
    """
    
    xbmc.log("Search the metadata",xbmc.LOGINFO)
    
    if nbThread > 1:
        # ___ Add all element title to the input queue
        for element in elementList:
                
            if  'metadata' in element:
                if str(type) == str(TYPE_MOVIE_HD) :
                    if 'quality' in element:
                        q_in.put((element['title'],element['quality']))
                    else:
                        q_in.put((element['title'],''))
                        
                elif str(type) == str(TYPE_SERIE_DETAILS) :
                    if str(element['type']) == '11':
                        q_in.put((element['tvShow'], element['season'], element['title']))
                    else:
                        # ___ If the episode is empty, get the season detail
                        if element['episode'] == '':
                            q_in.put((element['tvShow'], element['season'], element['title']))                    
                        else:
                            q_in.put((element['tvShow'], element['season'], element['episode'], element['href']))
                          
                elif str(type) == str(TYPE_ANIME_DETAILS) :
                    if str(element['type']) == '21':
                        q_in.put((element['tvShow'], element['season'], element['title']))
                    else:
                        q_in.put((element['tvShow'], element['season'], element['episode'], element['href']))           
                else:
                    q_in.put(element['title'])
                    
        # ___ Return the list updated after running all threads 
        return startThreadForScraper(scraperId, type, elementList, nbThread, dialogProgress)
    
    # ___ Case of one thread
    else:        
        
        count = 0    
        
        total = len(elementList)
        if dialogProgress:
            dialogProgress.update(0,__addon__.getLocalizedString(70003),__addon__.getLocalizedString(70004)+'0'+'%')
        for element in elementList:
            # Remove result on q_out, and wait 500ms to avoid a race condition
            count += 1
            percent = int((count*100)/total)
            if dialogProgress:
                dialogProgress.update(percent,__addon__.getLocalizedString(70003),__addon__.getLocalizedString(70004)+str(percent)+'%')
            if  'metadata' in element:
                if str(type) == str(TYPE_MOVIE_HD) or str(type) == str(TYPE_MOVIE) :
                    metas = getMetadata(scraperId, TYPE_MOVIE, element['title'])
                    if metas is not None:
                        element['metadata'] = metas['info']
                    
                elif str(type) == str(TYPE_SERIE) :
                    metas = getMetadata(scraperId, TYPE_SERIE, element['tvShow'])
                    if metas is not None:
                        element['metadata'] = metas['info']
                        
                elif str(type) == str(TYPE_SERIE_DETAILS) :
                    if str(element['type']) == '11':
                        metas = getMetadata(scraperId, TYPE_SERIE_DETAILS, element['tvShow'],element['season'])
                        if metas is not None:
                            element['metadata'] = metas['info']
                    else:
                        # ___ If the episode is empty, get the season detail
                        if element['episode'] == '':
                            metas = getMetadata(scraperId, TYPE_SERIE_DETAILS, element['tvShow'],element['season'])
                            if metas is not None:
                                element['metadata'] = metas['info']                 
                        else:
                            metas = getMetadata(scraperId, TYPE_SERIE_DETAILS, element['tvShow'],element['season'],element['episode'])
                            if metas is not None:
                                element['metadata'] = metas['info']
                          
                elif str(type) == str(TYPE_ANIME) :
                    metas = getMetadata(scraperId, TYPE_ANIME, element['tvShow'])
                    if metas is not None:
                        element['metadata'] = metas['info'] 
                                                         
                elif str(type) == str(TYPE_ANIME_DETAILS) :
                    if str(element['type']) == '21':
                        metas = getMetadata(scraperId, TYPE_ANIME_DETAILS, element['tvShow'],element['season'])
                        if metas is not None:
                            element['metadata'] = metas['info']
                    else:
                            metas = getMetadata(scraperId, TYPE_ANIME_DETAILS, element['tvShow'],element['season'],element['episode'])
                            if metas is not None:
                                element['metadata'] = metas['info']          
                else:
                    pass
                    """
                    metas = getMetadata(scraperId, TYPE_MOVIE, element['title'])
                    if metas is not None:
                        element['metadata'] = metas['info']
                    """
        return elementList
          
    
def startThreadForScraper(scraperId, type, elementList, nbThread, dialogProgress=False):
    """
        Method to start all thread for scrapper
        
        @param the scraper id to use
        @param the type of element to get information
        @param the list of elements to update
        
        @return the list of elements updated
    """
    
    def getMovieHdInfo():
        """
            Method to get information for a movie hd
        """                   
        try:
            while True:
                name, quality = q_in.get_nowait()                            
                                    
                metas = getMetadata(scraperId, TYPE_MOVIE, name)
                if metas is not None:
                    metas['info']['title']=name
                else:
                    metas = {'info':{'title':name}}
                
                q_out.put((name,quality,metas))
        except Empty:
            # q_in is empty, it s finished
            pass
                
    def getMovieInfo():
        """
            Method to get information for a movie
        """                    
        try:
            while True:                         
                
                name = q_in.get_nowait()   
                
                metas = getMetadata(scraperId, TYPE_MOVIE, name)
                if metas is not None:
                    metas['info']['title']=name
                else:
                    metas = {'info':{'title':name}}
                    
                q_out.put((name, metas))
                
        except Empty:
            # q_in is empty, it s finished
            pass
                
    def getSerieInfo():
        """
            Method to get information for a serie
        """                  
        try:
            while True:                         
                
                name = q_in.get_nowait()   
                
                metas = getMetadata(scraperId, TYPE_SERIE, name)
                if metas is not None:
                    metas['info']['title']=name
                else:
                    metas = {'info':{'title':name}}
                q_out.put((name, metas))
                
        except Empty:
            # q_in is empty, it s finished
            pass
        
    def getAnimeInfo():
        """
            Method to get information for a anime
        """                  
        try:
            while True:                         
                
                name = q_in.get_nowait()   
                
                metas = getMetadata(scraperId, TYPE_ANIME, name)
                if metas is not None:
                    metas['info']['title']=name
                else:
                    metas = {'info':{'title':name}}
                q_out.put((name, metas))
                
        except Empty:
            # q_in is empty, it s finished
            pass
        
    def getDetailsSerieInfo():
        """
            Method to get details information for a serie (season and episode)
        """                  
        try:
            while True:                         
                
                element = q_in.get_nowait()  
                                     
                name = element[0]
                   
                # ___ Case of season                                  
                if len(element) == 3:                       
                    season = element[1]                           
                    displayName = element[2]
                      
                    metas = getMetadata(scraperId, TYPE_SERIE_DETAILS, name,season)
                    if metas is None:
                        metaseries = {'seriesName' : name, 'episode':'', 'season':season, 'title':displayName}
                        metas = {'info':metaseries}
                    else:                        
                        metas['info']['title'] = str(displayName)    
                        
                    q_out.put((displayName, metas))
                        
                # ___ Case of episode        
                elif len(element) == 4:                        
                    season = element[1]
                    episode = element[2]
                    url = element[3]
                    xbmc.log("Get metadata for season "+str(season)+" - Ep "+str(episode), xbmc.LOGINFO)
                    
                    metas = getMetadata(scraperId, TYPE_SERIE_DETAILS, name,season,episode)
                    if metas is None:
                        metaseries = {'seriesName' : name, 'episode':episode, 'season':season, 'title':name+' S'+str(season)+'E'+str(episode)}
                        metas = {'info':metaseries} 
                    else:
                        metas['info']['title'] = name  
                        
                    # __ Add the serie's name to informations  (Needed for history) 
                    q_out.put((url, metas))
                                            
        except Empty:
            # q_in is empty, it s finished
            pass
        
    def getDetailsAnimeInfo():
        """
            Method to get details information for a anime (season and episode)
        """                  
        try:
            while True:                         
                
                element = q_in.get_nowait()                    
                name = element[0]
                   
                # ___ Case of season                                  
                if len(element) == 3:                       
                    season = element[1]                           
                    displayName = element[2]
                      
                    metas = getMetadata(scraperId, TYPE_ANIME_DETAILS, name,season)
                    if metas is None:
                        metaseries = {'seriesName' : name, 'episode':'', 'season':season, 'title':displayName}
                        metas = {'info':metaseries}
                    else:
                        metas['info']['title'] = str(displayName)    
                        
                    q_out.put((displayName, metas))
                        
                # ___ Case of episode        
                elif len(element) == 4:                        
                    season = element[1]
                    episode = element[2]
                    url = element[3]
                    xbmc.log("Get metadata for season "+str(season)+" - Ep "+str(episode), xbmc.LOGINFO)
                    
                    metas = getMetadata(scraperId, TYPE_ANIME_DETAILS, name,season,episode)
                    if metas is None:
                        metaseries = {'seriesName' : name, 'episode':episode, 'season':season, 'title':name+' S'+str(season)+'E'+str(episode)}
                        metas = {'info':metaseries} 
                    else:
                        metas['info']['title'] = name  
                        
                    # __ Add the serie's name to informations  (Needed for history) 
                    q_out.put((url, metas))
                                            
        except Empty:
            # q_in is empty, it s finished
            pass
              
              
    # __ Start threads for the selected type
    start = time()
    for index in xrange(nbThread):
        if str(type) == str(TYPE_MOVIE_HD):  
            t = threading.Thread(target = getMovieHdInfo)
            t.start()
        elif str(type) == str(TYPE_MOVIE):   
            t = threading.Thread(target = getMovieInfo)
            t.start()                 
        elif str(type) == str(TYPE_SERIE):  
            t = threading.Thread(target = getSerieInfo)
            t.start()  
        elif str(type) == str(TYPE_SERIE_DETAILS):
            t = threading.Thread(target = getDetailsSerieInfo)
            t.start() 
        elif str(type) == str(TYPE_ANIME):
            t = threading.Thread(target = getAnimeInfo)
            t.start()  
        elif str(type) == str(TYPE_ANIME_DETAILS):
            t = threading.Thread(target = getDetailsAnimeInfo)
            t.start() 
    count = 0    
    
    total = len(elementList)
    if dialogProgress:
        dialogProgress.update(0,__addon__.getLocalizedString(70003),__addon__.getLocalizedString(70004)+'0'+'%')
        
    # While there are actif thread or available result in q_out
    while threading.activeCount() > 1 or not q_out.empty():
        try:
            # Remove result on q_out, and wait 500ms to avoid a race condition
            count += 1
            percent = int(((total-int(q_in.qsize()))*100)/total)
            if dialogProgress:
                dialogProgress.update(percent,__addon__.getLocalizedString(70003),__addon__.getLocalizedString(70004)+str(percent)+'%')
                
            # ___ Case of Movie HD
            if str(type) == str(TYPE_MOVIE_HD):                                
                name, quality, metas = q_out.get(True, 0.25)
                
                for element in elementList:                    
                    if str(element['title']) == name:
                        element['metadata'] = metas['info']
                        
            
            # ___ Case of TV Show details or Anime details
            elif str(type) == str(TYPE_SERIE_DETAILS) or str(type) == str(TYPE_ANIME_DETAILS): 
                name,metas = q_out.get(True, 0.25) 
                for element in elementList:                    
                    if str(element['href']) == name or str(element['title']) == name:
                        element['metadata'] = metas['info'] 
                                            
            # ___ Other
            else:
                name, metas = q_out.get(True, 0.25)
                for element in elementList:                    
                    if str(element['title']) == name:
                        element['metadata'] = metas['info']    
            
        except Empty:
            # q_out is empty, it s finished
            pass
        
    xbmc.log("%d informations recovered in  %f seconds" % (count, time() - start),xbmc.LOGINFO)
    return elementList



loadModules()
createInstances()