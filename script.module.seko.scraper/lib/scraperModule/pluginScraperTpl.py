# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 12 Aug 2015

@author: Seko
@summary: The default Scraper

'''
#---------------------------------------------------------------------
# ____________________        I M P O R T        ____________________
import re

# ____________________         C L A S S         ____________________
class Scraper(object): 
    '''
        All scrapers should implements this interface
    '''
    
    name = "dummy scraper"
    id = 0
    
    def getName(self):
        '''
            Method to get the name of the scraper
        '''
        return self.name
        
    def getId(self):
        '''
            Method to get the name of the scraper
        '''
        return self.id
    
    def deleteAccent(self,title):
        """
            Method to delete accent from title
            
            @param title: the title to process
            
            @return the title without accent
        """
        accents = { 'a': ['à', 'ã', 'á', 'â'],
                    'e': ['é', 'è', 'ê', 'ë'],
                    'i': ['î', 'ï'],
                    'u': ['ù', 'ü', 'û'],
                    'o': ['ô', 'ö'] }
        for (char, accented_chars) in accents.iteritems():
            for accented_char in accented_chars:
                try:
                    title = title.replace(accented_char, char)
                except :
                    try:
                        title = title.decode('utf-8').replace(accented_char, char)
                    except :
                        pass
        return title
    
    def formatTitle(self, title):
        """
            Method to change the title
                -Remove the date in the movie name
            @param title: the title to process
            
            @param the processed title
        """
        
        # ___ Remove the date in the name (YYYY)
        patternDate = re.compile('.*\\(\d{4}\\)')
        match = patternDate.match(title.strip())
            
        if match is not None:
            title = title[0:title.rfind('(')]
        
        return title.strip()
    
    def getYearFromName(self,title):
        """
            Method to get the year in the name
            @param title: the name
            
            @return the year
        """
        patternDate = re.compile('.*\\(\d{4}\\)')
        match = patternDate.match(title.strip())
        if match is not None:        
            year = title[title.rfind(')')-4:title.rfind(')')]
        else:
            year = None
        
        return year
    
    def getMovieMeta(self, title, params=None):
        print 'Function undefined'
        return None
       
    def getTvShowMeta(self, title, params=None):
        print 'Function undefined'
        return None
    
    def getTvShowDetailsMeta(self, title, season, episode=False, params=None):
        print 'Function undefined'
        return None
    
    def getAnimeMeta(self,title):
        print 'Function undefined'
        return None
    
    def getAnimeDetailsMeta(self, title, season, episode=False, params=None):
        print 'Function undefined'
        return None