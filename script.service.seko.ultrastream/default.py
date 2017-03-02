# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
    Created on 20 sept. 2014
    
    @author: Seko
    @summary: UltraStream Service
'''
#---------------------------------------------------------------------

# ____________________      CHECK  ULTRASTREAM      ____________________


import xbmc

# ___ Unzip last archive from package 
# ___     (Fix for windows bug)

if not xbmc.getCondVisibility('System.HasAddon(%s)' % 'plugin.video.seko.ultrastream'):
    import fnmatch, os
    import glob,os
    lastFile = max(glob.iglob(xbmc.translatePath('special://home')+'/addons/packages/plugin.video.seko.ultrastream-*.zip'), key=os.path.getctime)
   
    if lastFile is not None:
        try:
            xbmc.executebuiltin('Extract('+lastFile+','+xbmc.translatePath('special://home')+'addons/)')
            xbmc.executebuiltin('UpdateLocalAddons')
            xbmc.executebuiltin('InstallAddon(plugin.video.seko.ultrastream)')
        except e:
            print e
        

# ___ Launch service if ultrastream is installed
if xbmc.getCondVisibility('System.HasAddon(%s)' % 'plugin.video.seko.ultrastream'):
    # ____________________        I M P O R T        ____________________
    import xbmcaddon
    import xbmc    
    import services
    import os
    import logger
    import miscFunctions
    import src_mod as sources
    import constant
    import threading
    
    # ____________________     V A R I A B L E S     ____________________
        
    settings = xbmcaddon.Addon(id='plugin.video.seko.ultrastream')
    
    version = "0.1.3"
    plugin = "Ultrastream Service-" + version
    __LOGGER__ = logger.Logger('UltraStream-Service')
    __LOGGER__.log(plugin)
    
        
    
    # Get the current source
    __SOURCE__ = sources.getStreaminSource(constant.__addon__.getSetting('default_stream_src'))
    
    # Create or update settings file
    miscFunctions.writeSettingsFile(sources.getSourcesXmlSettings(),__SOURCE__.getServiceSettingValue())
    
    # Set the default directory for movie
    if constant.__addon__.getSetting('service_movie_dir') == 'false':
        movieDir = os.path.join( constant.__addonDir__, 'strm', 'movies')
        constant.__addon__.setSetting('service_movie_dir',movieDir)
        
    # Set the default directory for tvshow
    if constant.__addon__.getSetting('service_tvshow_dir') == 'false':
        movieDir = os.path.join( constant.__addonDir__, 'strm', 'tvshows')
        constant.__addon__.setSetting('service_tvshow_dir',movieDir)
        
    # Launch service in an other thread if it is activated 
    if constant.__addon__.getSetting('activate_service') == 'true':
    
        __LOGGER__.log('UltraStream Service launched')
        t = threading.Thread(target = services.launchServices )
        t.start()
         
     