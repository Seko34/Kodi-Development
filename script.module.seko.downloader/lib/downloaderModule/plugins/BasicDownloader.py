# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 07 Nov. 2015

@author: Seko
@summary: Basic downloader

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import os.path
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import urllib
import time

from downloaderModule.pluginDownloaderTpl import downloaderTemplate 

    
"""
    BasicDownloader  Class
"""
class BasicDownloader(downloaderTemplate):
    
    def __init__(self):
        """
            Constructor
        """        
        self.ID = 1
    
    def clearAll(self):
        pass

    class CancelDownloadException(Exception):
        pass  
    
    def download(self,fileName, params, async=False):
        """
            Download method
            @param fileName: the name of the file to download
            @param params: the dictionnary with informations about the file to download
                 The minimum format is : 
                 {
                 'url':'<the url to download the file>',
                 'title':'<Title of the movie>',
                 'destinationFolder':'<Title of the movie>'
                 }
            @param async: Boolean which indicates if the download should be start in an other thread
        """
        
        dp = xbmcgui.DialogProgress()
        dp.create("Basic Downloader","Downloading file",params['title'])
        dest = params['destinationFolder']+"/"+fileName
        url=params['url']
        urllib.urlretrieve(url,dest,lambda nb, bs, fs, url1=url : self._pbhook(nb,bs,fs,url1,dp))
    
    
    def _pbhook(self, numblocks, blocksize, filesize, url ,dp=None):
        """
            Method to display a progress bar
        """
        global start_time
        if numblocks == 0:
            start_time = time.time()
            
            return
        
        try:
            duration = time.time() - start_time
                        
            # ___ Speed in KBytes/s
            speed = int((numblocks*blocksize) / (1024 * duration))   
            
            # ___ Percent
            percent = min((numblocks*blocksize*100)/filesize, 100)  
            
            xbmc.log('Percent : '+str(percent)+" - "+'Speed : '+str(speed),xbmc.LOGINFO)
            # ___ Update the dialg progres
            dp.update(percent, line3='Percent : '+str(percent)+" - "+'Speed : '+str(speed)+" Kb/s")   
            
            #xbmc.log(__addon__.getLocalizedString(33054)+str(percent)+" - "+__addon__.getLocalizedString(33055)+str(speed),xbmc.LOGINFO)
            #dp.update(percent, line3=__addon__.getLocalizedString(33055)+str(speed)+" Kb/s")       
            
        except:
            percent = 100
            dp.update(percent)
        
        if dp.iscanceled(): 
            xbmc.log("DOWNLOAD CANCELLED",xbmc.LOGWARNING)
            dp.close()        
            
    
    def _startDownload(self):
        pass
    
    def _stopDownload(self):
        pass
    
    def _pauseDownload(self):
        pass
    
    def _resumeDownload(self):
        pass
    
    def _getQueue(self):
        pass 
    
    def _addToQueue(self,fileName, params, async=True):
        pass 
    
    def _removeToQueue(self,fileName, params, async=True):
        pass 

    def _clearQueue(self):
        pass 
    
    def _isStarted(self):
        pass