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

# ____________________     C O N S T A N T S       ____________________


__addon__    = xbmcaddon.Addon(id='plugin.video.seko.ultrastream')
__addonDir__ = xbmc.translatePath( __addon__.getAddonInfo('path') )

__coreAddon__ = xbmcaddon.Addon(id='script.module.core.ultrastream')
__coreAddonDir__ = xbmc.translatePath( __coreAddon__.getAddonInfo('path') )