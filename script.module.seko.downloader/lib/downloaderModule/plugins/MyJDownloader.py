# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 29 Dec. 2015
@author: Seko
@summary: JDownloader

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import util
import xbmc
import xbmcgui
import xbmcaddon
from downloaderModule.pluginDownloaderTpl import downloaderTemplate 
import downloaderModule.myjdapi as myjdapi
    
"""
    MyJDownloader  Class
"""
class MyJDownloader(downloaderTemplate):
    
    # ___ HEADER CONFIGURATION FOR HTML REQUEST
    HEADER_CFG = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
    
    def __init__(self):
        """
            Constructor
        """        
        self.ID = 4
        # ___ MyJDwonloader variable
        self.__MyJD = False
        self.__MyJDConnnection = False
    
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
                 'webBrowserId': '<the web browser id>', 
                 'myjd_mail': <myjd_mail>,
                 'myjd_pwd': <jd myjd_pwd>,
                 'myjd_device': <myjd_device>
                 }
            @param async: Boolean which indicates if the download should be start in an other thread
        """
        
        self.__addon__ = xbmcaddon.Addon(id='script.module.seko.downloader')  
        
        isConnected = self._getMyJDConnection(params['myjd_mail'], params['myjd_pwd'])
        
        # ___ Check if we are connected and if the device is started
        if isConnected and self._checkDeviceConnection(params['myjd_device']) == True:
            
            # ___ Add the link to MyJDownloader device
            self.__MyJD.getDevice(name=params['myjd_device']).linkgrabber.addLinks([{"autostart" : False, 
                                                               "links" : params['url'],
                                                               "packageName" : params['title'] }])
            
            self._showMessage("MyJDownloader", self.__addon__.getLocalizedString(33270))
    
        else:
            # Display error message
            self._showDialog( self.__addon__.getLocalizedString(33268), self.__addon__.getLocalizedString(33269))
    
        # ___ If we are connected, disconnect the connection
        if self.__MyJDConnnection == True:
            self.__MyJD.disconnect()
            
        """  
        jd =  myjdapi.myjdapi()
        isConnected = jd.connect(params['myjd_mail'], params['myjd_pwd'])
        if isConnected:
            jd.getDevices()
            myDevice = jd.getDevice(name=params['myjd_device'])
            if myDevice != False:
                myDevice.linkgrabber.addLinks([{"autostart" : False, 
                                                               "links" : params['url'],
                                                               "packageName" : params['title'] }])
                self._showMessage("MyJDownloader", self.__addon__.getLocalizedString(33270))
            else: 
                # Display error message
                self._showDialog( self.__addon__.getLocalizedString(33268), self.__addon__.getLocalizedString(33269))
                
            jd.disconnect()    
        else:
            # Display error message
            self._showDialog( self.__addon__.getLocalizedString(33268), self.__addon__.getLocalizedString(33269)) 
        """      
    def _checkDeviceConnection(self,deviceName):
        """
            Method to check the connection with the jd device
            @param deviceName: the device name in MyJDownloader
        """
        xbmc.log("Check the connection with MyJDownloader and device "+deviceName, xbmc.LOGDEBUG)
        # ___ 'getDevices' method is mandatory before using 'getDevice' method
        self.__MyJD.getDevices()
        if self.__MyJD.getDevice(name=deviceName) != False:    
            return True
                    
        return False
    
    def _getMyJDConnection(self,jdmail,jdpwd):
        """
            Method to get a MyJDownloader connection
            @param jdmail: the email for MyJDownloader
            @param jdpwd: the password for MyJDownloader
        """        
        if not self.__MyJD:
            self.__MyJD = myjdapi.myjdapi()
            self.__MyJDConnnection = self.__MyJD.connect(jdmail,jdpwd)
            
        return self.__MyJDConnnection
    
    def _showMessage(self, heading, message):
        """
            Method to show a notification
            @param heading : the heading text
            @param message : the message of the notification            
        """
        xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % (heading, message.encode("utf-8"), 2000)).encode("utf-8"))
   
    def _showDialog(self, heading, message): 
        """
            Method to show a "ok" dialog window
            @param heading : the heading text
            @param message : the message of the dialog window            
        """       
        dialog = xbmcgui.Dialog()
        dialog.ok(heading, message)
        
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