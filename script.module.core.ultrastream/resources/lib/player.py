# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 December 2016

@author: Seko
@summary: Player functions

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import xbmcgui
import xbmcplugin
import sys
import time
import miscFunctions
import urlresolver
import webUtil
import constant
import history
from unshortenurl import UnshortenUrl
from item import StreamItem

# ____________________     V A R I A B L E S     ____________________



# ____________________     F U N C T I O N S       ____________________
def displayVideoOptions(streamItem):
    """
        Method to display video options
        @param streamItem: the selected StreamItem   
    """
    
    constant.__LOGGER__.log("Try to resolve url "+streamItem.getHref(),xbmc.LOGDEBUG)
    
    # ___ Try to unshort link
    unshort = UnshortenUrl()
    href = unshort.unshortUrl(streamItem.getHref())
    constant.__LOGGER__.log('Unshort url : '+str(href))
    streamItem.setHref(href)
    
    # ___ Resolve url
    playableUrl = False
    progress = xbmcgui.DialogProgress()
    progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70009))
    try:
        playableUrl = urlresolver.resolve(streamItem.getHref())
    except:
        pass
    progress.close()
    constant.__LOGGER__.log("Resolved url : "+str(playableUrl),xbmc.LOGDEBUG) 
    
    # ___If the url is resolved, play automatically if the setting is activated  
    if playableUrl != False  and isinstance(playableUrl,unicode) and constant.__addon__.getSetting('play_auto') == 'true':
        streamItem.setPlayableUrl(playableUrl)
        playVideo(streamItem)
        
    # ___If the url is resolved, display the the list of possibilities (Open in web browser, Play, Download or Download & Play )    
    elif playableUrl != False  and isinstance(playableUrl,unicode) and constant.__addon__.getSetting('play_auto') == 'false':
        
        streamItem.setPlayableUrl(playableUrl)
        if constant.__addon__.getSetting('downloader_module') == '0' and constant.__addon__.getSetting('activate_web_browser') == 'false':
            # ___ Do not display download choice if the downloader is not set.
            liste = [constant.__addon__.getLocalizedString(70001)]            
        elif constant.__addon__.getSetting('downloader_module') == '0' and constant.__addon__.getSetting('activate_web_browser') == 'true':
            # ___ Do not display download choice if the downloader is not set.
            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70002)]
        
        elif constant.__addon__.getSetting('downloader_module') != '0' and constant.__addon__.getSetting('activate_web_browser') == 'false':
            # ___ Do not display download choice if the downloader is not set.
            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70003)]      
        else:
            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70002),constant.__addon__.getLocalizedString(70003)]
        
        selectDialog = xbmcgui.Dialog()
        select = selectDialog.select(constant.__addon__.getLocalizedString(70000), liste)
        if select == 0:
            playVideo(streamItem) 
        elif select == 1 and constant.__addon__.getSetting('activate_web_browser') == 'true':        
            isRealDebrid = False
            
            # ___ If we use real-debrid, build the streaming page : 
            # ___     https://real-debrid.com/streaming-<MEDIA ID FOR REALDEBRID>
            if 'rdb.so' in str(playableUrl) or 'rdeb.io' in str(playableUrl):
                urlToPlay = "https://real-debrid.com/streaming-"+playableUrl.split("/")[4]                
                streamItem.setPlayableUrl(playableUrl)
                isRealDebrid = True
            
            # ___  For real-debrid we use firefox    
            if isRealDebrid:
                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('rd_web_browser'))   
            else:
                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('android_web_browser'))         
            
            # ___ Create or update the history
            history.createOrUpdateHistory(streamItem)
        
        elif select == 1 and constant.__addon__.getSetting('activate_web_browser') == 'false':   
            miscFunctions.downloadFile(streamItem, False)                              
        elif select == 2:
            miscFunctions.downloadFile(streamItem, False)                              
          
        
    # __ Else display limited options        
    elif constant.__addon__.getSetting('activate_web_browser') == 'true': 
        constant.__LOGGER__.log("Unable to resolve url "+streamItem.getHref(),xbmc.LOGWARNING)        
        
        # ___ Only display the option : Open in web browser
        liste = [constant.__addon__.getLocalizedString(70002)]            
            
        selectDialog = xbmcgui.Dialog()
        select = selectDialog.select(constant.__addon__.getLocalizedString(70000), liste)
        if select == 0:
            # ___ Open in web browser                
            isRealDebrid = False
            
            # ___ If we use real-debrid, build the streaming page : 
            # ___     https://real-debrid.com/streaming-<MEDIA ID FOR REALDEBRID>
            if 'rdb.so' in str(playableUrl) or 'rdeb.io' in str(playableUrl):
                urlToPlay = "https://real-debrid.com/streaming-"+playableUrl.split("/")[4]
                isRealDebrid = True
                streamItem.setPlayableUrl(urlToPlay)
            
            # ___  For real-debrid we use the selected web browser in settings -- Only for Android    
            if isRealDebrid:
                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('rd_web_browser'))   
            else:
                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('android_web_browser'))         
            
            # ___ Create or update the history     
            history.createOrUpdateHistory(streamItem)
            
    # __ Else display notification for unavailable link
    else:
        miscFunctions.displayNotification(constant.__addon__.getLocalizedString(70014),'info') 
        
def playVideo(streamItem):
    """
        Method to play a video
        @param streamItem: the streamItem to play        
    """
    constant.__LOGGER__.log('Play url : '+streamItem.getPlayableUrl(),xbmc.LOGDEBUG)       
    
    # ___ Boolean uses for seeking
    seekBool = False
    
    # ___ Get the history of the element
    historyEl = history.getHistory(streamItem)  
    constant.__LOGGER__.log(historyEl)
    if historyEl is not None:
        
        # If the percent is between 0 and 99, ask to resume the video
        if int(historyEl['percent']) >0 and int(historyEl['percent']) <99:
            dialog = xbmcgui.Dialog()
            seekBool = dialog.yesno(constant.__addon__.getLocalizedString(70001), constant.__addon__.getLocalizedString(33059))
            
    
    # ___ Open the movie with KODI Player
    player = xbmc.Player()
    player.play(streamItem.getPlayableUrl())        
    
    # ___ Waiting to play the movie
    videotimewatched = 0
    isComplete = 0
    percent = 0
    
    # ___ Wait until the player is playing
    while not player.isPlaying() :
        time.sleep(0.1) 
        
    # ___ While the movie is playing
    if player.isPlaying() :
        # ___ Get the total time
        videototaltime = player.getTotalTime()
        
        # ___ Wait until the timer progress
        currentTime = player.getTime()
        while player.isPlaying() and player.getTime() <= currentTime:
            time.sleep(0.1)
        
        # ___ ! Now the movie is started
        
        # ___ Seek time if necessary
        if seekBool and historyEl is not None:
            player.seekTime(float(historyEl['seektime']))
            
               
        # ___ While the movie is watched
        while player.isPlaying() :
            
            # ___ Get the current time
            videotimewatched = player.getTime()
            
            if videototaltime == 0:
                # ____Get the total time
                videototaltime = player.getTotalTime() 
            # ___ Sleep 500ms
            time.sleep(0.5)
    
   
    # ___ Verify if the movie is ended    
    if videotimewatched is not None and videototaltime is not None and videotimewatched >= videototaltime:
        isComplete = 1
    else:
        isComplete = 0
        
    # ___ Calculate the percent of video watched
    if videotimewatched is not None and videototaltime is not None and videototaltime > 0:
        percent = float( ( videotimewatched * 100 ) / videototaltime )
    else:
        percent = 0
                
    # ___ Create or update the history       
    history.createOrUpdateHistory(streamItem,videotimewatched,percent,isComplete)

    
def playStrm(listItems):
    """
        Method to play a .strm file
        @param streamItem : the StreamItem get from the .strm file
    """
    
    # ___ Display links choice
    dialog = xbmcgui.Dialog()
    listStr = []
    for index in range(0,len(listItems)):
        item = listItems[index]
        item.regenerateKodiTitle()
        listStr.append(item.getKodiTitle())
    result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
    
    # ___ Until the link is not resolved, we display the links choice dialog
    error = False
    while result > -1 or error: 
        result = -1
        error = False
        # ___ Resolve url
        playableUrl = False
        progress = xbmcgui.DialogProgress()
        progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70009))
        try:
            # ___ Try to unshort link
            unshort = UnshortenUrl()
            href = unshort.unshortUrl(listItems[result].getHref())
            playableUrl = urlresolver.resolve(href)
        except:
            # ___ If the url is not resolved, display link choice again.
            error = True   
            listItems[result].setKOLinkStatus()
            listItems[result].regenerateKodiTitle()
            listStr[result] = listItems[result].getKodiTitle()
            result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
            
        progress.close()
        constant.__LOGGER__.log("Resolved url : "+str(playableUrl),xbmc.LOGDEBUG) 
        
        # ___If the url is resolved, display the the list of possibilities (Open in web browser, Play, Download or Download & Play )
        if not error:
            if playableUrl != False  and isinstance(playableUrl,unicode) :        
                
                item = xbmcgui.ListItem(path=playableUrl)
                xbmcplugin.setResolvedUrl(int(sys.argv[ 1 ]),True,item)
            
            else:
                # ___ If the url is not resolved, display link choice again.            
                error = True   
                listItems[result].setKOLinkStatus()
                listItems[result].regenerateKodiTitle()
                listStr[result] = listItems[result].getKodiTitle()
                result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
                 

def displayLinksInDialog(listItems):
    """
        Method to display a dialog with all link
        @param listItems :  all StreamItem links
    """
    
    # ___ Display links choice
    dialog = xbmcgui.Dialog()
    listStr = []
    for index in range(0,len(listItems)):
        item = listItems[index]
        item.regenerateKodiTitle()
        listStr.append(item.getKodiTitle())
        
    result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
    
    # ___ Until the link is not resolved, we display the links choice dialog
    if result > -1:
        error = True
    while error: 
               
        error = False
        if int(listItems[result].getAction()) == StreamItem.ACTION_MORE_LINKS :
            import src_mod as sources
            listItems = sources.getMoreLinks(constant.__addon__.getSetting('default_stream_src'), listItems[result])
            for item in listItems:
                item.setMetadata(listItems[result].getMetadata())    
            
            listStr = []    
            for index in range(0,len(listItems)):
                item = listItems[index]
                item.regenerateKodiTitle()
                listStr.append(item.getKodiTitle())
                
            result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
            error = True
       
        else:
            # ___ Resolve url
            playableUrl = False
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70009))
            try:     
                # ___ Try to unshort link
                unshort = UnshortenUrl()
                href = unshort.unshortUrl(listItems[result].getHref())
                playableUrl = urlresolver.resolve(href)
            except:
                # ___ If the url is not resolved, display link choice again.
                error = True   
                listItems[result].setKOLinkStatus()
                listItems[result].regenerateKodiTitle()
                listStr[result] = listItems[result].getKodiTitle()
                result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
                
            progress.close()
            constant.__LOGGER__.log("Resolved url : "+str(playableUrl),xbmc.LOGDEBUG) 
            
            # ___If the url is resolved, display the the list of possibilities (Open in web browser, Play, Download or Download & Play )
            if not error:
                if playableUrl != False  and isinstance(playableUrl,unicode) :        
                    
                    streamItem = listItems[result]
                    
                    # ___If the url is resolved, play automatically if the setting is activated  
                    if constant.__addon__.getSetting('play_auto') == 'true':
                        streamItem.setPlayableUrl(playableUrl)
                        playVideo(streamItem)
                        
                    # ___If the url is resolved, display the the list of possibilities (Open in web browser, Play, Download or Download & Play )    
                    elif constant.__addon__.getSetting('play_auto') == 'false':
                        
                        streamItem.setPlayableUrl(playableUrl)
                        if constant.__addon__.getSetting('downloader_module') == '0' and constant.__addon__.getSetting('activate_web_browser') == 'false':
                            # ___ Do not display download choice if the downloader is not set.
                            liste = [constant.__addon__.getLocalizedString(70001)]            
                        elif constant.__addon__.getSetting('downloader_module') == '0' and constant.__addon__.getSetting('activate_web_browser') == 'true':
                            # ___ Do not display download choice if the downloader is not set.
                            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70002)]
                        
                        elif constant.__addon__.getSetting('downloader_module') != '0' and constant.__addon__.getSetting('activate_web_browser') == 'false':
                            # ___ Do not display download choice if the downloader is not set.
                            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70003)]      
                        else:
                            liste = [constant.__addon__.getLocalizedString(70001),constant.__addon__.getLocalizedString(70002),constant.__addon__.getLocalizedString(70003)]
                        
                        selectDialog = xbmcgui.Dialog()
                        select = selectDialog.select(constant.__addon__.getLocalizedString(70000), liste)
                        if select == 0:
                            playVideo(streamItem) 
                        elif select == 1 and constant.__addon__.getSetting('activate_web_browser') == 'true':        
                            isRealDebrid = False
                            
                            # ___ If we use real-debrid, build the streaming page : 
                            # ___     https://real-debrid.com/streaming-<MEDIA ID FOR REALDEBRID>
                            if 'rdb.so' in str(playableUrl) or 'rdeb.io' in str(playableUrl):
                                urlToPlay = "https://real-debrid.com/streaming-"+playableUrl.split("/")[4]                
                                streamItem.setPlayableUrl(playableUrl)
                                isRealDebrid = True
                            
                            # ___  For real-debrid we use firefox    
                            if isRealDebrid:
                                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('rd_web_browser'))   
                            else:
                                webUtil.openInWebbrowser(streamItem.getPlayableUrl(),constant.__addon__.getSetting('android_web_browser'))         
                            
                            # ___ Create or update the history
                            history.createOrUpdateHistory(streamItem)
                        
                        elif select == 1 and constant.__addon__.getSetting('activate_web_browser') == 'false':   
                            miscFunctions.downloadFile(streamItem, False)                              
                        elif select == 2:
                            miscFunctions.downloadFile(streamItem, False)
                
                else:
                    # ___ If the url is not resolved, display link choice again.            
                    error = True   
                    listItems[result].setKOLinkStatus()
                    listItems[result].regenerateKodiTitle()
                    listStr[result] = listItems[result].getKodiTitle()
                    result = dialog.select(constant.__addon__.getLocalizedString(70013), listStr)
                
        if result == -1:
            error=False