# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 31 Dec. 2017

@author: Seko
@summary: Favorite Util

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import os.path
import re
import xbmc
import xbmcaddon
import xbmcvfs
import strUtil
import miscFunctions
import json
from historyModule import __addon__

try:
    from sqlite3 import dbapi2 as sqlite
    xbmc.log("Loading sqlite3 as DB engine", xbmc.LOGDEBUG)
except:
    from pysqlite2 import dbapi2 as sqlite
    xbmc.log("Loading pysqlite2 as DB engine", xbmc.LOGDEBUG)
    

# ____________________        C L A S S        ____________________
class FavoriteUtil():
    
    def __init__(self):
        pass
    
    def initModule(self, addon_id, db_prefix): 
        # ___ Get addon
        self.__addon__       = xbmcaddon.Addon(id=addon_id)
        # ___ userdata addon directory
        self.__addondir__    = xbmc.translatePath( self.__addon__.getAddonInfo('profile') ) 
        # ___ db file
        self.__dbFile__ = os.path.join( self.__addondir__, db_prefix+'_favorite')
        
        try:
            self.db = sqlite.connect(self.__dbFile__)
            self.dbCursor = self.db.cursor()
            
            #if not self.isDbExists:
            self.createDatabase()
        except:
            
            xbmc.log("Error during connection to the favorite database", xbmc.LOGERROR)
            
            
               
        
    def createDatabase(self):
        
        # ___ Create table
        sql_create_db = "CREATE TABLE IF NOT EXISTS favorites (type TEXT, json TEXT);"
    
        self.dbCursor.execute(sql_create_db)
        
        try:
            self.db.commit() 
            
            xbmc.log("Database created",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during creating database with query "+sql_create_db,xbmc.LOGERROR)
         
        
        
    def clearAll(self):
        
        # ___ Delete all values
        sql_clear_db = "DELETE FROM favorites"
        
        self.dbCursor.execute(sql_clear_db)
        
        try:
            self.db.commit() 
            
            xbmc.log("clear all db with success",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during delete execution in db with query : "+sql_clear_db,xbmc.LOGERROR)
           
    
    def createFavorite(self,type, jsonR):
        
        # ___ Insert value
        sql_insert = "INSERT INTO favorites VALUES ( '%s', '%s')" % (type, json.dumps(jsonR))
        
        self.dbCursor.execute(sql_insert)
        
        try:
            self.db.commit() 
            miscFunctions.displayNotification('Add to favorite success','info')
            xbmc.log("Insert success in db with sql "+sql_insert,xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during insertion execution in db with query : "+sql_insert,xbmc.LOGERROR)
           
        
    def getFavorites(self, type):       
            
        clause_value = "type = '%s'" % (type)      
        
        sql_search = "SELECT type,json FROM favorites WHERE %s" % (clause_value)
        
        
        resultsJson = []
        try:
            self.dbCursor.execute(sql_search)
            results = self.dbCursor.fetchall() 
            if len(results) > 0: 
                for result in results:
                    jsonR = json.loads(result[1])                      
                    resultsJson.append(jsonR)
                    xbmc.log("Find %s success in db" % (clause_value),xbmc.LOGINFO)
                    
            return resultsJson
            
        except Exception, e:
            print str(e)
            xbmc.log("Error during select execution in db with query : "+sql_search,xbmc.LOGERROR)
        
        return resultsJson
        
        
    
    def hasFavorites(self,type):
        sql_search = "SELECT count(*) FROM favorites WHERE type ='%s'" % (type)
        
        results = []
        try:
            self.dbCursor.execute(sql_search)
            results = self.dbCursor.fetchall() 
            if len(results) > 0: 
                if int(results[0][0])>0:
                    return True
                                
        except Exception, e:
            print str(e)
            xbmc.log("Error during select execution in db with query : "+sql_search,xbmc.LOGERROR)
        
        return False
        
        
    def deleteHistory(self, jsonR):
        
        clause_value = "json = '%s'" % (json.dumps(jsonR))
                  
        sql_delete = "DELETE FROM favorites  WHERE %s" % (clause_value)
        
        self.dbCursor.execute(sql_delete)
        try:
            self.db.commit()             
            miscFunctions.displayNotification('Delete from favorite success','info')
            xbmc.log("Delete success in db",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during delete execution in db with query : "+sql_delete,xbmc.LOGERROR)
        
    def deleteAll(self):
        
                  
        sql_delete = "DELETE FROM favorites"
        
        self.dbCursor.execute(sql_delete)
        try:
            self.db.commit() 
            miscFunctions.displayNotification('Delete all favorites','info')            
            xbmc.log("Delete success in db",xbmc.LOGINFO)
        except Exception, e:
            xbmc.log("Error during delete execution in db with query : "+sql_delete,xbmc.LOGERROR)
        
    def __del__(self):
        
        # ___ Destroy object
        try:
            self.dbCursor.close()
            self.dbcon.close()
        except: pass
        
favUtil = FavoriteUtil()
favUtil.initModule('plugin.video.seko.ultrastream', 'ultrastream')
    