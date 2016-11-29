# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 Aug 2015

@author: Seko
@summary: the metahandler scrapper
'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import xbmc
import re
from metahandler import metahandlers
from scraperModule.pluginScraperTpl import Scraper


class MetahandlerScraper(Scraper):

    # ____________________     OVERRIDE VARIABLES    ____________________
    name = "Metahandler scraper"
    id = 2
    
    # API KEY FOR THEMOVIEDB
    API_KEY = "47565088b22296f33e76445d59403e15"
    
    # ____________________     V A R I A B L E S     ____________________
   
    
    
    
    # ____________________     F U N C T I O N S     ____________________
    
    def getMovieMeta(self, title, params=None):
        
        self.metaget = metahandlers.MetaData(preparezip=False,tmdb_api_key = self.API_KEY)
        newtitle = self.formatTitle(title)
        newtitle = self.deleteAccent(newtitle)
        yearTitle = self.getYearFromName(title)
        try:
            if yearTitle is not None:
                infos = self.metaget.get_meta('movie', newtitle, year=self.getYearFromName(title))
            else:
                infos = self.metaget.get_meta('movie', newtitle)
        except:
            infos = None     
        if infos is not None:
            return {'info':infos,'iconImage':infos['backdrop_url'],'thumbnailImage':infos['cover_url']}
        else:
            return None
        
    def getTvShowMeta(self, title, params=None):
        self.metaget = metahandlers.MetaData(preparezip=False,tmdb_api_key = self.API_KEY)        
        newtitle = self.formatTitle(title)
        newtitle = self.deleteAccent(newtitle)
        try:
            infos = self.metaget.get_meta('tvshow', newtitle)
        except:
            infos = None     
        
        if infos is not None:
            return {'info':infos,'iconImage':infos['backdrop_url'],'thumbnailImage':infos['cover_url']}
        else:
            return None
    
    def getTvShowDetailsMeta(self, title, season, episode=False, params=None):
        self.metaget = metahandlers.MetaData(preparezip=False,tmdb_api_key = self.API_KEY)        
        newtitle = self.formatTitle(title)
        newtitle = self.deleteAccent(newtitle)
        if not episode:
            try:
                tvShowInfo = self.metaget.get_meta('tvshow', newtitle)
            except:
                tvShowInfo = None  
                
            if tvShowInfo is not None:      
                try:
                    infos = self.metaget.get_seasons(newtitle, tvShowInfo['imdb_id'], str(season))
                except:
                    infos = None
            else:
                infos = None
                
            if infos is not None and len(infos)>0:
                return {'info':infos}
            else:
                return None
            
        else:            
            tvShowInfo = self.metaget.get_meta('tvshow', newtitle)
            # ___ Remove the -
            patternEp = re.compile('(.*)(-)(.*)')
            match = patternEp.match(str(episode).strip())
                
            if match is not None:                
                episode = match.group(1).encode('UTF-8')
            
                
            infos = self.metaget.get_episode_meta( newtitle, tvShowInfo['imdb_id'], season, int(episode))
                           
            if infos is not None:
                return {'info':infos,'iconImage':infos['backdrop_url'],'thumbnailImage':infos['cover_url']}
            else:
                return None
            
    def getAnimeMeta(self,title, params=None):
        infos = self.getTvShowMeta(title)
        if infos is None :
            infos = self.getMovieMeta(title)
            if infos is None :
                return None
            else:
                return infos
        else:        
            return infos
    
    def getAnimeDetailsMeta(self, title, season, episode=False, params=None):
        
        return None
        '''
        if not episode:
            if str(season)=='False':
                season = 1
            return self.getTvShowDetailsMeta(title, str(season), False)
        else:
            if str(season)=='False':
                season = 1
            return self.getTvShowDetailsMeta(title, str(season), str(episode))
        '''