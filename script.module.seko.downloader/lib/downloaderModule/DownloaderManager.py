#---------------------------------------------------------------------
'''
Created on 27 sept. 2014

@author: Seko
@summary: Downloader GUI Library

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import xbmcaddon
import xbmcgui
import xbmc
import util

# ____________________      V A R I A B L E S     ____________________

__addon__ = xbmcaddon.Addon('script.module.seko.downloader')
__addonDir__ = xbmc.translatePath( __addon__.getAddonInfo('path') )

# ____________________       M E T H O D S        ____________________

    
    
def displayDownloadManager(addon_handle, dlModule):
    """
        Method to display the download manager
        @param addon_handle: the addon handler
        @param downloader: the downloader
    """   
    
    elements = list()    
    # ___ 0 : Start Download
    elements.append(__addon__.getLocalizedString(33203))
    # ___ 1 : Stop Download
    elements.append(__addon__.getLocalizedString(33204))
    # ___ 2 : Show list
    elements.append(__addon__.getLocalizedString(33205))    
    # ___ 3 : Delete element of the list
    elements.append(__addon__.getLocalizedString(33209))
    
    # ____ Display the list of choise
    selectDialog = xbmcgui.Dialog()
    select = selectDialog.select(__addon__.getLocalizedString(33202), elements)
    
    if select == 0:
        # ___ Start download                   
        dlModule._startDownload()      
        
    elif select == 1:
        # ___ Stop download
        dlModule._stopDownload()
        
    elif select == 2:
        # ___ Display the list of element
        displayListDownloadManager(dlModule)        
        displayDownloadManager(addon_handle, dlModule)
        
    elif select == 3:
        # ___ Delete an element of the list
        deleteAnElementOfTheList(dlModule)
        displayDownloadManager(addon_handle, dlModule) 
        
def displayListDownloadManager(downloader):  
    """
        Method to display all elements in the downloader queue
        @param downloaded: the downloader
    """
    # ____ Get all elements in the queue 
    queueDl = downloader.getQueue()
    elements = list()
    elementsTitle = list()   
    listIndex = 0
    if queueDl is not None and len(queueDl) > 0:
        for element in queueDl:       
            elements.append({'index': listIndex, 'mode':'remove_item_from_queue','title':element['title'],'info':element, 'iconImage':'resources/media/remove.png'})
            elementsTitle.append(element['title'])
            listIndex = listIndex + 1
   
        # ____ Display the list of choise
        selectDialog = xbmcgui.Dialog()
        selectDialog.select(__addon__.getLocalizedString(33209), elementsTitle)
    else:
        # ___ If there are any elements in the queue, we inform the user
        msgDialog = xbmcgui.Dialog()
        msgDialog.ok(__addon__.getLocalizedString(33200), __addon__.getLocalizedString(33211)) 
    
def deleteAnElementOfTheList(downloader):   
    """
        Method to delete an element in the downloader queue
        @param downloaded: the downloader
    """
    queueDl = downloader.getQueue()
    
    # ____ Get all elements in the queue
    elements = list()
    elementsTitle = list()   
    listIndex = 0
    if queueDl is not None and len(queueDl) > 0:
        for element in queueDl:       
            elements.append({'index': listIndex, 'mode':'remove_item_from_queue','title':element['title'],'info':element, 'iconImage':'resources/media/remove.png'})
            elementsTitle.append(element['title'])
            listIndex = listIndex + 1
   
        # ____ Display the list of choise
        selectDialog = xbmcgui.Dialog()
        select = selectDialog.select(__addon__.getLocalizedString(33210), elementsTitle)
        
        if select >=0 :
            downloader.__queue__._removeToQueue(elements[select]['info']['fileName'])
            deleteAnElementOfTheList(downloader)
        
    else:
        # ___ If there are any elements in the queue, we inform the user
        msgDialog = xbmcgui.Dialog()
        msgDialog.ok(__addon__.getLocalizedString(33200), __addon__.getLocalizedString(33211)) 
    
    
    
    