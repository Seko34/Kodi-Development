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
import sys
import xbmc
import xbmcaddon
import xbmcgui
import strUtil
import constant
import timeit
from item import StreamItem
from difflib import SequenceMatcher as SM

from sourceTemplate import streamingSourceTemplate as PARENT_CLASS


MODULES_IMPORTED = {}
MODULES_INSTANCES = []

# ___ Change for test
if sys.argv[0].endswith('test.py'):
    constant.__coreAddonDir__ = sys.argv[2]

__sourcesPath__ = os.path.join( constant.__coreAddonDir__,'resources','lib','src_mod','sources')

__pluginImportPrefix__ = "resources.lib.src_mod.sources."
__pluginImportPrefixForService__ = "src_mod.sources."

def loadModules():
    """
        Method to load all plugin module
    """
    # ___Get plugins files
    lst = os.listdir(__sourcesPath__)
    files = []
    
    for f in lst:
        s = __sourcesPath__ + os.sep + f
        if os.path.isfile(s) and os.path.exists(s) and f.endswith('.py') and f != '__init__.py':
            files.append(f[0:len(f)-3])
    # ___ Load the modules
    for file in files:

        try:
            MODULES_IMPORTED[file] = __import__(__pluginImportPrefix__ + file, fromlist = ["*"])
        except:
            MODULES_IMPORTED[file] = __import__(__pluginImportPrefixForService__ + file, fromlist = ["*"])

                
            
def createInstances():
    """
        Method to create plugins instance
    """
    for cls in PARENT_CLASS.__subclasses__():
        MODULES_IMPORTED[cls.__name__]
        class_ = getattr(MODULES_IMPORTED[cls.__name__], cls.__name__)
        instance = class_()
        MODULES_INSTANCES.append(instance)
        xbmc.log("[ STREAMING SOURCE MODULE ] Load module %s" % (cls.__name__), xbmc.LOGINFO)

def getStreaminSource(sourceId):
    """
        Method to get the specific module from its id
        
        @param moduleId: the id of the module
    """
    for inst in MODULES_INSTANCES:
        if str(inst.getId()) == str(sourceId):
            return inst
        
    return PARENT_CLASS()

def getMoreMovieLink(sourceId, streamItem,strictlyEgal=False): 
    """
        Method to get more link for a movie
        @param sourceId: the current sourceId
        @param streamItem: a stream item
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70004),"","0/" + str(len(MODULES_INSTANCES)))
    
    elementList = []
    # ___ Loop on each instance of sources
    for inst in MODULES_INSTANCES:
        # ___ If the instance is equal to our main sourceId
        if str(inst.getId()) == str(sourceId):  
            percent = int( ( 1 / len(MODULES_INSTANCES) ) * 100)  
            progress.update( percent, str(constant.__addon__.getLocalizedString(70005))+inst.getName(), "1/" + str(len(MODULES_INSTANCES)))
            
            # ___ Search the movie in the current source
            searchMovies = inst.searchMovie(streamItem.getTitle())
            for movie in searchMovies:
                # ___ When the movie is found
                if movie.getTitle() == streamItem.getTitle():
                    # ___ Get the list
                    elementList = inst.getMovieLink(movie)
            break
        
    newElementList = [] 
    nbInst = 1
    for inst in MODULES_INSTANCES:
        # ___ If the instance is not equal to our main sourceId
        if str(inst.getId()) != str(sourceId) and inst.isActivated():           
            isFound = False
            nbInst = nbInst+1
            percent = int((100*nbInst) / len(MODULES_INSTANCES))  
            progress.update( percent, str(constant.__addon__.getLocalizedString(70005))+inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
            
            # ___ Search the movie in the current source
            searchMovies = inst.searchMovie(streamItem.getTitle())
            if searchMovies is not None and len(searchMovies) > 0:
                for movie in searchMovies:
                    # ___ When the movie is found                   
                    if isEquals(movie.getTitle(),streamItem.getTitle()):
                        isFound = True
                        # ___ Get links
                        newElementList = inst.getMovieLink(movie)   
                        # ___ Add link to the list
                        if newElementList is not None and len(newElementList) > 0:
                            for element in newElementList:
                                elementList = appendLinkInList(element, elementList)  
                                         
                # ___ If not found, search approximatly 
                if not isFound and not strictlyEgal:
                    
                    for movie in searchMovies:

                        # ___ When the movie is found                   
                        if SM(None, movie.getTitle(), streamItem.getTitle()).ratio() > 0.5:                            
                            # ___ Get links
                            newElementList = inst.getMovieLink(movie)   
                            # ___ Add link to the list
                            if newElementList is not None and len(newElementList) > 0:
                                for element in newElementList:
                                    elementList = appendLinkInList(element, elementList)     
                    """
                    movie = searchMovies[0]
                    # ___ Get links of the first element
                    newElementList = inst.getMovieLink(movie)   
                    # ___ Add link to the list
                    if newElementList is not None and len(newElementList) > 0:
                        for element in newElementList:
                            elementList = appendLinkInList(element, elementList)   
                    """
    progress.close()
    return elementList 


def getMoreTvShowEpisodeLink(sourceId, streamItem): 
    """
        Method to get more link for a tvshow episode
        @param sourceId: the current sourceId
        @param streamItem: a stream item
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70004),"","0/" + str(len(MODULES_INSTANCES)))
    
    
    elementList = []
    # ___ Loop on each instance of sources
    for inst in MODULES_INSTANCES:
        # ___ If the instance is equal to our main sourceId
        if str(inst.getId()) == str(sourceId):  
            percent = int( ( 1 / len(MODULES_INSTANCES) ) * 100)  
            progress.update( percent, str(constant.__addon__.getLocalizedString(70005))+inst.getName(), "1/" + str(len(MODULES_INSTANCES)))
           
            # ___ Search the tvshow in the current source
            searchTvShows = inst.searchTvShow(streamItem.getTvShowName())
            for tvShow in searchTvShows:
                # ___ When the tvshow is found
                if tvShow.getTvShowName() == streamItem.getTvShowName():
                    
                    # ___ Search seasons
                    searchSeasons = inst.getTvShowSeasons(tvShow)
                    
                    if searchSeasons is not None and len(searchSeasons) > 0:
                        for season in searchSeasons:
                            # ___ When the season is found
                            if season.getSeason() == streamItem.getSeason():
                                # ___ Search episode
                                searchEpisodes = inst.getTvShowEpisodes(season)
                                
                                if searchEpisodes is not None and len(searchEpisodes) > 0:
                                    for episode in searchEpisodes:
                                        # ___ When the episode is found
                                        if episode.getEpisodes() is not None and len(episode.getEpisodes()) > 0 and  streamItem.getEpisodes() is not None and len(streamItem.getEpisodes()) > 0 and episode.getEpisodes()[0] == streamItem.getEpisodes()[0]:
                                
                                            elementList = inst.getTvShowEpisodeLink(episode)
                                            break                                
                                break
                    break
            break
        
    newElementList = [] 
    nbInst = 1
    
    for inst in MODULES_INSTANCES:
        # ___ If the instance is not equal to our main sourceId
        if str(inst.getId()) != str(sourceId) and inst.isActivated():
            nbInst = nbInst+1
            percent = int((100*nbInst) / len(MODULES_INSTANCES))  
            progress.update( percent, str(constant.__addon__.getLocalizedString(70005))+inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
            
            # ___ Search the tvshow in the current source
            searchTvShows = inst.searchTvShow(streamItem.getTvShowName())
            
            if searchTvShows is not None and len(searchTvShows)>0:
                for tvShow in searchTvShows:
                    # ___ When the tvshow is found
                    if tvShow.getTvShowName() == streamItem.getTvShowName():
                        
                        # ___ Search seasons
                        searchSeasons = inst.getTvShowSeasons(tvShow)
                        
                        if searchSeasons is not None and len(searchSeasons) > 0:
                            for season in searchSeasons:
                                # ___ When the season is found
                                if season.getSeason() == streamItem.getSeason():
                                    # ___ Search episode
                                    searchEpisodes = inst.getTvShowEpisodes(season)
                                    
                                    if searchEpisodes is not None and len(searchEpisodes) > 0:
                                        for episode in searchEpisodes:
                                            # ___ When the episode is found
                                            if episode.getEpisodes() is not None and len(episode.getEpisodes()) > 0 and  streamItem.getEpisodes() is not None and len(streamItem.getEpisodes()) > 0 and episode.getEpisodes()[0] == streamItem.getEpisodes()[0]:
                                    
                                                newElementList = inst.getTvShowEpisodeLink(episode)
                                                # ___ Add link to the list
                                                if newElementList is not None and len(newElementList) > 0:
                                                    for element in newElementList:
                                                        elementList = appendLinkInList(element, elementList)   
                                                break                                
                                    break
                        break
                
    
    progress.close()
    
    return elementList

def getMoreAnimeEpisodeLink(sourceId, streamItem): 
    """
        Method to get more link for a tvshow episode
        @param sourceId: the current sourceId
        @param streamItem: a stream item
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70004),"","0/" + str(len(MODULES_INSTANCES)))
    
    
    elementList = []
    # ___ Loop on each instance of sources
    for inst in MODULES_INSTANCES:
        # ___ If the instance is equal to our main sourceId
        if str(inst.getId()) == str(sourceId):  
            percent = int( ( 1 / len(MODULES_INSTANCES) ) * 100)  
            progress.update( percent,str(constant.__addon__.getLocalizedString(70005))+ inst.getName(), "1/" + str(len(MODULES_INSTANCES)))
           
            # ___ Search the tvshow in the current source
            searchTvShows = inst.searchAnime(streamItem.getTvShowName())
            for tvShow in searchTvShows:
                # ___ When the tvshow is found
                if tvShow.getTvShowName() == streamItem.getTvShowName():
                    
                    # ___ Search seasons
                    searchSeasons = inst.getAnimeSeasons(tvShow)
                    
                    if searchSeasons is not None and len(searchSeasons) > 0:
                        for season in searchSeasons:
                            # ___ When the season is found
                            if season.getSeason() == streamItem.getSeason():
                                # ___ Search episode
                                searchEpisodes = inst.getAnimeEpisodes(season)
                                
                                if searchEpisodes is not None and len(searchEpisodes) > 0:
                                    for episode in searchEpisodes:
                                        # ___ When the episode is found
                                        if episode.getEpisodes() is not None and len(episode.getEpisodes()) > 0 and  streamItem.getEpisodes() is not None and len(streamItem.getEpisodes()) > 0 and episode.getEpisodes()[0] == streamItem.getEpisodes()[0]:
                                    
                                            elementList = inst.getAnimeEpisodeLink(episode)
                                            break                                
                                break
                    break
            break
        
    newElementList = [] 
    nbInst = 1
    
    for inst in MODULES_INSTANCES:
        # ___ If the instance is not equal to our main sourceId
        if str(inst.getId()) != str(sourceId) and inst.isActivated():
            nbInst = nbInst+1
            percent = int((100*nbInst) / len(MODULES_INSTANCES))  
            progress.update( percent, str(constant.__addon__.getLocalizedString(70005))+inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
            
            # ___ Search the tvshow in the current source
            searchTvShows = inst.searchAnime(streamItem.getTvShowName())
            
            if searchTvShows is not None and len(searchTvShows)>0:
                for tvShow in searchTvShows:
                    # ___ When the tvshow is found
                    if tvShow.getTvShowName() == streamItem.getTvShowName():
                        
                        # ___ Search seasons
                        searchSeasons = inst.getAnimeSeasons(tvShow)
                        
                        if searchSeasons is not None and len(searchSeasons) > 0:
                            for season in searchSeasons:
                                # ___ When the season is found
                                if season.getSeason() == streamItem.getSeason():
                                    # ___ Search episode
                                    searchEpisodes = inst.getAnimeEpisodes(season)
                                    
                                    if searchEpisodes is not None and len(searchEpisodes) > 0:
                                        for episode in searchEpisodes:
                                            # ___ When the episode is found
                                            if episode.getEpisode() == streamItem.getEpisode():
                                    
                                                newElementList = inst.getAnimeEpisodeLink(episode)
                                                # ___ Add link to the list
                                                if newElementList is not None and len(newElementList) > 0:
                                                    for element in newElementList:
                                                        elementList = appendLinkInList(element, elementList)   
                                                break                                
                                    break
                        break
                
    progress.close()
    
    return elementList 

def searchMovie(title):
    """
        Method to search movie on all source
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70006),"","0/" + str(len(MODULES_INSTANCES)))
    
    elementList = []
    nbInst = 0
    for inst in MODULES_INSTANCES:
        nbInst = nbInst+1
        percent = int( ( nbInst * 100) / len(MODULES_INSTANCES) )  
        progress.update( percent,str(constant.__addon__.getLocalizedString(70006))+ inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
           
        sourceElList = inst.searchMovie(title)
        if sourceElList is not None and len(sourceElList)>0:
            for el in sourceElList:
                el.setSourceId(inst.getId())
                appendElementInList(el,elementList)
                
    progress.close()
    
    # ___ Sort the list
    startTime=timeit.default_timer()
    elementList = sorted(elementList,key = lambda streamItem: streamItem.__compare__(title), reverse = True )
    endTime=timeit.default_timer()
    xbmc.log("Global search - Sort list in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    return elementList

def searchTvShow(title):
    """
        Method to search tvshow on all source
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70006),"","0/" + str(len(MODULES_INSTANCES)))
    
    elementList = []
    nbInst = 0
    for inst in MODULES_INSTANCES:
        nbInst = nbInst+1
        percent = int( ( nbInst* 100)  / len(MODULES_INSTANCES) ) 
        progress.update( percent,str(constant.__addon__.getLocalizedString(70006))+ inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
           
        sourceElList = inst.searchTvShow(title)
        if sourceElList is not None and len(sourceElList)>0:
            for el in sourceElList:
                el.setSourceId(inst.getId())
                appendElementInList(el,elementList)
                
    progress.close()
    
    # ___ Sort the list
    startTime=timeit.default_timer()
    elementList = sorted(elementList,key = lambda streamItem: streamItem.__compare__(title), reverse = True )
    endTime=timeit.default_timer()
    xbmc.log("Global search - Sort list in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    return elementList   
    
def searchAnime(title):
    """
        Method to search anime on all source
    """
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70006),"","0/" + str(len(MODULES_INSTANCES)))
    
    elementList = []
    nbInst = 0
    for inst in MODULES_INSTANCES:
        nbInst = nbInst+1
        percent = int( ( nbInst * 100) / len(MODULES_INSTANCES) )
        progress.update( percent,str(constant.__addon__.getLocalizedString(70006))+ inst.getName(), str(nbInst) + "/" + str(len(MODULES_INSTANCES)))
           
        sourceElList = inst.searchAnime(title)
        if sourceElList is not None and len(sourceElList)>0:
            for el in sourceElList:
                el.setSourceId(inst.getId())
                appendElementInList(el,elementList)
                
    progress.close()
    
    # ___ Sort the list
    startTime=timeit.default_timer()
    elementList = sorted(elementList,key = lambda streamItem: streamItem.__compare__(title), reverse = True )
    endTime=timeit.default_timer()
    xbmc.log("Global search - Sort list in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    return elementList
   
def getMoreLinks(sourceId, streamItem,strictlyEgal=False):
    """
        Method to get more links from other sources
    """
    
    elementList = []
    
    # ___ Case of MOVIE
    if streamItem.getType() == StreamItem.TYPE_MOVIE:
        elementList = getMoreMovieLink(sourceId, streamItem,strictlyEgal) 
    if streamItem.getType() == StreamItem.TYPE_TVSHOW_EPISODE:
        elementList = getMoreTvShowEpisodeLink(sourceId, streamItem) 
    if streamItem.getType() == StreamItem.TYPE_ANIME_EPISODE:
        elementList = getMoreAnimeEpisodeLink(sourceId, streamItem) 
           
    return elementList

def isEquals(str1,str2):
    
    str1 = strUtil.remove_special_char(str1)
    str1 = strUtil.deleteAccent(str1)
    
    str2 = strUtil.remove_special_char(str2)
    str2 = strUtil.deleteAccent(str2)
    
    return str1.upper() == str2.upper()
    
def appendElementInList(streamItem,elementList):
        """
            Method to append a element in a list if the title is not already in the list
            @param streamItem : the StreaItem to add
            @param elementList: the list to append
        """
        for el in elementList:
            # ___ If the title is in the list, return the list as it is.
            if isEquals(streamItem.getTitle(), el.getTitle()):
                return elementList 
        # ___ Else add the element       
        elementList.append(streamItem)
        return elementList     

def appendLinkInList(streamItem,elementList):
        """
            Method to append a link in a list if the link is not already in the list
            @param streamItem : the StreaItem to add
            @param elementList: the list to append
        """
        for el in elementList:
            # ___ If the link is in the list, return the list as it is.
            if el.getPlayableUrl() == streamItem.getPlayableUrl():
                return elementList 
        # ___ Else add the link       
        elementList.append(streamItem)
        return elementList 
    
def getSourcesXmlSettings():
    """
        Method to get settings for each source
    """
    settingsTxt = ''
    for inst in MODULES_INSTANCES:
        settingsTxt += inst.getSettingsXml()
        
    return settingsTxt

loadModules()
createInstances()