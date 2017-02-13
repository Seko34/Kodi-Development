# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 17 Nov 2016

@author: Seko
@summary: Ultrastream Service

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmc
import xbmcgui
import constant
import metadata
from logger import Logger
from item import StreamItem

# ____________________     V A R I A B L E S     ____________________

# __ Init addon variable & Logger
__LOGGER__ = Logger('UltraStream-Service')

# ____________________     F U N C T I O N S       ____________________
def launchServices():
    """
        Method to launch ultrastream service
        @param __SOURCE__: the selected source   
    """
    import src_mod as sources
        
    __SOURCE__ = sources.getStreaminSource(constant.__addon__.getSetting('default_stream_src'))
    
    
    # ___ Get movie strm file
    if constant.__addon__.getSetting('activate_movie_service') == 'true':
        # ___ Init background progress
        progressDialogBG = xbmcgui.DialogProgressBG()
        progressDialogBG.create(constant.__addon__.getLocalizedString(90000),constant.__addon__.getLocalizedString(90001))
        
        # ___ Update background progress
        progressDialogBG.update(20)
        
        # ___ Get the list of items
        listItems = __SOURCE__.getMovieListService()
        
        if listItems is not None and len(listItems) > 0 : 
            # ___ Update background progress
            progressDialogBG.update(50)
            # ___ Get metadatas
            listItems = metadata.getMetadataForList(listItems[0].getType(), listItems,None,True)
            # ___ Update background progress
            progressDialogBG.update(80)
            
            # ___ For each element write strm and nfo files
            for item in listItems:
                if not item.isPage() :
                    item.writeStrmFile(constant.__addon__.getSetting('service_movie_dir'))
                    item.writeNfoFile(constant.__addon__.getSetting('service_movie_dir'))
            # ___ Update background progress        
            progressDialogBG.update(99)
            
        # ___ Close background      
        progressDialogBG.update(100)
        progressDialogBG.close()              
        progressDialogBG = None
        
    # ___ Get tv show strm file
    if constant.__addon__.getSetting('activate_tvshow_service') == 'true':
        # ___ Init background progress
        progressDialogBG = xbmcgui.DialogProgressBG()
        progressDialogBG.create(constant.__addon__.getLocalizedString(90000),constant.__addon__.getLocalizedString(90002))
        
        # ___ Update background progress
        progressDialogBG.update(20)
        
        # ___ Get the list of items
        listTvShow = __SOURCE__.getTvShowListService()
        
        
        if listTvShow is not None and len(listTvShow) > 0 : 
            
            # ___ Case of episodes items
            if listTvShow[0].getType() == StreamItem.TYPE_TVSHOW_EPISODE:
                # ___ Update background progress
                progressDialogBG.update(50)
                # ___ Get metadatas
                listTvShow = metadata.getMetadataForList(listTvShow[0].getType(), listTvShow,None,True)
                # ___ Update background progress
                progressDialogBG.update(80)
                
                # ___ For each element write strm and nfo files
                for item in listTvShow:
                    if not item.isPage() :
                        item.writeStrmFile(constant.__addon__.getSetting('service_tvshow_dir'))
                        item.writeNfoFile(constant.__addon__.getSetting('service_tvshow_dir'))
                
            # ___ Case of tvshow items
            elif listTvShow[0].getType() == StreamItem.TYPE_TVSHOW:
                
                count = 0
                # ___ For each tvshows, get the last season
                for tvShow in listTvShow:
                    count += 1
                    if not tvShow.isPage():
                        
                        seasons = __SOURCE__.getTvShowSeasons(tvShow)                      
                        # ___ Get the last seasons
                        if seasons is not None and len(seasons)>0:
                            
                            season = seasons[len(seasons)-1]
                            # ___ Get all episodes
                            episodes = __SOURCE__.getTvShowEpisodes(season)
                            
                            if episodes is not None and len(episodes)>0: 
                                # ___ Get the last episode
                                episode = episodes[len(episodes)-1]
                                # ___ Get metadatas
                                episode = metadata.getMetadata(episode,None,True)
                                # ___ Write strm and nfo files
                                episode.writeStrmFile(constant.__addon__.getSetting('service_tvshow_dir'))
                                episode.writeNfoFile(constant.__addon__.getSetting('service_tvshow_dir'))
                     
                    # ___ Update background progress
                    progressDialogBG.update(20+int(int(80*count)/len(listTvShow)))
             
            # ___ Case of seasons items       
            elif listTvShow[0].getType() == StreamItem.TYPE_TVSHOW_SEASON:
                count = 0
                # ___ For each season, get the last episode
                for tvShowSeason in listTvShow:
                    count += 1                                  
                    episodes = __SOURCE__.getTvShowEpisodes(tvShowSeason)
                    
                    if episodes is not None and len(episodes)>0:     
                        # ___ Get the last episode               
                        episode = episodes[len(episodes)-1]
                        # ___ Get metadatas
                        episode = metadata.getMetadata(episode,None,True)
                        # ___ Write strm and nfo files 
                        episode.writeStrmFile(constant.__addon__.getSetting('service_tvshow_dir'))
                        episode.writeNfoFile(constant.__addon__.getSetting('service_tvshow_dir'))
                    
                    # ___ Update background progress
                    progressDialogBG.update(20+int(int(80*count)/len(listTvShow)))
         
        # ___ Update background progress        
        progressDialogBG.update(100)
        # ___ Close background progress
        progressDialogBG.close()              
        progressDialogBG = None
            
    # ___ Force to update library if necessary
    if constant.__addon__.getSetting('activate_movie_service') == 'true':
        xbmc.executebuiltin('UpdateLibrary(video)') 
    elif constant.__addon__.getSetting('activate_tvshow_service') == 'true':
        xbmc.executebuiltin('UpdateLibrary(video)')       
    