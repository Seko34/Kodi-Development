# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 09 September 2016

@author: Seko
@summary: Addon constant

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________

import xbmcaddon
import xbmc
import os
import sys
from logger import Logger

# ____________________     C O N S T A N T S       ____________________

# ___ Addon variable
__addon__    = xbmcaddon.Addon(id='plugin.video.seko.ultrastream')
__addonDir__ = xbmc.translatePath( __addon__.getAddonInfo('path') )

# ___ Core module variable
__coreAddon__ = xbmcaddon.Addon(id='script.module.core.ultrastream')
__coreAddonDir__ = xbmc.translatePath( __coreAddon__.getAddonInfo('path') )


# ___ Logger
__LOGGER__ = Logger('UltraStream')

# ___ Language
__LANG__ = xbmc.getInfoLabel('System.Language')

# Get the kodi major version
if not sys.argv[0].endswith('test.py'):
    __kodiVersion__ =xbmc.getInfoLabel('System.BuildVersion')[0:2]
else:
    __kodiVersion__ = '17'

if not sys.argv[0].endswith('test.py'):
    # ___ Directory
    __MEDIADIR__ = os.path.join( __coreAddonDir__, 'resources', 'media')
    
    defaultIconLang = 'en'
    if __LANG__ == 'French':
        defaultIconLang = 'fr'
    __ICONDIR__ = os.path.join( __MEDIADIR__, 'icons',defaultIconLang)
else:
    __MEDIADIR__ = 'test'
    __LANG__ = 'fr'
    __ICONDIR__ = 'test'