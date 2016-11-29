# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
    Init class
    Created on 23 aug. 2015
    
    @author: Seko
    @summary: 
'''
#---------------------------------------------------------------------


# ____________________        I M P O R T        ____________________
import os
import xbmc
import xbmcaddon
from pluginDownloaderTpl import downloaderTemplate as PARENT_CLASS



MODULES_IMPORTED = {}
MODULES_INSTANCES = []

__addon__ = xbmcaddon.Addon(id='script.module.seko.downloader')
__addonDir__ = xbmc.translatePath( __addon__.getAddonInfo('path') )
__pluginPath__ = os.path.join( __addonDir__,'lib','downloaderModule','plugins')
__pluginImportPrefix__ = "downloaderModule.plugins."


def loadModules():
    """
        Method to load all plugin module
    """
    # ___Get plugins files
    lst = os.listdir(__pluginPath__)
    files = []
    
    for f in lst:
        s = __pluginPath__ + os.sep + f
        if os.path.isfile(s) and os.path.exists(s) and f.endswith('.py') and f != '__init__.py':
            files.append(f[0:len(f)-3])
    # ___ Load the modules
    for file in files:
        MODULES_IMPORTED[file] = __import__(__pluginImportPrefix__ + file, fromlist = ["*"])
    
def createInstances():
    """
        Method to create plugins instance
    """
    for cls in PARENT_CLASS.__subclasses__():
        MODULES_IMPORTED[cls.__name__]
        class_ = getattr(MODULES_IMPORTED[cls.__name__], cls.__name__)
        instance = class_()
        MODULES_INSTANCES.append(instance)
        xbmc.log("[ DOWNLOADER MODULE ] Load module %s" % (cls.__name__), xbmc.LOGINFO)

def getDownloadModule(moduleId):
    """
        Method to get the specific module from its id
        
        @param moduleId: the id of the module
    """
    for inst in MODULES_INSTANCES:
        if str(inst.getId()) == str(moduleId):
            return inst
        
    return DownloaderModule()



loadModules()
createInstances()