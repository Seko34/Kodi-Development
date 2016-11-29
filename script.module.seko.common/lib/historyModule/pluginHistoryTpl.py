# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 23 Aug. 2015

@author: Seko
@summary: Template for history plugin class

'''
#---------------------------------------------------------------------


class historyTemplate(object):
    
    # ___ The module ID
    ID = -1
    
    """
        Template class for history module
    """
    def __init__(self):
        pass
    
    def getId(self):
        return self.ID
    
    def initModule(self, addon_id, db_prefix):
        pass
        
    def clearAll(self):
        pass
    
    def createHistory(self,name, url, seektime, percent, isComplete, tvshow='', season='', episode=''):
        pass
        
    def findHistory(self, name, url=False, tvshow=False, season=False, episode=False):
        pass
    
    def updateHistory(self, name, url, seektime, percent, isComplete, tvshow=False, season=False, episode=False):
        pass 
       
        
    def deleteHistory(self, name, url = False, tvshow=False, season=False, episode=False):
        pass
        
