# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
    Created on 20 sept. 2014
    
    @author: Seko
    @summary: Common Library
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import xbmcaddon

# ____________________     V A R I A B L E S     ____________________
settings = xbmcaddon.Addon(id='script.module.seko.common')
language = settings.getLocalizedString
version = "0.0.9"
plugin = "SekoCommon-" + version

