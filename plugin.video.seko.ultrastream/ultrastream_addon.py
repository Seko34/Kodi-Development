# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
"""
    Main script for the UltraStream
    Copyright (C) 2014 Seko
    
    Created on 1 sept. 2015
    @author: Seko
    @summary: The main python script of the plugin.video.seko.ultrastream addon
    
"""

# ____________________     I M P O R T     ____________________
import xbmcaddon
import urlparse
import xbmc
import os
import shutil
import sys
import ga
import resources.lib.router as router
import src_mod as sources
import miscFunctions as miscFunctions
import constant as constant
from urlparse import parse_qsl

# ____________________     V A R I A B L E S     ____________________


    # ___ Get base_url, add_handle and arguments
__url__ = sys.argv[0]
    # ___ Get the handle integer
__handle__ = int(sys.argv[1])    
    # ___ Parse a URL-encoded paramstring to the dictionary of
    # ___ {<parameter>: <value>} elements
__params__ = dict(parse_qsl(sys.argv[2][1:]))
args = urlparse.parse_qs(sys.argv[2][1:])

    # Try to copy the tiles for titan skin 
try:
    fileToMove = os.path.join( constant.__coreAddonDir__, 'resources', 'media', 'icon_ultrastream_titan.png')
    __addonTitan__ = xbmcaddon.Addon(id='skin.titan')
    __addonTitanDir__ = xbmc.translatePath( __addonTitan__.getAddonInfo('path') )
    destFile = os.path.join( __addonTitanDir__, 'extras', 'hometiles', 'icon_ultrastream_titan.png')
    shutil.copyfile(fileToMove, destFile)
except Exception, e:
    xbmc.log("Error during copy of png tile for titan skin",xbmc.LOGERROR)
    xbmc.log(str(e),xbmc.LOGERROR)   


    # Create or update settings file
miscFunctions.writeSettingsFile(sources.getSourcesXmlSettings(),sources.getStreaminSource(constant.__addon__.getSetting('default_stream_src')).getServiceSettingValue())

  
    # Set the default directory for movie
if constant.__addon__.getSetting('service_movie_dir') == 'false':
    movieDir = os.path.join( constant.__addonDir__, 'strm', 'movies')
    constant.__addon__.setSetting('service_movie_dir',movieDir)
    
    # Set the default directory for tvshow
if constant.__addon__.getSetting('service_tvshow_dir') == 'false':
    movieDir = os.path.join( constant.__addonDir__, 'strm', 'tvshows')
    constant.__addon__.setSetting('service_tvshow_dir',movieDir)   

        
        
# ____________________     START ADDON SCRIPT     ____________________

# ___ Google Analytics
if constant.__kodiVersion__ >= 17:
    ga.pushData()

# ___ Router
router.router(__params__)

# ____________________     END ADDON SCRIPT     ____________________
