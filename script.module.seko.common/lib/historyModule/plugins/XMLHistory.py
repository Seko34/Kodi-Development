# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 26 Oct. 2014

@author: Seko
@summary: XML Util

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________

import elementtree.ElementTree as ET
import os.path
import xbmc
import xbmcaddon
from historyModule.pluginHistoryTpl import historyTemplate 
from _elementtree import Element

# ____________________     V A R I A B L E S     ____________________


    
# ____________________         C L A S S         ____________________ 

class XMLHistory(historyTemplate):
    
    def __init__(self):
        
        self.ID = 1
     
    def initModule(self, addon_id, db_prefix):   
        # ___ Get addon
        self.__addon__       = xbmcaddon.Addon(id=addon_id)
        # ___ userdata addon directory
        self.__addondir__    = xbmc.translatePath( self.__addon__.getAddonInfo('profile') ) 
        # ___ history file
        self.__history_file__ = os.path.join( self.__addondir__, db_prefix+'_history.xml')

    def createHistoryFile(self):
        """ 
            Method to create the history file
        """
        rootEl = ET.Element('histories')
        tree = ET.ElementTree(rootEl)
        # ___ Write the file
        tree.write(self.__history_file__)
        
        
    def parseHistoryFile(self):
        """
            Method to parse the history file
            
            @return the parsing of the history file
        """
        # ___ If the history file does not exist, we will create it
        if not os.path.isfile(self.__history_file__):
            self.createHistoryFile()
        
        # ___ return the parsing of the history file 
        return ET.parse(self.__history_file__)
    
    
    def createHistory(self,name, url, seektime, percent, isComplete, tvshow='', season='', episode=''):
        """
            Method to create a history line
            
            @param name : the movie name
            @param url : the url of the movie
            @param seekTime : the time watched
            @param percent : the percent of time watched
            @param isComplete : boolean which indicates if the watched is complete
        """
        
        # ___ Get the Tree
        tree = self.parseHistoryFile()
        
        # ___ Get the root element (histories)
        root = tree.getroot()
        
        # ___ Add the history element
        historyNode = ET.SubElement(root, "history")
        
        # ___ Add the name node to the history node
        nameNode = ET.SubElement(historyNode, "name")
        nameNode.text = name
        # ___ Add the url node to the history node
        urlNode = ET.SubElement(historyNode, "url")
        urlNode.text = url
        # ___ Add the seektime node to the history node
        seektimeNode = ET.SubElement(historyNode, "seektime")
        seektimeNode.text = str(seektime)  
        # ___ Add the percent node to the history node
        seektimeNode = ET.SubElement(historyNode, "percent")
        seektimeNode.text = str(percent)
        # ___ Add the isComplete node to the history node
        isCompleteNode = ET.SubElement(historyNode, "isComplete")
        isCompleteNode.text = str(isComplete)
        
        # ___ Add tvshow name
        tvshowNode = ET.SubElement(historyNode, "tvshow")
        if tvshow:
            tvshowNode.text = str(tvshow)
        else:            
            tvshowNode.text = str('')
            
        # ___ Add season
        seasonNode = ET.SubElement(historyNode, "season")
        if tvshow:
            seasonNode.text = str(season)
        else:            
            seasonNode.text = str('')
            
        # ___ Add episode
        episodeNode = ET.SubElement(historyNode, "episode")
        if tvshow:
            episodeNode.text = str(episode)
        else:            
            episodeNode.text = str('')
            
        
        # ___ Write the file
        xbmc.log("Write file "+self.__history_file__,xbmc.LOGDEBUG)
        tree = ET.ElementTree(root)
        tree.write(self.__history_file__)
        
    def findHistoryInXml(self, name, url = False, tvshow=False, season=False, episode=False):
        """
            Method to create a history line
            
            @param name : the movie name
            @param url : the url of the movie
            
            @return the (tree, element) couple if it exists, else return False
        """
        
        # ___ Get the Tree
        tree = self.parseHistoryFile()
        
        # ___ Get all history lines with the searched name
        for element in tree.getroot().findall("history"):
            
            # __ If the node url has the searched url
            if  element.find('name').text == name:
                
                # __ Check if the url is the same
                if url and element.find('url').text == url:
                    return (tree, element)
                
                # __ Else check others attributes
                elif not url:
                    
                    # __ If we search only by name
                    if not tvshow and not season and not episode:                    
                        return (tree, element)
                    # __ If search by name, tvshow, season and episode
                    elif element.find('tvshow').text == tvshow and element.find('season').text == season and element.find('episode').text == episode:
                        return (tree, element)
        
        # ___ If the element is not found, we return False  
        return (False, False)
    
    def findHistory(self, name, url = False, tvshow=False, season=False, episode=False):
        """
            Method to create a history line
            
            @param name : the movie name
            @param url : the url of the movie
            
            @return the (tree, element) couple if it exists, else return False
        """
        
        (tree, element) = self.findHistoryInXml(name, url, tvshow, season, episode)
        
        if tree and element:
            resultJSON = { 'name':element.find('name').text,
                           'url':element.find('url').text,
                           'seektime':element.find('seektime').text,
                           'percent':element.find('percent').text,
                           'isComplete':element.find('isComplete').text,
                           'tvshow':element.find('tvshow').text,
                           'season':element.find('season').text,
                           'episode':element.find('episode').text
                        }
            return resultJSON
        else:
            return None
        
    
    def updateHistory(self, name, url, seektime, percent, isComplete, tvshow=False, season=False, episode=False):
        """
            Method to update a history line
            
            @param name : the movie name
            @param url : the url of the movie
            @param seekTime : the time watched
            @param percent : the percent of time watched
            @param isComplete : boolean which indicates if the watched is complete
        """
        
        # ___ Search the history line
        tree, element = self.findHistoryInXml(name, url)
        
        # ___ If the element is not found, we create it
        if not element:        
            xbmc.log("Create history for "+name,xbmc.LOGDEBUG)
            self.createHistory(name, url, seektime, 0,  isComplete, tvshow, season, episode)
            
        # ___ else we update the line
        else:        
            xbmc.log("Update history for "+name,xbmc.LOGDEBUG) 
            # ___ Update the name node to the history node
            nameNode = element.find("name")
            nameNode.text = name
            # ___ Update the url node to the history node
            urlNode = element.find("url")
            urlNode.text = url
            # ___ Update the seektime node to the history node
            seektimeNode = element.find("seektime")
            seektimeNode.text = str(seektime)
            # ___ Update the percent node to the history node
            seektimeNode = element.find("percent")
            seektimeNode.text = str(percent) 
            # ___ Update the isComplete node to the history node
            isCompleteNode = element.find("isComplete")
            isCompleteNode.text = str(isComplete)
            # ___ Update tvshow name
            tvshowNode =  element.find("tvshow")
            if tvshow:
                tvshowNode.text = str(tvshow)
            else:            
                tvshowNode.text = str('')
                
            # ___ Update season
            seasonNode =  element.find("season")
            if tvshow:
                seasonNode.text = str(season)
            else:            
                seasonNode.text = str('')
                
            # ___ Update episode
            episodeNode =  element.find("episode")
            if tvshow:
                episodeNode.text = str(episode)
            else:            
                episodeNode.text = str('')
                
            # ___ Write the file
            tree.write(self.__history_file__)
            
                
                
            
    def deleteHistory(self, name, url = False, tvshow=False, season=False, episode=False):
        """
            Method to delete a history line
            
            @param name : the movie name
            @param url : the url of the movie
            @param tvshow : the tvshow name
            @param season : the season
            @param episode : the episode
        """
        
        # ___ Search the history line
        tree, element = self.findHistoryInXml(name, url, tvshow, season, episode)
        # ___ If the element is not found, we do nothing
        if not element:
            pass
        
        # ___ else we delete it
        else:
          
            # ___ Remove the element
            tree.remove(element)
            # ___ Write the file
            tree.write(self.__history_file__)
            
            
    def clearAll(self):        
        """
            Method to delete all history
        """
        # ___ Get the Tree
        tree = self.parseHistoryFile()
        
        # ___ Get all history lines with the searched name
        for element in tree.getroot().findall("history"):
            # ___ Remove the element
            tree.remove(element)
            
        # ___ Write the file
        tree.write(self.__history_file__)