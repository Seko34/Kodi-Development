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
import historyModule
import constant

from item import StreamItem
# ____________________     V A R I A B L E S     ____________________


# __ Init history module
historyMod = historyModule.getHistoryModule(constant.__addon__.getSetting('historyModule'))
historyMod.initModule('plugin.video.seko.ultrastream', 'ultrastream')

# ____________________     C O N S T A N T S       ____________________


# ____________________     M E T H O D S       ____________________
def getHistory(streamItem):
    """
       Method to get the history for the streamItem 
       @param streamItem: the streamItem to play     
       @return the history element 
       resultJSON = { 
                   'name':result[0][0],
                   'url':result[0][1],
                   'seektime':result[0][2],
                   'percent':result[0][3],
                   'isComplete':result[0][4],
                   'tvshow':result[0][5],
                   'season':result[0][6],
                   'episode':result[0][7]
                }
    """
    historyElement = None
    
    if streamItem.isEpisode():
        historyElement = historyMod.findHistory(streamItem.getDbTitle(), tvshow=streamItem.getDbTvShowName(), season=streamItem.getSeason(), episode=streamItem.getEpisode())
    else:
        historyElement = historyMod.findHistory(streamItem.getDbTitle() )
    
    return historyElement
    
def createOrUpdateHistory(streamItem, videotimewatched=0,percent=0,isComplete=0):
    """
       Method t create or update a history entry for the streamItem 
       @param streamItem: the streamItem to play
    """
    # ___ Create or update the history
    if streamItem.isEpisode():
        constant.__LOGGER__.log('Insert History for episode',xbmc.LOGDEBUG);
        historyMod.updateHistory(streamItem.getDbTitle(), streamItem.getHref(), videotimewatched, percent, isComplete, tvshow=streamItem.getDbTvShowName(), season=streamItem.getSeason(), episode=streamItem.getEpisode())
    else:
        constant.__LOGGER__.log('Insert History for movie',xbmc.LOGDEBUG);
        historyMod.updateHistory(streamItem.getDbTitle(), streamItem.getHref(), videotimewatched, percent, isComplete)
        