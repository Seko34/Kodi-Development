# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 Fev 2017

@author: Seko
@summary: Functions to get icon
constant.__coreAddonDir__+'/resources/media/films_hd.png
'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________

import constant
import os

# ____________________     V A R I A B L E S     ____________________


def getIcon(title,hd=False):
    """
        Method to get the icon depends on the language and on the settings
        @param the icon title
        @return the icon path
    """    
    # ___ Get the selected theme
    theme = constant.__addon__.getSetting('theme')
    if theme == None or len(str(theme)) ==0 or not isinstance(theme,str):
        theme = '0'
        
    if hd:
        return  os.path.join(constant.__ICONDIR__,theme,title+'_hd.png')
   
    return  os.path.join(constant.__ICONDIR__,theme,title+'.png')