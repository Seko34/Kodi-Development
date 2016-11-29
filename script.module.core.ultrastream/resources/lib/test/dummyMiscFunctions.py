# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 24 Jan 2016

@author: Seko
@summary: Miscellaneous functions

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import os
import kodiUtil
import constant
from item import StreamItem
from logger import Logger

# ____________________     V A R I A B L E S     ____________________

# __ Init addon variable & Logger
__LOGGER__ = Logger('UltraStream')

# ____________________     F U N C T I O N S       ____________________
def displayVideoOptions(streamItem):
    """
        Method to display video options
        @param streamItem: the selected StreamItem   
    """
    pass
        
        
def playVideo(streamItem):
    """
        Method to play a video
        @param streamItem: the streamItem to play        
    """
    pass
    
def playStrm(listItems):
    """
        Method to play a .strm file
        @param streamItem : the StreamItem get from the .strm file
    """
    
    pass


def downloadFile(streamItem,playAtEnd):
    """
        Method to download a file
        @param streamItem : the streamItem
    """
    pass

def displayStreamItem(listStreamItems):
    """
        Method to display a list of StreamItem
    """
    kodiUtil.beginContentDirectory()
    
    if listStreamItems is not None and len(listStreamItems) > 0:
        for item in listStreamItems:
            item.addListItemToDirectory()
    
    kodiUtil.endOfDirectory()
    
def displayNotification(message):
    """
        Method to display a notification
        @param message : the message to display
    """
    xbmc.executebuiltin('Notification(\'UltraStream\','+message+',3000,error)')                       
    __LOGGER__.log(message, xbmc.LOGINFO)


def readSettingsTemplate():
    """
        Method to read the settings template
    """
    templateFilePath = os.path.join( constant.__addonDir__, 'resources', 'settings_tpl.xml')                      
    templateFile = open(templateFilePath,'r')
    result = templateFile.read()

    return result

def writeSettingsFile(settingsTxt,serviceSettingsTxt):
    """
        Method to write the settings file
    """
    settingsFilePath = os.path.join( constant.__addonDir__, 'resources', 'settings.xml')                      
    
    xmlTxt = readSettingsTemplate()
    #xmlTxt += sources.getSourcesXmlSettings()
    xmlTxt += serviceSettingsTxt
    xmlTxt += "    </category>\n      <category label=\"52000\">"
    xmlTxt += settingsTxt
    xmlTxt += "    </category>\n</settings>"
    try:
        with open(settingsFilePath, 'w') as f:
            f.write(xmlTxt)
        __LOGGER__.log("Settings file created/updated.")
    except:
        raise
