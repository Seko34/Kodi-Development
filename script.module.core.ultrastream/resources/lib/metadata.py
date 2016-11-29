# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 24 November 2016

@author: Seko
@summary: Metadata lib

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________

import xbmc
import history
import scraperModule as Scrapers
import constant as constant

from item import StreamItem
from logger import Logger

# ____________________     V A R I A B L E S     ____________________

# __ Init addon variable & Logger
__LOGGER__ = Logger('UltraStream')

# ____________________     C O N S T A N T S       ____________________


# ____________________     M E T H O D S       ____________________
def getMetadataForList(type,listItems,dialogProgress=False,useAsService=False):
    """
        Method to get metadatas of a list
        
        @param type : the type of elements in the list
        @param listItems : the list to updated
        
        @return the list updated
    """  
    """
    @todo: Modify scrapper to use StreamItem type ?
    TYPE_MOVIE = 0
    TYPE_SERIE = 1
    TYPE_ANIME = 2
    TYPE_MOVIE_HD = 3
    
    TYPE_SERIE_DETAILS = 11  
    TYPE_ANIME_DETAILS = 12
    """
    if listItems[0].getType() != StreamItem.TYPE_PAGE:
        type = int(listItems[0].getType())
            
    if type == StreamItem.TYPE_MOVIE or type == StreamItem.TYPE_SHOW or type == StreamItem.TYPE_DOCUMENTARY:
        scraperType = 0
    elif type == StreamItem.TYPE_TVSHOW:
        scraperType = 1    
    elif type == StreamItem.TYPE_ANIME:
        scraperType = 2    
    elif type == StreamItem.TYPE_MOVIE_HD:
        scraperType = 3 
    elif type == StreamItem.TYPE_TVSHOW_EPISODE or type == StreamItem.TYPE_TVSHOW_SEASON:
        scraperType = 11    
    elif type == StreamItem.TYPE_ANIME_EPISODE or type == StreamItem.TYPE_ANIME_SEASON:
        scraperType = 12
    else:
        scraperType = -1
        
    __LOGGER__.log('Scraper type = '+str(scraperType),xbmc.LOGDEBUG)
    
    
    # ___ Transform list of streamitem in list of json
    listJSON = []    
    for item in listItems:
        listJSON.append(item.getJsonItem())
        
    # ___ If we want all synopsis/informations from scraper, we start all threads for it    
    # ___     Case 1 : getdetails settings is superior to 0
    # ___     Case 2 : We display a link list
    
    if ( int(constant.__addon__.getSetting('getdetails')) > 0  or int(listItems[0].getAction()) == StreamItem.ACTION_PLAY) and scraperType > -1:    
        if useAsService:
            listJSON = Scrapers.getMetadatas(constant.__addon__.getSetting('getdetails'),scraperType,listJSON)
        else:
            listJSON = Scrapers.getMetadatas(constant.__addon__.getSetting('getdetails'),scraperType,listJSON,int(constant.__addon__.getSetting("nbthread")),dialogProgress)
    
    # ___ Transform list of json in list of streamitem
    listStreamItems = []
    for item in listJSON:
        listStreamItems.append(StreamItem(item['title'],item))
        
    # ___ Update all elements with history if necessary
    for elementList in listStreamItems:        
        historyElement = history.getHistory(elementList)
        if historyElement is not None:
            elementList.setPlayCount(1)
    
    
        
    return listStreamItems

def getMetadata(streamItem,dialogProgress=False,useAsService=False):
    """
        Method to get metadata of a streamItem only
        
        @param streamItem : the StreamItem to updated
        @param dialogProgress : the  dialog to display the progress
        @param useAsService : boolean to indicate if we user the method in the service
        
        @return the StreamItem updated
    """  
    """
    @todo: Modify scrapper to use StreamItem type ?
    TYPE_MOVIE = 0
    TYPE_SERIE = 1
    TYPE_ANIME = 2
    TYPE_MOVIE_HD = 3
    
    TYPE_SERIE_DETAILS = 11  
    TYPE_ANIME_DETAILS = 12
    """
    type = -1
    if streamItem.getType() != StreamItem.TYPE_PAGE:
        type = int(streamItem.getType())
            
    if type == StreamItem.TYPE_MOVIE or type == StreamItem.TYPE_SHOW or type == StreamItem.TYPE_DOCUMENTARY:
        scraperType = 0
    elif type == StreamItem.TYPE_TVSHOW:
        scraperType = 1    
    elif type == StreamItem.TYPE_ANIME:
        scraperType = 2    
    elif type == StreamItem.TYPE_MOVIE_HD:
        scraperType = 3 
    elif type == StreamItem.TYPE_TVSHOW_EPISODE or type == StreamItem.TYPE_TVSHOW_SEASON:
        scraperType = 11    
    elif type == StreamItem.TYPE_ANIME_EPISODE or type == StreamItem.TYPE_ANIME_SEASON:
        scraperType = 12
    else:
        scraperType = -1
        
    __LOGGER__.log('Scraper type = '+str(scraperType),xbmc.LOGDEBUG)
    
    
    # ___ Transform list of streamitem in list of json
    listJSON = []    
    listJSON.append(streamItem.getJsonItem())
        
    # ___ If we want all synopsis/informations from scraper, we start all threads for it    
    # ___     Case 1 : getdetails settings is superior to 0
    # ___     Case 2 : We display a link list
    
    if ( int(constant.__addon__.getSetting('getdetails')) > 0  or int(streamItem.getAction()) == StreamItem.ACTION_PLAY) and scraperType > -1:    
        if useAsService:
            listJSON = Scrapers.getMetadatas(constant.__addon__.getSetting('getdetails'),scraperType,listJSON)
        else:
            listJSON = Scrapers.getMetadatas(constant.__addon__.getSetting('getdetails'),scraperType,listJSON,int(constant.__addon__.getSetting("nbthread")),dialogProgress)
    
    # ___ Transform json in streamitem
    streamItem = StreamItem(listJSON[0]['title'],listJSON[0])
    
    # ___ Update all elements with history if necessary
    historyElement = history.getHistory(streamItem)
                
    if historyElement is not None:
        streamItem.setPlayCount(1)
        
    return streamItem      