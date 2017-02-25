# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 26 Oct. 2014

@author: Seko
@summary: XML Util

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import os.path
import re
import xbmc
import xbmcaddon
import xbmcvfs
import strUtil
from historyModule.pluginHistoryTpl import historyTemplate 

try:
    from sqlite3 import dbapi2 as sqlite
    xbmc.log("Loading sqlite3 as DB engine", xbmc.LOGDEBUG)
except:
    from pysqlite2 import dbapi2 as sqlite
    xbmc.log("Loading pysqlite2 as DB engine", xbmc.LOGDEBUG)
    
"""
    DbHistory  Class
"""
class DBHistory(historyTemplate):
    
    def __init__(self):
        
        self.ID = 2
    
    def initModule(self, addon_id, db_prefix): 
        # ___ Get addon
        self.__addon__       = xbmcaddon.Addon(id=addon_id)
        # ___ userdata addon directory
        self.__addondir__    = xbmc.translatePath( self.__addon__.getAddonInfo('profile') ) 
        # ___ db file
        self.__dbFile__ = os.path.join( self.__addondir__, db_prefix+'_history')
        
        #self.isDbExists = xbmcvfs.exists(self.__dbFile__)
        
        try:
            self.db = sqlite.connect(self.__dbFile__)
            self.dbCursor = self.db.cursor()
            
            #if not self.isDbExists:
            self.createDatabase()
        except:
            
            xbmc.log("Error during connection to the history database", xbmc.LOGERROR)
        
        
    def createDatabase(self):
        
        # ___ Create table
        sql_create_db = "CREATE TABLE IF NOT EXISTS history (name TEXT, url TEXT, seektime TEXT, percent REAL, isComplete INTEGER, tvshow TEXT, season TEXT, episode TEXT);"
    
        self.dbCursor.execute(sql_create_db)
        
        try:
            self.db.commit() 
            
            xbmc.log("Database created",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during creating database with query "+sql_create_db,xbmc.LOGERROR)
         
        
        
    def clearAll(self):
        
        # ___ Delete all values
        sql_clear_db = "DELETE FROM history"
        
        self.dbCursor.execute(sql_clear_db)
        
        try:
            self.db.commit() 
            
            xbmc.log("clear all db with success",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during delete execution in db with query : "+sql_clear_db,xbmc.LOGERROR)
           
    
    def createHistory(self,name, url, seektime, percent, isComplete, tvshow='', season='', episode=''):
        name = strUtil.remove_special_char(name)
        if tvshow and tvshow != '':
            tvshow = strUtil.remove_special_char(tvshow)
        # ___ Insert value
        sql_insert = "INSERT INTO history VALUES ( '%s', '%s', '%s', %s, %s, '%s', '%s', '%s')" % (name, url, seektime, percent, isComplete, tvshow, season, episode)
        
        self.dbCursor.execute(sql_insert)
        
        try:
            self.db.commit() 
            
            xbmc.log("Insert success in db with sql "+sql_insert,xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during insertion execution in db with query : "+sql_insert,xbmc.LOGERROR)
           
        
    def findHistory(self, name, url=False, tvshow=False, season=False, episode=False):
        name = strUtil.remove_special_char(name)
        if tvshow and tvshow != '':
            tvshow = strUtil.remove_special_char(tvshow)
            
        clause_value = "name = '%s'" % (name)      
        
        #if url:
        #   clause_value = clause_value + " AND url = '%s'" % (url)
        if tvshow:
            clause_value = clause_value + " AND tvshow = '%s'" % (tvshow)
        if season:
            clause_value = clause_value + " AND season = '%s'" % (season)
        if episode:
            clause_value = clause_value + " AND episode = '%s'" % (episode)
        
        sql_search = "SELECT * FROM history WHERE %s" % (clause_value)
        
        print sql_search
        
        try:
            self.dbCursor.execute(sql_search)
            result = self.dbCursor.fetchall() 
            if len(result) > 0: 
                resultJSON = { 'name':result[0][0],
                               'url':result[0][1],
                               'seektime':result[0][2],
                               'percent':result[0][3],
                               'isComplete':result[0][4],
                               'tvshow':result[0][5],
                               'season':result[0][6],
                               'episode':result[0][7]
                            }
                
                xbmc.log("Find %s success in db" % (clause_value),xbmc.LOGINFO)
                return resultJSON
            
        except Exception, e:
            print str(e)
            xbmc.log("Error during select execution in db with query : "+sql_search,xbmc.LOGERROR)
        
        return None
        
        
    
    def updateHistory(self, name, url, seektime, percent, isComplete, tvshow=False, season=False, episode=False):
        name = strUtil.remove_special_char(name)
        if tvshow and tvshow != '':
            tvshow = strUtil.remove_special_char(tvshow)
        if self.findHistory(name, url, tvshow, season, episode) is not None:
            clause_value = "name = '%s'" % (name)
            
            #if url:
            #    clause_value = clause_value + " AND url = '%s'" % (url)
            if tvshow:
                clause_value = clause_value + " AND tvshow = '%s'" % (tvshow)
            if season:
                clause_value = clause_value + " AND season = '%s'" % (season)
            if episode:
                clause_value = clause_value + " AND episode = '%s'" % (episode)
                
            sql_update = "UPDATE history SET seektime = '%s', percent = %s, isComplete = %s WHERE %s" % (seektime,percent,isComplete,clause_value) 
            
            self.dbCursor.execute(sql_update)
            try:
                self.db.commit() 
                
                xbmc.log("Update success in db",xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("Error during update execution in db with query : "+sql_update,xbmc.LOGERROR)
        else:
            self.createHistory(name, url, seektime, percent, isComplete, tvshow, season, episode)
        
        
    def deleteHistory(self, name, url = False, tvshow=False, season=False, episode=False):
        name = strUtil.remove_special_char(name)
        if tvshow and tvshow != '':
            tvshow = strUtil.remove_special_char(tvshow)
        clause_value = "name = '%s'" % (name)
        
        #if url:
        #    clause_value = clause_value + " AND url = '%s'" % (url)
        if tvshow:
            clause_value = clause_value + " AND tvshow = '%s'" % (tvshow)
        if season:
            clause_value = clause_value + " AND season = '%s'" % (season)
        if episode:
            clause_value = clause_value + " AND episode = '%s'" % (episode)
            
        sql_delete = "DELETE FROM history  WHERE %s" % (clause_value)
        
        self.dbCursor.execute(sql_delete)
        try:
            self.db.commit() 
            
            xbmc.log("Delete success in db",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during delete execution in db with query : "+sql_delete,xbmc.LOGERROR)
        
        
    def __del__(self):
        
        # ___ Destroy object
        try:
            self.dbCursor.close()
            self.dbcon.close()
        except: pass
    