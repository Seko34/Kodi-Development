# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 07 Nov. 2015

@author: Seko
@summary: WebBrowser Downloader

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import util

from downloaderModule.pluginDownloaderTpl import downloaderTemplate 

    
"""
    AdvancedDownloader  Class
"""
class WebBrowserDownloader(downloaderTemplate):
    
    def __init__(self):
        """
            Constructor
        """        
        self.ID = 3
    
    def clearAll(self):
        pass
  
    
    def download(self,fileName, params, async=False):
        """
            Download method
            @param filename: the name of the file to download
            @param params: the dictionnary with informations about the file to download
                 The minimum format is : 
                 {
                 'url':'<the url to download the file>',
                 'title':'<Title of the movie>',
                 'destinationFolder':'<Title of the movie>',
                 'webBrowserId': '<the web browser id>'
                 }
            @param async: Boolean which indicates if the download should be start in an other thread
        """
        
        util.openInWebbrowser(params['url'],params['webBrowserId'])
    
    
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