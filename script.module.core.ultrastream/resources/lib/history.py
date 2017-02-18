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
        historyMod.updateHistory(streamItem.getDbTitle(), streamItem.getHref(), videotimewatched, percent, isComplete, tvshow=streamItem.getDbTvShowName(), season=streamItem.getSeason(), episode=streamItem.getEpisode())
    else:
        historyMod.updateHistory(streamItem.getDbTitle(), streamItem.getHref(), videotimewatched, percent, isComplete)
        