# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 02 Jan 2016

@author: Seko
@summary: Router file

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
 
import sys
import xbmcaddon
import xbmc
import src_mod as sources
import cacheFunctions
import miscFunctions
import player
import xbmcgui
import downloaderModule
import metadata
import constant
import ga
from item import StreamItem
from resources.lib.trailer import YoutubeTrailer
from resources.lib.watamovie import Filmou 
from downloaderModule import DownloaderManager
import kodiUtil

    # ___ Get base_url, add_handle and arguments
__url__ = sys.argv[0]
    # ___ Get the handle integer
__handle__ = int(sys.argv[1])    



# ____________________     M E T H O D S     ____________________

def router(params):
    """
        Router function that calls other functions
        depending on the provided paramstring
        @param params: string slicing to trim the leading '?' from the plugin call paramstring
    
    """
    #params = dict(parse_qsl(paramstring))
    paramsItem = StreamItem(params=params)
    
    # ___ Google Analytics
    if constant.__kodiVersion__ >= 17:
        ga.pushData(paramsItem)
    
    # ___ Get the source
    __SOURCE__ = sources.getStreaminSource(constant.__addon__.getSetting('default_stream_src'))
    
    # ___ If the source of the streamItem is not None
    if paramsItem.getSourceId() is not None and len(paramsItem.getSourceId())>0:
        # ___ If the source of the streamItem is not the selected source in settings
        if paramsItem.getSourceId() != constant.__addon__.getSetting('default_stream_src'):
            # ___ Change the source with the item's source
            __SOURCE__ = sources.getStreaminSource(paramsItem.getSourceId())
           
    # ___ Check the parameters passed to the plugin
    if params:
        listItems = [] 
        progress = None
        
        # ___ Display list of link when launch the addon from .strm file
        if 'strm' in params and int(params['strm']) == 1:
                                
            # ___ Google Analytics
            if constant.__kodiVersion__ >= 17:
                ga.pushData(paramsItem,'strm')
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007))  
            
            # __ MOVIE LINK
            if int(params['type'])   == StreamItem.TYPE_MOVIE or int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                listItems = __SOURCE__.getMovieLink(paramsItem)
            # __ TV SHOW LINK
            elif int(params['type']) == StreamItem.TYPE_TVSHOW_EPISODE:                    
                listItems = __SOURCE__.getTvShowEpisodeLink(paramsItem)
            # __ ANIME LINK            
            elif int(params['type']) == StreamItem.TYPE_ANIME_EPISODE: 
                listItems = __SOURCE__.getAnimeEpisodeLink(paramsItem)
            # __ SHOW LINK            
            elif int(params['type']) == StreamItem.TYPE_SHOW: 
                listItems = __SOURCE__.getShowLink(paramsItem)
            # __ DOCUMENTARY LINK            
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY: 
                listItems = __SOURCE__.getDocumentaryLink(paramsItem)
            
            progress.close()            
            player.playStrm(listItems)
                
        # ___ Use cache if the cached page is the requested page
        # ___ Functionnality used until Kodi fix the cacheToDisc problem
        if cacheFunctions.isCachedPage(params) and int(params['action']) != StreamItem.ACTION_DISPLAY_MENU:            
            listItems = cacheFunctions.getPreviousCachedPage()            
        # ___ MAIN MENU
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_MENU :
            cacheFunctions.clearCache()
            __SOURCE__.build_menu()
        # ___ TYPE MENU
        elif paramsItem.getAction() == StreamItem.ACTION_DISPLAY_TYPE_MENU:
                        
            # ___ Movie Menu
            if int(params['type'])   == StreamItem.TYPE_MOVIE:
                __SOURCE__.build_movie_menu()
            # ___ Movie HD Menu
            elif int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                __SOURCE__.build_movie_hd_menu()
            # ___ Tvshow Menu
            elif int(params['type']) == StreamItem.TYPE_TVSHOW:
                __SOURCE__.build_tv_show_menu()
            # ___ Anime Menu
            elif int(params['type']) == StreamItem.TYPE_ANIME:
                __SOURCE__.build_anime_menu()
            # ___ Show Menu
            elif int(params['type']) == StreamItem.TYPE_SHOW:
                __SOURCE__.build_show_menu()
            # ___ Documentary Menu
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY:
                __SOURCE__.build_documentary_menu()
        
                    
        # ___ CATEGORIE MENU     
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_CATEGORIE_MENU:
            
            # __ Alphabetic
            if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                __SOURCE__.build_alphabetic_category(int(params['type']))
                
            # __ Genre
            if int(params['subtype']) == StreamItem.SUBTYPE_GENRE:
                __SOURCE__.build_genre_category(int(params['type']))
                   
        # __  DISPLAY LIST 
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_TYPE_LIST:            
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007))  
            
            # ___ MOVIE LIST
            if int(params['type']) == StreamItem.TYPE_MOVIE or int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                
                # __ Last
                if int(params['subtype'])   == StreamItem.SUBTYPE_LAST:
                    listItems = __SOURCE__.getLastMovie(paramsItem)
                # __ Top
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_RATE:
                    listItems = __SOURCE__.getTopMovie(paramsItem)
                # __ Top week
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_WEEK:
                    listItems = __SOURCE__.getTopWeekMovie(paramsItem)
                # __ Most view
                elif int(params['subtype']) == StreamItem.SUBTYPE_MOST_VIEW:
                    listItems = __SOURCE__.getMostViewMovie(paramsItem)   
                # __ Exclue
                elif int(params['subtype']) == StreamItem.SUBTYPE_EXCLUE:
                    listItems = __SOURCE__.getExclueMovie(paramsItem)    
                # __ List
                elif int(params['subtype']) == StreamItem.SUBTYPE_LIST:
                    listItems = __SOURCE__.getMovieList(paramsItem)               
                    
            # ___ TVSHOW LIST
            elif int(params['type']) == StreamItem.TYPE_TVSHOW:  
                
                #__ Last                  
                if int(params['subtype']) == StreamItem.SUBTYPE_LAST:
                    listItems = __SOURCE__.getLastTvShow(paramsItem)  
                # __ Top
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_RATE:
                    listItems = __SOURCE__.getTopTvShow(paramsItem)
                # __ Top week
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_WEEK:
                    listItems = __SOURCE__.getTopWeekTvShow(paramsItem)
                # __ Most view
                elif int(params['subtype']) == StreamItem.SUBTYPE_MOST_VIEW:
                    listItems = __SOURCE__.getMostViewTvShow(paramsItem)   
                # __ List
                elif int(params['subtype']) == StreamItem.SUBTYPE_LIST:
                    listItems = __SOURCE__.getTvShowList(paramsItem)                          
             
            # ___ ANIME LIST       
            elif int(params['type']) == StreamItem.TYPE_ANIME:   
                
                #__ Last          
                if int(params['subtype'])   == StreamItem.SUBTYPE_LAST:
                    listItems = __SOURCE__.getLastAnime(paramsItem)
                # __ Top
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_RATE:
                    listItems = __SOURCE__.getTopAnime(paramsItem)
                # __ Top week
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_WEEK:
                    listItems = __SOURCE__.getTopWeekAnime(paramsItem)
                # __ Most view
                elif int(params['subtype']) == StreamItem.SUBTYPE_MOST_VIEW:
                    listItems = __SOURCE__.getMostViewAnime(paramsItem)   
                # __ List
                elif int(params['subtype']) == StreamItem.SUBTYPE_LIST:
                    listItems = __SOURCE__.getAnimeList(paramsItem)          
                
                    
            # ___ SHOW LIST       
            elif int(params['type']) == StreamItem.TYPE_SHOW:   
                
                #__ Last          
                if int(params['subtype'])   == StreamItem.SUBTYPE_LAST:
                    listItems = __SOURCE__.getLastShow(paramsItem)
                # __ Top
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_RATE:
                    listItems = __SOURCE__.getTopShow(paramsItem)
                # __ Top week
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_WEEK:
                    listItems = __SOURCE__.getTopWeekShow(paramsItem)
                # __ Most view
                elif int(params['subtype']) == StreamItem.SUBTYPE_MOST_VIEW:
                    listItems = __SOURCE__.getMostViewShow(paramsItem)              
            
            # ___ DOCUMENTARY LIST       
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY:   
                
                #__ Last          
                if int(params['subtype'])   == StreamItem.SUBTYPE_LAST:
                    listItems = __SOURCE__.getLastDocumentary(paramsItem)
                # __ Top
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_RATE:
                    listItems = __SOURCE__.getTopDocumentary(paramsItem)
                # __ Top week
                elif int(params['subtype']) == StreamItem.SUBTYPE_TOP_WEEK:
                    listItems = __SOURCE__.getTopWeekDocumentary(paramsItem)
                # __ Most view
                elif int(params['subtype']) == StreamItem.SUBTYPE_MOST_VIEW:
                    listItems = __SOURCE__.getMostViewDocumentary(paramsItem)   
            
        # ___ DISPLAY CATEGORIE LIST 
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_CATEGORIE_LIST:
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
            
            # ___ MOVIE LIST
            if int(params['type'])   == StreamItem.TYPE_MOVIE :
                
                # __ Alphabetic
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticMovieList(paramsItem)
                
                # __ Genre
                if int(params['subtype']) == StreamItem.SUBTYPE_GENRE:
                    listItems = __SOURCE__.getMovieListByGenre(paramsItem)
                    
            # ___ MOVIE HD LIST              
            elif int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                
                # __ Alphabetic
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticMovieHDList(paramsItem)
                            
            # ___ TVSHOW LIST
            elif int(params['type']) == StreamItem.TYPE_TVSHOW:  
                
                #__ Alphabetic                 
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticTvShowList(paramsItem)        
             
            # ___ ANIME LIST       
            elif int(params['type']) == StreamItem.TYPE_ANIME:   
                
                #__ Alphabetic          
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticAnimeList(paramsItem)
                    
            # ___ SHOW LIST              
            elif int(params['type']) == StreamItem.TYPE_SHOW:
                
                # __ Alphabetic
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticShowList(paramsItem)
                    
            # ___ DOCUMENTARY LIST              
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY:
                
                # __ Alphabetic
                if int(params['subtype']) == StreamItem.SUBTYPE_ALPHABETICS:
                    listItems = __SOURCE__.getAlphabeticDocumentaryList(paramsItem)
            
        # ___ DISPLAY SEASON FOR ANIME OR TVSHOW
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_SEASONS:
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
            
            if int(params['type'])   == StreamItem.TYPE_TVSHOW:                    
                listItems = __SOURCE__.getTvShowSeasons(paramsItem)
            elif int(params['type']) == StreamItem.TYPE_ANIME:             
                listItems = __SOURCE__.getAnimeSeasons(paramsItem)
                
        # ___ DISPLAY EPISODES FOR ANIME OR TVSHOW    
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_EPISODES:
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
            
            if int(params['type'])   == StreamItem.TYPE_TVSHOW_SEASON:                    
                listItems = __SOURCE__.getTvShowEpisodes(paramsItem)
            elif int(params['type']) == StreamItem.TYPE_ANIME_SEASON:             
                listItems = __SOURCE__.getAnimeEpisodes(paramsItem)
            
        # ___ DISPLAY LINKS
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_LINKS and constant.__addon__.getSetting('links_in_dialog') == 'false':
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
            
            # __ MOVIE LINK
            if int(params['type'])   == StreamItem.TYPE_MOVIE or int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                listItems = __SOURCE__.getMovieLink(paramsItem)
            # __ TV SHOW LINK
            elif int(params['type']) == StreamItem.TYPE_TVSHOW_EPISODE:                    
                listItems = __SOURCE__.getTvShowEpisodeLink(paramsItem)
            # __ ANIME LINK            
            elif int(params['type']) == StreamItem.TYPE_ANIME_EPISODE: 
                listItems = __SOURCE__.getAnimeEpisodeLink(paramsItem)
            # __ SHOW LINK            
            elif int(params['type']) == StreamItem.TYPE_SHOW: 
                listItems = __SOURCE__.getShowLink(paramsItem)
            # __ DOCUMENTARY LINK            
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY: 
                listItems = __SOURCE__.getDocumentaryLink(paramsItem)
          
            # __ Add "More links" button
            moreLink = paramsItem.copy()
            moreLink.setAction(StreamItem.ACTION_MORE_LINKS)
            moreLink.regenerateKodiTitle()
            listItems.append(moreLink)
            
            # ___ Filter the links list
            listItems = miscFunctions.filterLinksList(listItems)
            
        # ___ GET MORE LINKS
        elif int(params['action']) == StreamItem.ACTION_MORE_LINKS and constant.__addon__.getSetting('links_in_dialog') == 'false':
            
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
            
            listItems = sources.getMoreLinks(constant.__addon__.getSetting('default_stream_src'), paramsItem)
            for item in listItems:
                item.setMetadata(paramsItem.getMetadata())
                
            # ___ Filter the links list
            listItems = miscFunctions.filterLinksList(listItems)
                
        # ___ SEARCH MOVIE, TVSHOW, ANIME ETC ...
        elif int(params['action']) == StreamItem.ACTION_SEARCH:
            keyboardInput =  xbmc.Keyboard('',constant.__addon__.getLocalizedString(33048),False)
            keyboardInput.doModal()
            
            # ___ If we search something
            if keyboardInput.isConfirmed():
                # Take the input text
                title=keyboardInput.getText()
            
                progress = xbmcgui.DialogProgress()
                progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
                                
                if int(params['type'])   == StreamItem.TYPE_MOVIE:
                    listItems = __SOURCE__.searchMovie(title)
                elif int(params['type']) == StreamItem.TYPE_MOVIE_HD:                    
                    listItems = __SOURCE__.searchMovie(title)
                elif int(params['type']) == StreamItem.TYPE_TVSHOW:                    
                    listItems = __SOURCE__.searchTvShow(title)
                elif int(params['type']) == StreamItem.TYPE_ANIME:
                    listItems = __SOURCE__.searchAnime(title)
                elif int(params['type']) == StreamItem.TYPE_SHOW:
                    listItems = __SOURCE__.searchShow(title)
                elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY:
                    listItems = __SOURCE__.searchDocumentary(title)
                    
        # ___ DISPLAY LINKS IN DIALOG
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_LINKS and constant.__addon__.getSetting('links_in_dialog') == 'true':
            
            # __ MOVIE LINK
            if int(params['type'])   == StreamItem.TYPE_MOVIE or int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                listItems = __SOURCE__.getMovieLink(paramsItem)
            # __ TV SHOW LINK
            elif int(params['type']) == StreamItem.TYPE_TVSHOW_EPISODE:                    
                listItems = __SOURCE__.getTvShowEpisodeLink(paramsItem)
            # __ ANIME LINK            
            elif int(params['type']) == StreamItem.TYPE_ANIME_EPISODE: 
                listItems = __SOURCE__.getAnimeEpisodeLink(paramsItem)
            # __ SHOW LINK            
            elif int(params['type']) == StreamItem.TYPE_SHOW: 
                listItems = __SOURCE__.getShowLink(paramsItem)
            # __ DOCUMENTARY LINK            
            elif int(params['type']) == StreamItem.TYPE_DOCUMENTARY: 
                listItems = __SOURCE__.getDocumentaryLink(paramsItem)
          
            # __ Add "More links" button
            moreLink = paramsItem.copy()
            moreLink.setAction(StreamItem.ACTION_MORE_LINKS)
            moreLink.regenerateKodiTitle()
            listItems.append(moreLink)
            
            # ___ Filter the links list
            listItems = miscFunctions.filterLinksList(listItems)
            
            player.displayLinksInDialog(listItems)
            
        # ___ GET MORE LINKS IN DIALOG
        elif int(params['action']) == StreamItem.ACTION_MORE_LINKS and constant.__addon__.getSetting('links_in_dialog') == 'true':
            
            listItems = sources.getMoreLinks(constant.__addon__.getSetting('default_stream_src'), paramsItem)
            for item in listItems:
                item.setMetadata(paramsItem.getMetadata())
            
            # ___ Filter the links list
            listItems = miscFunctions.filterLinksList(listItems)
            
            player.displayLinksInDialog(listItems)
            
        # ___ DISPLAY VIDEO OPTION           
        elif int(params['action']) == StreamItem.ACTION_PLAY:
                                
            # ___ Google Analytics
            if constant.__kodiVersion__ >= 17:
                ga.pushData(paramsItem,'play')
            player.displayVideoOptions(paramsItem)     
       
        # ___ SETTINGS MENU
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_MENU_SETTINGS:
            __SOURCE__.build_settings_menu()
        
        # ___ SETTINGS    
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_SETTINGS:
            constant.__addon__.openSettings() 
            
        # ___ METAHANDLER SETTINGS
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_METAHANDLER_SETTINGS:
            xbmcaddon.Addon(id='script.module.metahandler').openSettings() 
            
            
        # ___ URLRESOLVER SETTINGS
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_URLRESOLVER_SETTINGS:
            xbmcaddon.Addon(id='script.module.urlresolver').openSettings() 
            
        # ___ DOWNLOAD
        elif int(params['action']) == StreamItem.ACTION_DOWNLOAD:
            miscFunctions.downloadFile(paramsItem, playAtEnd=False)                 
            
        # ___ DOWNLOAD MANAGER
        elif int(params['action']) == StreamItem.ACTION_DISPLAY_DOWNLOAD_MANAGER:
            dlMod = downloaderModule.getDownloadModule(constant.__addon__.getSetting('downloader_module'));
            DownloaderManager.displayDownloadManager(__handle__,dlMod)
         
        # ___ PLAY TRAILER
        elif int(params['action']) == StreamItem.ACTION_PLAY_TRAILER:
            youtubeTrailer = YoutubeTrailer()
            youtubeTrailer.playTrailer(params['title'])
         
        # ___ WATAMOVIE SEARCH
        elif int(params['action']) == StreamItem.ACTION_SEARCH_WATAMOVIE:
            watam = Filmou()
            watam.doModal()
            del watam
            
        # ___ GLOBAL SEARCH
        elif int(params['action']) == StreamItem.ACTION_GLOBAL_SEARCH:
            keyboardInput =  xbmc.Keyboard('',constant.__addon__.getLocalizedString(33048),False)
            keyboardInput.doModal()
            
            # ___ If we search something
            if keyboardInput.isConfirmed():
                # Take the input text
                title=keyboardInput.getText()
            
                progress = xbmcgui.DialogProgress()
                progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
                                
                if int(params['type'])   == StreamItem.TYPE_MOVIE:
                    listItems = sources.searchMovie(title)
                elif int(params['type']) == StreamItem.TYPE_MOVIE_HD:
                    listItems = sources.searchMovie(title)
                elif int(params['type']) == StreamItem.TYPE_TVSHOW:                    
                    listItems = sources.searchTvShow(title)
                elif int(params['type']) == StreamItem.TYPE_ANIME:
                    listItems = sources.searchAnime(title)
        
        # ___ Get synopsis of selected item
        elif int(params['action']) == StreamItem.ACTION_GET_SYNOPSIS:
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70008))
            titleToSearch = params['title']
            params = cacheFunctions.getCachedParams()
            listItems = cacheFunctions.getCachedPage()
            listItems = metadata.getMetadataFromContextMenu(listItems,titleToSearch,progress)
            
        # ___ TEST ACTION
        elif int(params['action']) == StreamItem.ACTION_TEST:
            """
            params = {'subtitle': 'None', 
                      'hostName': 'Allvid', 
                      'isFolder': False, 
                      'href': 'http://allvid.ch/embed-fdyng0r2n5sj.html/', 
                      'playableUrl': u'http://212.7.213.12/oxyi6vzxwemxxkpdr63fvt4foq2yobougu6gav3wns6wujleoiojuc2mhdsa/v.mp4', 
                      'year': '', 
                      'quality': 'DVDRIP', 
                      'id': '23350', 
                      'title': 'Insaisissables 2', 
                      'type': 102, 'metadata': '', 
                      'dbTitle': 'Insaisissables 2', 
                      'iconImage': 'DefaultMovies.png', 
                      'season': '',
                      'tvShow': '',
                      'lang': 'None',
                      'episode': '', 
                      'dbTvShow': '', 
                      'sourceId': '', 
                      'subtype_value': '', 
                      'subtype': 0, 
                      'kodi_title': '[B]Insaisissables 2[/B]', 
                      'action': 18, 
                      'page': ''}
            fileToDl = StreamItem("Insaisissables 2", params)
            miscFunctions.downloadFile(fileToDl, False)
            """
            
            """
            listItem = __SOURCE__.getTopWeekMovie()
            if listItems is not None and len(listItems) > 0 : 
                listItems = metadata.getMetadataForList(listItem[0].getType(), listItems,None)
                for item in listItem:                    
                    item.writeStrmFile('D:\\test')
                    item.writeNfoFile('D:\\test')
            """
            pass
            
            
                
        # ___ Update the list of elements 
        if listItems is not None and len(listItems) > 0 :
            if progress is not None:
                progress.update(0,constant.__addon__.getLocalizedString(70008))
            else:
                progress = xbmcgui.DialogProgress()
                progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70008)) 
                 
            listItems = metadata.getMetadataForList(params['type'], listItems,progress) 
        
        # ___ Cached the current page before displaying it
        # ___ Functionnality used until Kodi fix the cacheToDisc problem
        if int(params['action']) != StreamItem.ACTION_DISPLAY_MENU and \
           int(params['action']) != StreamItem.ACTION_DISPLAY_TYPE_MENU and \
           int(params['action']) != StreamItem.ACTION_DISPLAY_CATEGORIE_MENU and \
           int(params['action']) != StreamItem.ACTION_DISPLAY_DOWNLOAD_MANAGER and \
           int(params['action']) != StreamItem.ACTION_GLOBAL_SEARCH and \
           int(params['action']) != StreamItem.ACTION_SEARCH_WATAMOVIE and \
           int(params['action']) != StreamItem.ACTION_SEARCH and \
           int(params['action']) != StreamItem.ACTION_PLAY and \
           int(params['action']) != StreamItem.ACTION_PLAY_TRAILER and \
           int(params['action']) != StreamItem.ACTION_DOWNLOAD and \
           int(params['action']) < StreamItem.ACTION_DISPLAY_MENU_SETTINGS:
            cacheFunctions.cachePage(params,listItems)
        
        # ___ Close the progress dialog
        if progress is not None:
            progress.close()
        
        # ___ Display all StreamItem
        miscFunctions.displayStreamItem(listItems)
        
    else:        
        cacheFunctions.clearCache()
        __SOURCE__.build_menu()
