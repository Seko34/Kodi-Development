# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 14 Fev 2017

@author: Seko
@summary: Cached functions

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import timeit
import kodiUtil
from item import StreamItem
from logger import Logger

# ____________________     V A R I A B L E S     ____________________

# __ Init addon variable & Logger
__LOGGER__ = Logger('UltraStream_Cached')

try:
   import StorageServer
except:
   import storageserverdummy as StorageServer

# __ Init the cache variable
__CACHE__ = StorageServer.StorageServer("ultrastream", 24) 

# ___ Init cached key
KEY_URL_PARAM ="urlParams"
KEY_STREAMITEM_LIST ="streamItemList"
KEY_CURRENT_LVL ="lastLevel"
 
# ____________________     F U N C T I O N S       ____________________

def cachePage(urlParams,listStreamItems):
    """
        Method to cache a page as the last page
        @param listStreamItems: the list of StreaItem to display
        @param urlParams: the url parameters to retrieve the last page
        
    """
    startTime=timeit.default_timer()
    # ___ Get the current level and add 1
    level = getCurrentLvl() + 1
    
    # ___ Save url parameters in cache
    __CACHE__.set(KEY_URL_PARAM+str(level),repr(urlParams))
    
    # ___ Transform list of StreamItem in array of JSON
    arrayItems = []
    if listStreamItems is not None and len(listStreamItems) > 0:
        for item in listStreamItems:
            arrayItems.append(item.getJsonItem())
            
    # ___ Save JSON array in cache
    __CACHE__.set(KEY_STREAMITEM_LIST+str(level),repr(arrayItems))
    
    # ___ Increment the current level
    __CACHE__.set(KEY_CURRENT_LVL,str(level))
    endTime=timeit.default_timer()
    __LOGGER__.log("Cached page with level : "+str(level)+" in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)

def getCurrentLvl():
    """
        Method to get the current level
        @return an integer
    """
    lvlStr = __CACHE__.get(KEY_CURRENT_LVL)
    if lvlStr is not None and len(lvlStr)>0:
        __LOGGER__.log("Current level is "+lvlStr,xbmc.LOGDEBUG) 
        return int(lvlStr)
    else:
        __CACHE__.set(KEY_CURRENT_LVL,str(0))
        __LOGGER__.log("Current level is 0",xbmc.LOGDEBUG)
        return 0

def isCachedPage(urlParams):
    """
        Method to know if the requested page is the cached page
        @param urlParams: the url parameters to retrieve the last page
        @return True if the requested page is the cached page, else return false
    """
    __LOGGER__.log("Url params is: "+str(urlParams),xbmc.LOGDEBUG)
    # ___ Get the current level minus one
    level = getCurrentLvl() - 1
    
    # ___ Get cached params values
    if __CACHE__.get(KEY_URL_PARAM+str(level)) is not None and len(__CACHE__.get(KEY_URL_PARAM+str(level))) > 0:
        paramsCached = eval(__CACHE__.get(KEY_URL_PARAM+str(level)))
        __LOGGER__.log("Get cached params : "+str(paramsCached),xbmc.LOGDEBUG)   
        # ___ If not None, compare with url params
        if paramsCached is not None:
            if cmp (paramsCached,urlParams)==0 :
                __LOGGER__.log("Params is same as cached params",xbmc.LOGDEBUG)   
                return True
        
    return False

def getPreviousCachedPage():
    """
        Method to retrieve the cached page
        @return the list of StreamItem cached
    """
    startTime=timeit.default_timer()
    # ___ Get the current level minus one
    level = getCurrentLvl() - 1
    
    listStreamItems = []
    # ___ Get array of JSON from cache
    arrayItems = eval(__CACHE__.get(KEY_STREAMITEM_LIST+str(level)))
    # ___ Transform the JSON array to StreamItem array
    if arrayItems is not None and len(arrayItems) > 0:
        for item in arrayItems:
            listStreamItems.append(StreamItem(params=item))
            
    # ___ Then remove the two last cached page
    __CACHE__.delete(KEY_STREAMITEM_LIST+str(level+1))    
    __CACHE__.delete(KEY_URL_PARAM+str(level+1))
    __CACHE__.delete(KEY_STREAMITEM_LIST+str(level))    
    __CACHE__.delete(KEY_URL_PARAM+str(level))    
    __CACHE__.set(KEY_CURRENT_LVL,str(level-1))
    __LOGGER__.log("New level is : "+str(level),xbmc.LOGDEBUG)
    endTime=timeit.default_timer()
    __LOGGER__.log("Get previous cached page in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    # ___ Return a StreamItem array
    return listStreamItems

def getCachedPage():
    """
        Method to retrieve the cached page
        @return the list of StreamItem cached
    """
    
    startTime=timeit.default_timer()
    # ___ Get the current level
    level = getCurrentLvl()
    
    listStreamItems = []
    # ___ Get array of JSON from cache
    arrayItems = eval(__CACHE__.get(KEY_STREAMITEM_LIST+str(level)))
    # ___ Transform the JSON array to StreamItem array
    if arrayItems is not None and len(arrayItems) > 0:
        for item in arrayItems:
            listStreamItems.append(StreamItem(params=item))
            
    # ___ Then remove the last cached page
    __CACHE__.delete(KEY_STREAMITEM_LIST+str(level))    
    __CACHE__.delete(KEY_URL_PARAM+str(level))    
    __CACHE__.set(KEY_CURRENT_LVL,str(level-1))
    
    endTime=timeit.default_timer()
    __LOGGER__.log("Get last cached page in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    # ___ Return a StreamItem array
    return listStreamItems

def getCachedParams():
    """
        Method to retrieve the cached page
        @return the list of StreamItem cached
    """
    
    startTime=timeit.default_timer()
    # ___ Get the current level
    level = getCurrentLvl()

    # ___ Get the current params
    params = eval(__CACHE__.get(KEY_URL_PARAM+str(level)))
      
    endTime=timeit.default_timer()
    __LOGGER__.log("Get last cached params in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    
    # ___ Return a StreamItem array
    return params

def getParentUrl():
    """
        Method to get the parent url
        @return the parent url
    """
    startTime=timeit.default_timer()
    # ___ Get the current level
    level = getCurrentLvl()

    # ___ Get the current params
    params = eval(__CACHE__.get(KEY_URL_PARAM+str(level)))
      
    endTime=timeit.default_timer()
    __LOGGER__.log("Get last url in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
    return kodiUtil.build_url(params)

def clearCache():
    """
        Method to clear the cache
    """
    startTime=timeit.default_timer()
    __CACHE__.delete("%")
    endTime=timeit.default_timer()
    __LOGGER__.log("Clear cache in "+str(endTime-startTime)+" sec",xbmc.LOGDEBUG)
