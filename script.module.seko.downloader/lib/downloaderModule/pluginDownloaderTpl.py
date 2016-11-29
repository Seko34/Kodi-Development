# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 23 Aug. 2015

@author: Seko
@summary: Template for downloader plugin class

'''
#---------------------------------------------------------------------


class downloaderTemplate(object):
    
    # ___ The module ID
    ID = -1
    
    
    
    """
        Template class for history module
    """
    def __init__(self):
        pass
    
    def getId(self):
        return self.ID
           
    def clearAll(self):
        pass
    
    def download(self,fileName, params, async=True):
        """
            Download method
            @param filename: the name of the file to download
            @param params: the dictionnary with informations about the file to download
            @param async: Boolean which indicates if the download should be start in an other thread
        """
        pass
        
    
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