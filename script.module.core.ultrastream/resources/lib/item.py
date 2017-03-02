# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 02 Jan 2016

@author: Seko
@summary: Item file

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmcgui
import strUtil
import kodiUtil
import os
import xbmc
import json
import ast
import webUtil
import traceback
import constant
import icons
from logger import Logger
from difflib import SequenceMatcher as SM
    
# ____________________     C L A S S       ____________________
class StreamItem:
    
    
    # TYPE 
    TYPE_DEFAULT        = -1
    
    TYPE_MOVIE          = 0
    TYPE_MOVIE_HD       = 1
    TYPE_DOCUMENTARY    = 2    
    TYPE_SHOW           = 3
    
    TYPE_TVSHOW         = 10
    TYPE_TVSHOW_SEASON  = 11  
    TYPE_TVSHOW_EPISODE = 12   
    
    TYPE_ANIME          = 20
    TYPE_ANIME_SEASON   = 21
    TYPE_ANIME_EPISODE  = 22
    
    TYPE_WEBTV          = 30
    
    TYPE_MENU           = 100
    TYPE_PAGE           = 101
    TYPE_STREAMING_LINK = 102
    TYPE_SETTINGS       = 103
    
    
    # ACTION
    ACTION_SERVICE                = 0
        # Default action
    ACTION_DISPLAY_MENU           = 10
        # Search, last element etc...
    ACTION_DISPLAY_TYPE_MENU      = 11
    ACTION_DISPLAY_TYPE_LIST      = 12
        # Alphabetic, Genres etc..
    ACTION_DISPLAY_CATEGORIE_MENU = 13
    ACTION_DISPLAY_CATEGORIE_LIST = 14
    
    ACTION_DISPLAY_SEASONS        = 15
    ACTION_DISPLAY_EPISODES       = 16
    ACTION_DISPLAY_LINKS          = 17
    
    ACTION_PLAY                   = 18
    ACTION_SEARCH                 = 19
    ACTION_PUREVID_ID             = 20
    ACTION_DOWNLOAD               = 21
        
    ACTION_MORE_LINKS             = 22
    ACTION_PLAY_TRAILER           = 23
    
    ACTION_SEARCH_WATAMOVIE       = 24
    ACTION_GLOBAL_SEARCH          = 25
    ACTION_GET_SYNOPSIS           = 26
    
        # Settings
    ACTION_DISPLAY_MENU_SETTINGS        = 50
    ACTION_DISPLAY_URLRESOLVER_SETTINGS = 51
    ACTION_DISPLAY_METAHANDLER_SETTINGS = 52
    ACTION_DISPLAY_SETTINGS             = 53
    
    ACTION_DISPLAY_DOWNLOAD_MANAGER     = 60    
    
    ACTION_TEST = 100
    
    # SUBTYPE
    SUBTYPE_NONE        = 0
    SUBTYPE_ALPHABETICS = 1
    SUBTYPE_LAST        = 2
    SUBTYPE_MOST_VIEW   = 3
    SUBTYPE_TOP_RATE    = 4
    SUBTYPE_TOP_WEEK    = 5
    SUBTYPE_GENRE       = 6
    SUBTYPE_EXCLUE      = 7
    SUBTYPE_LIST        = 8
    
    # LOGGER
    __LOGGER__ = Logger('UltraStream','StreamItem')

    
    def __init__(self, title=None, params=None):
        """
            Constructor
        """
               
        self.Item = {
            'action': self.ACTION_DISPLAY_MENU,
            'type': self.TYPE_DEFAULT,
            'subtype': self.SUBTYPE_NONE,
            'subtype_value':'',
            'page':'',
            'title':'',
            'kodi_title':'',
            'dbTitle':'',
            'tvShow':'',
            'dbTvShow':'',
            'season': -1,
            'episode': '',
            'lang': '',
            'subtitle': '',
            'quality':'',
            'year':'',
            'hostName':'',
            'href':'',
            'playableUrl':'',
            'metadata': '',
            'iconImage':'DefaultMovies.png',
            'isFolder':True,
            'id':'',
            'sourceId':'',
            'strm':'0',
            'linkStatus':''
            }
    
        if title:
            self.setTitle(title)
        
        
        if params:
            
            if 'action' in params:
                self.setAction(params['action'])
            if 'type' in params:
                self.setType(params['type'])
            if 'subtype' in params:
                self.setSubType(params['subtype'])
            if 'subtype_value' in params:
                self.setSubTypeValue(params['subtype_value'])
            if 'title' in params:
                self.setTitle(params['title'])
            if 'tvShow' in params:
                self.setTvShowName(params['tvShow'])
            if 'season' in params:
                self.setSeason(params['season'])
            if 'episode' in params:
                if params['episode']!= '' and not isinstance(params['episode'], str) and len(params['episode']) > 0:                    
                    for ep in params['episode']:
                        self.addEpisode(ep)
                elif params['episode']!= '' and isinstance(params['episode'], str) and len(params['episode']) > 0:
                    if params['episode'].startswith('[') and params['episode'].endswith(']'):
                        episodes = ast.literal_eval(params['episode'])
                    else:
                        episodes = params['episode']
                    if not isinstance(episodes, str) and not isinstance(episodes, int) and len(episodes) > 0:
                        for ep in episodes:
                            self.addEpisode(ep)
                    else:
                        self.setEpisode(params['episode'])
                
            if 'lang' in params:          
                self.setLang(params['lang'])        
            if 'subtitle' in params:  
                self.setSubTitle(params['subtitle'])
            if 'quality' in params:
                self.setQuality(params['quality'])            
            if 'href' in params:
                self.setHref(params['href'])           
            if 'hostName' in params:
                self.setHostname(params['hostName'])      
            if 'playableUrl' in params:
                self.setPlayableUrl(params['playableUrl'])        
            if 'page' in params:
                self.setPage(params['page'])
            if 'iconImage' in params:
                self.setIconImage(params['iconImage'])
            if 'metadata' in params:
                self.setMetadata(params['metadata'])
            if 'isFolder' in params:
                self.Item['isFolder'] = self.isFolder()
            if 'id' in params:
                self.setId(params['id'])
            if 'sourceId' in params:
                self.setSourceId(params['sourceId'])                
            if 'strm' in params:
                self.Item['strm']=params['strm']
            
    def getJsonItem(self):
        """
            Getter for the JSON Item
            @return the JSON item
        """
        return self.Item
    
    def getListItem(self):
        """
            Getter for the JSON Item
            @return the JSON item
        """
        # ___ Generate Kodi Title
        self.regenerateKodiTitle()
        
        # ___ Create the list item with the name, the default iconImage is 'DefaultMovies.png'
        li = xbmcgui.ListItem(self.Item['kodi_title'], iconImage=self.Item['iconImage'])
        
        # ___ If the iconImage value starts with 'resources/media', we use it as icon and thumbail image
        if self.Item['iconImage'].startswith('resources/media'):
            li.setIconImage(xbmc.translatePath(os.path.join(constant.__addonDir__,self.Item['iconImage'])))
            li.setThumbnailImage(xbmc.translatePath(os.path.join(constant.__addonDir__,self.Item['iconImage'])))
        
        # ___ If the dictionnary has the 'metadata' value not null, we used it as video informations
        
        if self.Item['metadata'] != '' and not self.isPage(): 

            # ___ Load metada str in json object or dict in json obect __ Fix in the metadata setter
            meta = self.getMetadata()
            """
            try:            
                if isinstance(self.Item['metadata'],str):
                    meta = json.loads(self.Item['metadata'])
                else:
                    meta = self.Item['metadata']
            except:                
                #traceback.print_exc()
                try:
                    meta = ast.literal_eval(self.Item['metadata'])
                except:
                    #traceback.print_exc()
                    meta = self.Item['metadata']
            """
                
            try:
                li.setInfo("video", meta)
                
                # ___ If 'metadata' has a 'picturepath' parameter, we used it as Thumbnail image and icon image
                if 'picturepath' in meta:
                    try:
                        li.setThumbnailImage(meta['picturepath'])
                    except:
                        pass                    
                    li.setIconImage(meta['picturepath'])
                 
                # ___ If 'metadata' has a 'fanart_image' parameter, we used it as fanart_image
                if 'fanart_image' in meta:
                    li.setProperty('fanart_image',meta['fanart_image'])
                  
                if 'cover_url' in meta:         
                    try:
                        li.setIconImage(meta['cover_url']) 
                    except:
                        pass
                    
                if 'backdrop_url' in meta:
                    try:
                        li.setProperty('fanart_image',meta['backdrop_url'])
                    except:
                        pass
                    
            except:
                traceback.print_exc()
                self.__LOGGER__.log('Error during setting property of listItem',xbmc.LOGERROR)
                
        # ___ If the item is  movie
        if (self.getType() == self.TYPE_MOVIE or self.getType() == self.TYPE_MOVIE_HD) and self.getAction() == self.ACTION_DISPLAY_LINKS:
            li.addContextMenuItems([ (constant.__addon__.getLocalizedString(70012).title(), 'RunPlugin(plugin://plugin.video.seko.ultrastream/?action=23&title='+self.getTitle()+')'),
                                    (constant.__addon__.getLocalizedString(70008).title(), 'Container.Update(plugin://plugin.video.seko.ultrastream/?action=26&type=-1&title='+self.getTitle()+')')])
            
        
             
        # ___ If the item is a page, we set the page thumbnail and page icon.
        if self.isPage():
            li.setThumbnailImage(icons.getIcon('nextpage'))
            li.setIconImage(icons.getIcon('nextpage'))
    
        return li
    
    def addListItemToDirectory(self):
        """
            Method to add the item to the current directory
        """
        self.__LOGGER__.log('Add item to directory :',xbmc.LOGDEBUG)
        self.__LOGGER__.log(str(self.Item),xbmc.LOGDEBUG)
        kodiUtil.addDirectoryItem(kodiUtil.build_url(self.Item),
                                self.getListItem(),
                                self.isFolder())
        
    def getAddonUrl(self):
        """
            Method to get the addon url associated to the StreamItem
        """
        addonurl = kodiUtil.build_url(self.Item)
        if addonurl.startswith('plugin://plugin.video.seko.ultrastream/'):
            return addonurl
        else:
            return 'plugin://plugin.video.seko.ultrastream/'+addonurl
    
    def setTitle(self,title):
        """
            Setter for the title
        """
        
        self.Item['title'] = title #strUtil.unescapeHtml(title) #strUtil.normalize(title)
        self.Item['dbTitle'] = strUtil.deleteAccent(strUtil.remove_special_char(self.Item['title']))
        
        self.regenerateKodiTitle()
    
    def regenerateKodiTitle(self):
        """
            Method to regenerate Kodi Title
        """
        
        if int(self.getAction()) == StreamItem.ACTION_MORE_LINKS:
            self.Item['kodi_title'] = constant.__addon__.getLocalizedString(70004)
            return
        
        if int(self.getType()) == self.TYPE_STREAMING_LINK:
            self.Item['kodi_title'] = "[B]"+self.Item['title']+"[/B]"
        else:
            self.Item['kodi_title'] = self.Item['title']
            
        if self.Item['quality'] is not None and self.Item['quality'] != '' and self.Item['quality'] != 'None':
            self.Item['kodi_title'] += " [COLOR green]["+self.Item['quality']+"][/COLOR]"
        
        if self.Item['lang'] is not None and self.Item['subtitle'] is not None and self.Item['lang'] != '' and self.Item['subtitle'] != '' and self.Item['subtitle'] != 'None' and self.Item['lang'] != 'None':
            self.Item['kodi_title'] += " [COLOR blue]["+self.Item['lang']+"ST"+self.Item['subtitle']+"][/COLOR]"        
        
        elif self.Item['lang'] is not None and self.Item['lang'] != '' and self.Item['lang'] != 'None':
            self.Item['kodi_title'] += " [COLOR blue]["+self.Item['lang']+"][/COLOR]"
        
        elif self.Item['subtitle'] is not None and self.Item['subtitle'] != '' and self.Item['subtitle'] != 'None':
            self.Item['kodi_title'] += " [COLOR blue][ST"+self.Item['subtitle']+"][/COLOR]"    
        
        if self.Item['year'] is not None and self.Item['year'] != '' and self.Item['year'] != 'None':
            self.Item['kodi_title'] += " ["+str(self.Item['year'])+"]"
            
        if self.Item['hostName'] is not None and self.Item['hostName'] != '' and self.Item['hostName'] != 'None':
            self.Item['kodi_title'] += " [I]["+str(self.Item['hostName'])+"][/I]"
        
        if self.getType() == self.TYPE_STREAMING_LINK and self.Item['linkStatus'] is not None and self.Item['linkStatus'] != '' and self.Item['linkStatus'] != 'None':
            self.Item['kodi_title'] += " [COLOR red]["+self.Item['linkStatus']+"][/COLOR]"
        
        self.Item['kodi_title'] = self.Item['kodi_title']
            
    def getTitle(self):
        """
            Getter for the title
        """
        return self.Item['title']
    
    def getKodiTitle(self):
        """
            Getter for the kodi title
        """
        return self.Item['kodi_title'] 
     
    def getDbTitle(self):
        """
            Getter for the db title
        """
        return self.Item['dbTitle'] 
          
    def determineSeasonTitle(self):
        """
            Method to set the title from the tvShow and the season
        """
        try:
            if int(self.Item['season']) > 0 and int(self.Item['season']) < 10:
                self.Item['title'] = self.Item['tvShow']+" - S0"+str(self.Item['season'])
            elif int(self.Item['season']) > 0 and int(self.Item['season']) >= 10:
                self.Item['title'] = self.Item['tvShow']+" - S"+str(self.Item['season'])
            else:
                self.Item['title'] = self.Item['tvShow']  
        except :
            self.Item['title'] = self.Item['tvShow']       
        
        self.Item['dbTitle'] = strUtil.remove_special_char(self.Item['title'])
               
    def determineEpisodeTitle(self):
        """
            Method to set the title from the tvShow,the season and episode
        """
        try:
            
            initTitle = self.getTitle()
            self.determineSeasonTitle()
            title = self.getTitle()
            
            
            title = title+' '
                
            # __ For each episode, concatenate with the title
            for index in range (0,len(self.getEpisodes())):
                episode = self.getEpisodes()[index]
                
                # __ Add '0' if the episode is inferior than 10
                if int(episode) > 0 and int(episode) < 10:
                    if index ==0:
                        title = title+"E0"+str(episode)
                    else:                            
                        title = title+"-0"+str(episode)
                elif int(episode) >= 10:
                    
                    if index ==0:
                        title = title+"E"+str(episode)
                    else:                            
                        title = title+"-"+str(episode)
                
                else:
                    title = title + " - "+initTitle    
                 
        except :
            title = title + " - " +initTitle   
        
        self.setTitle(title)
    
    def setTvShowName(self,tvshow):
        """
            Setter for the tvshow
        """
        self.Item['tvShow'] = tvshow 
        self.Item['dbTvShow'] = strUtil.remove_special_char(self.Item['tvShow'])
    
    def getTvShowName(self):
        """
            Getter for the tvshow
        """
        return self.Item['tvShow']
    
    def getDbTvShowName(self):
        """
            Getter for the db tvshow name
        """
        return self.Item['dbTvShow']
    
    def setSeason(self,season):
        """
            Setter for the season
            @note: Accept only integer
        """
        try:
            self.Item['season'] = int(season)
            #self.determineSeasonTitle()
        except:
            self.Item['season'] = ''
    
    def getSeason(self):
        """
            Getter for the season
            @note: Return only integer or -1
        """
        season = -1
        try:
            season = int(self.Item['season'])
        except:
            pass
        return season
        
    def setEpisode(self,episode):
        """
            Setter for the episode
            @param episode: the episode's number
            @note: Add integer only
        """
        try:
            epInt = int(episode)
            self.Item['episode'] = []
            self.Item['episode'].append(epInt)
            #self.determineEpisodeTitle()
        except:
            self.Item['episode'] = ''
            
    def addEpisode(self,episode):
        """
            Method to add an episode to the item
        """
        if self.Item['episode'] == '':
            # __ Add the first episode
            self.setEpisode(episode)
        else:
            # __ Else append episode if it's an integer
            try:
                self.Item['episode'].append(int(episode))
                #self.determineEpisodeTitle()
            except:
                pass
    
    def getEpisodes(self):
        """
            Getter for the Episode
            @note: return an Array if there are episode number, else return ''
        """
        return self.Item['episode']  
    
    
    def getEpisode(self):
        """
            Getter for the Episode
            @note: return an Array if there are episode number, else return ''
        """
        if isinstance(self.Item['episode'], str):
            return self.Item['episode']
        else:
            return self.Item['episode'][0]
    
    def isEpisode(self):
        """
            Method to know if the item is an episode
            @return True if the item is an episode, else return false
        """
        if self.Item['type'] == self.TYPE_ANIME_EPISODE or self.Item['type'] == self.TYPE_TVSHOW_EPISODE :
            return True
        else:
            return False
        
    def isSeason(self):
        """
            Method to know if the item is an season
            @return True if the item is an episode, else return false
        """
        if self.Item['type'] == self.TYPE_ANIME_SEASON or self.Item['type'] == self.TYPE_TVSHOW_SEASON :
            return True
        else:
            return False
        
    def setHref(self,href):
        """
            Setter for the href
            @note: In case of streaming link, set also the PlayableUrl
        """
        self.Item['href'] = href
        
        if int(self.Item['type']) == self.TYPE_STREAMING_LINK:
            self.setPlayableUrl(href)
            hostName = strUtil.getHostname(href)
            if hostName is not None:  
                self.Item['hostName'] = hostName
    
    def getHref(self):
        """
            Getter for the href
        """
        return self.Item['href']
    
    def getHostname(self):
        """
            Getter for the hostName
        """
        return self.Item['hostName']
    
    def setHostname(self,hostName):
        """
            Setter for the hostName
            @param hostName: the hostname
        """
        self.Item['hostName'] = hostName
    
    def setPlayableUrl(self,playableUrl):
        """
            Setter for the playable url
        """
        self.Item['playableUrl'] = playableUrl        
    
    def getPlayableUrl(self):
        """
            Getter for the playable url
        """
        return self.Item['playableUrl'] 
    
    
    def setAction(self,action):
        """
            Setter for the action
        """
        self.Item['action'] = int(action)

    def getAction(self):
        """
            Getter for the action
        """
        return self.Item['action']   
     
    def getType(self):
        """
            Getter for the type
        """
        return int(self.Item['type'])
               
    def setType(self,type):
        """
            Setter for the type
        """
        self.Item['type'] = int(type)          
        
    def setSubType(self,subtype):
        """
            Setter for the subtype
        """
        self.Item['subtype'] = int(subtype)
        
    def getSubType(self):
        """
            Getter for the subtype
        """
        return int(self.Item['subtype'])
        
    def setLang(self,lang):
        """
            Setter for the lang
        """
        self.Item['lang'] = lang   
        
    def getLang(self):
        """
            Getter for the lang
        """
        return self.Item['lang'] 
         
        
    def setSubTitle(self,subtitle):
        """
            Setter for the subtitle
        """
        self.Item['subtitle'] = subtitle  
             
        
    def getSubTitle(self):
        """
            Setter for the subtitle
        """
        return self.Item['subtitle']
                
    def setQuality(self,quality):
        """
            Setter for the quality
        """
        self.Item['quality'] = quality       
           
    def getQuality(self,):
        """
            Getter for the quality
        """
        return self.Item['quality'] 
        
    def setYear(self,year):
        """
            Setter for the year
        """
        self.Item['year'] = year  
        
    def setMetadata(self,metadata):
        """
            Setter for the metadata
        """
        # ___ Load metada str in json object or dict in json obect __ Fix
        try:            
            if isinstance(metadata,str):
                meta = json.loads(metadata)
            else:
                meta = metadata
        except:                
            try:
                meta = ast.literal_eval(metadata)
            except:
                meta = metadata
        
        # ___  Case of array and not dict
        if isinstance(meta, list):
            meta = meta[0]
            
        self.Item['metadata'] = meta   
        
    def getMetadata(self):
        """
            Getter for the metadata
        """
        return self.Item['metadata'] 
           
    def setIconImage(self,iconImage):
        """
            Setter for the iconImage
        """
        self.Item['iconImage'] = iconImage
        
    
    def isFolder(self):
        """
            Is the item is folder ?
        """
        if  self.Item['action'] == self.ACTION_PLAY or \
            self.Item['action'] == self.ACTION_DISPLAY_SETTINGS or \
            self.Item['action'] == self.ACTION_DISPLAY_URLRESOLVER_SETTINGS or \
            self.Item['action'] == self.ACTION_DISPLAY_METAHANDLER_SETTINGS or \
            self.Item['action'] == self.ACTION_DISPLAY_DOWNLOAD_MANAGER or \
            self.Item['action'] == self.ACTION_SEARCH_WATAMOVIE or \
            (self.Item['action'] == self.ACTION_DISPLAY_LINKS and constant.__addon__.getSetting('links_in_dialog') == 'true') or \
            self.Item['action'] == self.ACTION_TEST :
            return False
        
        return True
    
    def getSubTypeValue(self):
        """
            Getter for subtype value
        """
        return self.Item['subtype_value']
    
    def setSubTypeValue(self,value):
        """
            Setter for subtype value
            @param value: the value for the subtype
        """
        self.Item['subtype_value'] = value
    
    def getPage(self):
        """
            Getter for page
        """
        return self.Item['page']
    
    def setPage(self,page):
        """
            Setter for page
            @param value: the page value
        """
        self.Item['page'] = page
        
    def getLinkStatus(self):
        """
            Getter for link status
        """
        return self.Item['linkStatus']
    
    def setLinkStatus(self,linkStatus):
        """
            Setter for the link status
            @param value: the link status value
        """
        self.Item['linkStatus'] = linkStatus
        
    
    def setKOLinkStatus(self):
        """
            Setter the link status 'KO'
        """
        self.setLinkStatus('KO')
        
    def copy(self):
        """
            Method to copy the current StreamItem
        """
        item = StreamItem(self.getTitle(),self.getJsonItem())
        return item
    
    def getPlayingFile(self):
        """
            Method to get the filename
            @note: Get the DB filename + the extensin
        """
        return self.getDbTitle()+'.'+webUtil.getFileExtension(self.getPlayableUrl())
    
    def isPage(self):
        """
            Method to know if the item is a page or not
        """
        try:
            if self.getType() == self.TYPE_PAGE or int(self.getPage()) > 0 :
                return True
        except:
            pass
        return False
    
    def getId(self):
        """
            Getter for the id
            @return:  the id
        """
        return self.Item['id']
    
    def setId(self,ide):
        """
            Setter of the id
            @param ide: the id
        """        
        if ide == 'None':
            self.Item['id'] = None 
        else:
            self.Item['id'] = ide        
        
    
    def getSourceId(self):
        """
            Getter for the source id
            @return:  the id
        """
        return self.Item['sourceId']
    
    def setSourceId(self,ide):
        """
            Setter of the source id
            @param ide: the id
        """        
        self.Item['sourceId'] = ide
        
    def setMetadataYear(self,year):
        """
            Method to set the year in the metadata
            @param year: the year
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
            
        self.Item['metadata']['year']=year
        
    
    def setMetadataOverview(self,overview):
        """
            Method to set the overview in the metadata
            @param overview: the overview
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        self.Item['metadata']['plot']=overview
        
    
    def setMetadataGenre(self,genre):
        """
            Method to set the genre in the metadata
            @param genre: the genre
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        self.Item['metadata']['genre']=genre       
    
    
    def setMetadataWriter(self,writer):
        """
            Method to set the writer in the metadata
            @param writer: the writer
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        self.Item['metadata']['writer']=writer
        
    
    def setMetadataCast(self,cast):
        """
            Method to set the casting in the metadata
            @param cast: the casting
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        
        if isinstance(cast, str):
            self.Item['metadata']['cast']=[cast]
        else:
            self.Item['metadata']['cast']=cast
        
        
    def setMetadataTitle(self):
        """
            Method to set the title in the metadata
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        self.Item['metadata']['title']=self.getTitle()
        
        
    def setPlayCount(self,value):
        """
            Method to set the title in the metadata
            @param value : 1 if the element is already watched, else 0
        """
        if isinstance(self.Item['metadata'], str):
            self.Item['metadata'] = {}
        self.Item['metadata']['playcount']=value
        
    def writeStrmFile(self,filePath):
        """
            Method to write a .strm file
        """
        # ___ Case of movie
        if not self.isPage() and self.getType() == self.TYPE_MOVIE:
            strmFile = open(os.path.join(filePath,self.getDbTitle()+'.strm'),'w')
            self.Item['strm']=1
            strmFile.write(self.getAddonUrl()) 
            strmFile.close()
        # ___ Case of tvshow
        elif not self.isPage() and self.getType() == self.TYPE_TVSHOW_EPISODE :
            tvShowDir = os.path.join(filePath,self.getTvShowName(),'Season '+str(self.getSeason()))
            if not os.path.exists(tvShowDir):
                os.makedirs(tvShowDir)
            strmFile = open(os.path.join(tvShowDir,self.getDbTitle()+'.strm'),'w')
            self.Item['strm']=1
            strmFile.write(self.getAddonUrl()) 
            strmFile.close()
        
    def writeNfoFile(self,filePath):
        """
            Method to write a .nfo file
        """
        if not self.isPage()and self.getType() == self.TYPE_MOVIE:
            nfoFile = open(os.path.join(filePath,self.getDbTitle()+'.nfo'),'w')
            nfoFile.write('<movie>\n' )
            nfoFile.write('\t<title>'+self.getTitle()+'</title>\n')
            nfoFile.write('\t<originaltitle>'+self.getTitle()+'</originaltitle>\n')
            nfoFile.write('\t<filenameandpath>'+self.getDbTitle()+'.strm</filenameandpath>\n')
            
            if self.Item['iconImage'] is not None and len(self.Item['iconImage'])>0:
                nfoFile.write('\t<thumb>'+self.Item['iconImage']+'</thumb>\n')
            elif 'cover_url' in self.Item['metadata'] and len(self.Item['metadata']['cover_url']) > 0:
                nfoFile.write('\t<thumb>'+self.Item['metadata']['cover_url']+'</thumb>\n')
            elif 'thumb_url' in self.Item['metadata'] and len(self.Item['metadata']['thumb_url']) > 0:
                nfoFile.write('\t<thumb>'+self.Item['metadata']['thumb_url']+'</thumb>\n')
              
            if 'playcount' in self.Item['metadata']:
                nfoFile.write('\t<playcount>'+str(self.Item['metadata']['playcount'])+'</playcount>\n')
                
            if 'tmdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['tmdb_id']))>0:
                nfoFile.write('\t<id>'+str(self.Item['metadata']['tmdb_id'])+'</id>\n')
            elif 'imdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['imdb_id']))>0:
                nfoFile.write('\t<id>'+str(self.Item['metadata']['imdb_id'])+'</id>\n')
            
            if 'plot' in self.Item['metadata'] and len(self.Item['metadata']['plot'])>0:
                nfoFile.write('\t<plot>'+self.Item['metadata']['plot'].encode('utf-8')+'</plot>\n')
            if 'votes' in self.Item['metadata'] and len(str(self.Item['metadata']['votes']))>0:
                nfoFile.write('\t<votes>'+str(self.Item['metadata']['votes'].encode('utf-8'))+'</votes>\n')
            if 'year' in self.Item['metadata']:
                nfoFile.write('\t<year>'+str(self.Item['metadata']['year'])+'</year>\n')
            if 'duration' in self.Item['metadata'] and len(str(self.Item['metadata']['duration']))>0:
                nfoFile.write('\t<runtime>'+str(self.Item['metadata']['duration'])+'</runtime>\n')
            if 'mpaa' in self.Item['metadata'] and len(self.Item['metadata']['mpaa'])>0:
                nfoFile.write('\t<mpaa>'+str(self.Item['metadata']['mpaa'].encode('utf-8'))+'</mpaa>\n')
            if 'rating' in self.Item['metadata']:
                nfoFile.write('\t<rating>'+str(self.Item['metadata']['rating'])+'</rating>\n')
            if 'director' in self.Item['metadata'] and len(self.Item['metadata']['director'])>0:
                nfoFile.write('\t<director>'+str(self.Item['metadata']['director'].encode('utf-8'))+'</director>\n')
            if 'studio' in self.Item['metadata'] and len(self.Item['metadata']['studio'])>0:
                nfoFile.write('\t<studio>'+str(self.Item['metadata']['studio'].encode('utf-8'))+'</studio>\n')
            if 'genre' in self.Item['metadata'] and len(self.Item['metadata']['genre'])>0:
                nfoFile.write('\t<genre>'+str(self.Item['metadata']['genre'].encode('utf-8'))+'</genre>\n')
            if 'tagline' in self.Item['metadata'] and len(self.Item['metadata']['tagline'])>0:
                nfoFile.write('\t<tagline>'+str(self.Item['metadata']['tagline'].encode('utf-8'))+'</tagline>\n')
            if 'writer' in self.Item['metadata'] and len(self.Item['metadata']['writer'])>0:
                nfoFile.write('\t<writer>'+str(self.Item['metadata']['writer'].encode('utf-8'))+'</writer>\n')
            
            nfoFile.write('</movie>\n' )
            
            if 'tmdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['tmdb_id']))>0:
                nfoFile.write('http://www.themoviedb.org/movie/'+self.Item['metadata']['tmdb_id'])
            elif 'imdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['imdb_id']))>0:
                nfoFile.write('http://www.imdb.com/title/'+self.Item['metadata']['imdb_id'])
                
            nfoFile.close()
        # ___ Case of tvshow
        elif not self.isPage() and self.getType() == self.TYPE_TVSHOW_EPISODE:
            tvShowDir = os.path.join(filePath,self.getTvShowName(),'Season '+str(self.getSeason()))
            if not os.path.exists(tvShowDir):
                os.makedirs(tvShowDir)
            nfoFile = open(os.path.join(tvShowDir,self.getDbTitle()+'.nfo'),'w')
            nfoFile.write('<episodedetails>\n' )
            """
            
            """
            nfoFile.write('\t<title>'+self.getTitle()+'</title>\n')
            nfoFile.write('\t<season>'+str(self.getSeason())+'</season>\n')
            nfoFile.write('\t<episode>'+str(self.getEpisodes())+'</episode>\n')
            #nfoFile.write('\t<filenameandpath>'+self.getDbTitle()+'.strm</filenameandpath>\n')
            
            if self.Item['iconImage'] is not None and len(self.Item['iconImage'])>0:
                nfoFile.write('\t<thumb>'+self.Item['iconImage']+'</thumb>\n')
            elif 'cover_url' in self.Item['metadata'] and len(self.Item['metadata']['cover_url']) > 0:
                nfoFile.write('\t<thumb>'+self.Item['metadata']['cover_url']+'</thumb>\n')
            elif 'thumb_url' in self.Item['metadata'] and len(self.Item['metadata']['thumb_url']) > 0:
                nfoFile.write('\t<thumb>'+self.Item['metadata']['thumb_url']+'</thumb>\n')
              
            if 'playcount' in self.Item['metadata']:
                nfoFile.write('\t<playcount>'+str(self.Item['metadata']['playcount'])+'</playcount>\n')
                
            if 'tmdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['tmdb_id']))>0:
                nfoFile.write('\t<id>'+str(self.Item['metadata']['tmdb_id'])+'</id>\n')
            elif 'imdb_id' in self.Item['metadata'] and len(self.Item['metadata']['imdb_id'])>0:
                nfoFile.write('\t<id>'+str(self.Item['metadata']['imdb_id'])+'</id>\n')
            
            if 'plot' in self.Item['metadata'] and len(self.Item['metadata']['plot'])>0:
                nfoFile.write('\t<plot>'+self.Item['metadata']['plot'].encode('utf-8')+'</plot>\n')
            if 'votes' in self.Item['metadata'] and len(str(self.Item['metadata']['votes']))>0:
                nfoFile.write('\t<votes>'+str(self.Item['metadata']['votes'].encode('utf-8'))+'</votes>\n')
            if 'year' in self.Item['metadata']:
                nfoFile.write('\t<year>'+str(self.Item['metadata']['year'])+'</year>\n')
            if 'duration' in self.Item['metadata'] and len(str(self.Item['metadata']['duration']))>0:
                nfoFile.write('\t<runtime>'+str(self.Item['metadata']['duration'])+'</runtime>\n')
            if 'mpaa' in self.Item['metadata'] and len(self.Item['metadata']['mpaa'])>0:
                nfoFile.write('\t<mpaa>'+str(self.Item['metadata']['mpaa'].encode('utf-8'))+'</mpaa>\n')
            if 'rating' in self.Item['metadata']:
                nfoFile.write('\t<rating>'+str(self.Item['metadata']['rating'])+'</rating>\n')
            if 'director' in self.Item['metadata'] and len(self.Item['metadata']['director'])>0:
                nfoFile.write('\t<director>'+str(self.Item['metadata']['director'].encode('utf-8'))+'</director>\n')
            if 'studio' in self.Item['metadata'] and len(self.Item['metadata']['studio'])>0:
                nfoFile.write('\t<studio>'+str(self.Item['metadata']['studio'].encode('utf-8'))+'</studio>\n')
            if 'genre' in self.Item['metadata'] and len(self.Item['metadata']['genre'])>0:
                nfoFile.write('\t<genre>'+str(self.Item['metadata']['genre'].encode('utf-8'))+'</genre>\n')
            if 'tagline' in self.Item['metadata'] and len(self.Item['metadata']['tagline'])>0:
                nfoFile.write('\t<tagline>'+str(self.Item['metadata']['tagline'].encode('utf-8'))+'</tagline>\n')
            if 'writer' in self.Item['metadata'] and len(self.Item['metadata']['writer'])>0:
                nfoFile.write('\t<writer>'+str(self.Item['metadata']['writer'].encode('utf-8'))+'</writer>\n')
            if 'aired' in self.Item['metadata'] and len(self.Item['metadata']['aired'])>0:
                nfoFile.write('\t<aired>'+str(self.Item['metadata']['aired'].encode('utf-8'))+'</aired>\n')
            if 'premiered' in self.Item['metadata'] and len(self.Item['metadata']['premiered'])>0:
                nfoFile.write('\t<premiered>'+str(self.Item['metadata']['premiered'].encode('utf-8'))+'</premiered>\n')
            
            nfoFile.write('</episodedetails>\n' )
            
            if 'tmdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['tmdb_id']))>0:
                nfoFile.write('http://www.themoviedb.org/tv/'+self.Item['metadata']['tmdb_id'])
            elif 'imdb_id' in self.Item['metadata'] and len(str(self.Item['metadata']['imdb_id']))>0:
                nfoFile.write('http://www.imdb.com/tv/'+self.Item['metadata']['imdb_id'])
                
            nfoFile.close()
     
    def getGAUrl(self):
        """
            Method to get the GA Url
            @return the GA url
        """
        url = 'UltraStream/'
        url += 'action='+str(self.getAction())
        url += 'type='+str(self.getType())
        url += 'subtype='+str(self.getSubType())
        return url
           
    def __compare__(self,title):
        """
            Method to compare the current title with an other title
            @param title: the title to compare
            @return the ratio matching
        """
        return SM(None, self.getTitle(), title).ratio()
    
    def __str__(self):
        """ 
            Method __str__ 
        """        
        return json.dumps(self.getJsonItem(), indent=4, sort_keys=True)
    

