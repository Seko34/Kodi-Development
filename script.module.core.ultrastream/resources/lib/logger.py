# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 24 Jan 2016

@author: Seko
@summary: Logger

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc

# ____________________     C L A S S       ____________________
class Logger:
    
    __ADDON_NAME__ = None
       
    __MODULE_NAME__ =  None
    
    def __init__(self, addonName=None, moduleName=None):
        """
            Constructor
            @param addonName: The addon name
            @param moduleName: The module name            
        """        
        if addonName:
            self.__ADDON_NAME__  = addonName
        if moduleName:
            self.__MODULE_NAME__ = moduleName
            
    def _getPrefixMsg(self):
        """
            Method to get the prefix log message
        """
        prefix = ""
        if self.__ADDON_NAME__ or self.__MODULE_NAME__:
            prefix +="["
            
        if self.__ADDON_NAME__    :            
            prefix +=""+self.__ADDON_NAME__
            
        if self.__ADDON_NAME__ and self.__MODULE_NAME__:  
            prefix +=" - "
              
        if self.__MODULE_NAME__    :            
            prefix +=self.__MODULE_NAME__    
            
        if self.__ADDON_NAME__ or self.__MODULE_NAME__:
            prefix +="] "
        
        return prefix
            
    def log(self,msg,level=None):
        """
            Log function
        """
        #newMsg = strUtil.toUTF8(msg)
        
        if level is not None:
            xbmc.log(self._getPrefixMsg()+str(msg), level)
        else:            
            xbmc.log(self._getPrefixMsg()+str(msg))
        
        
        
    