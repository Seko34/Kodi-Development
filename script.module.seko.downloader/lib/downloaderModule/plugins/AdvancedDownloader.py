# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 07 Nov. 2015

@author: Seko
@summary: Advanced Downloader

'''
#---------------------------------------------------------------------

# ____________________        I M P O R T        ____________________
import util
import xbmc
import xbmcaddon
import xbmcvfs
import xbmcgui
import StorageServer
import os
import re
import urllib2
import time
import zipfile
from contextlib import closing
from downloaderModule.pluginDownloaderTpl import downloaderTemplate 

# ___ Initialize database
try:
    from sqlite3 import dbapi2 as sqlite
    xbmc.log("[AdvDownloader] Loading sqlite3 as DB engine", xbmc.LOGDEBUG)
except:
    from pysqlite2 import dbapi2 as sqlite
    xbmc.log("[AdvDownloader] Loading pysqlite2 as DB engine", xbmc.LOGDEBUG)

    
"""
    AdvancedDownloader  Class
"""
class AdvancedDownloader(downloaderTemplate):
    
    # ___ HEADER CONFIGURATION FOR HTML REQUEST
    HEADER_CFG = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                   'Accept-Encoding': 'none',
                   'Accept-Language': 'en-US,en;q=0.8',
                   'Connection': 'keep-alive'}
    
    # ___ DOWNLOAD STATUS    
    STATUS_STARTING = 0
    STATUS_DOWNLOADING = 1
    STATUS_DOWNLOADING_READY_TO_PLAY = 2
    STATUS_STOPPED = 3
    STATUS_FINISHED = 4
    STATUS_ERROR = 5
    
    # ___ QUEUE TYPE
    QUEUE_DB = 1
    QUEUE_CACHE = 2
    
    # ___ progressDialog
    pDialog = None
    
    def __init__(self):
        """
            Constructor
        """        
        self.ID = 2
        
        # ___ Various variables        
        self.__addon__ = xbmcaddon.Addon(id='script.module.seko.downloader')
        self.__addonDir__ = xbmc.translatePath(self.__addon__.getAddonInfo('path'))   
        
        # ___ Init queue
        # ___ @Todo : Add variable to settings
        self.queueType = 1
        if self.queueType == self.QUEUE_DB:
            self.__queue__ = DatabaseQueue()
        elif self.queueType == self.QUEUE_CACHE:
            self.__queue__ = CacheQueue()
            
        xbmc.log("[AdvDownloader] Init Advanced Downloader Done", xbmc.LOGDEBUG)
         
    def clearAll(self):
        pass  
    
    def download(self, fileName, params, async=True):
        """
            Download method
            @param filename: the name of the file to download
            @param params: the dictionnary with informations about the file to download
                 The minimum format is : 
                 {
                 'url':'<the url to download the file>',
                 'title':'<Title of the movie>',
                 'destinationFolder':'<the destination folder>',
                 'webBrowserId': '<the web browser id>',
                 'playAtEnd': playAtEnd,  => Boolean which indicates if the download file should be play at the end of the download
                 
                 (-- No mandatory variable --)
                 'useragent': the user-agent to use for download the file                 
                 'incomplete_path': incomplete_path, => path where the temporary file is downloaded
                 
                 (-- Variable added after --) 
                 'fileName' : the file name                 
                 'complete_path': complete_path, => path where the complete file is moved        
                 'totalsize': totalsize, => the total size of the downloaded file
                 'current_dl_size': float(result[i][7]),
                 'current_percent_dl': float(result[i][8]),
                 'dl_status': int(result[i][9]),
                 'async': int(result[i][10]),                 
                 'queuePosition': the position in the queue, => calculate during insertion in the queue    
                                
                 (-- Variable for streamer --)
                 'cacheSize': cache Size, => the cache size in percent
                 'percent': percent, => the current progress in percent of the download
                 'oldpercent':oldpercent, 
                 'initialpercent': initialpercent, => the initial percent at the start of the download (used for resume download)
                                                     Used for calculating the percent cache
                 'percentcache': percentcache, => the percent to exceed for reaching the cache (initialpercent+cacheSize)
                 'percentforcache': percentforcache => the percent to exceed for reaching the cache
                 }                 
            @param async: Boolean which indicates if the download should be start in an other thread
        """
        # ___ Initialize all necessary variable
        # ___     Set the filename
        params['fileName'] = self._slugify(fileName)
        
        # ___     Set the async value
        if async:
            params['async'] = 1
        else:
            params['async'] = 0
            
            
        # ___     Set the playAtEnd value
        if params['playAtEnd'] == 'True':
            params['playAtEnd'] = 1
        else:
            params['playAtEnd'] = 0
         
        # ___     Set the complete_path value         
        params['complete_path'] = os.path.join(params['destinationFolder'], params['fileName'].encode("utf-8"))
        
        # ___ If incomplete path is not in params variable, the incomplete path will be the complete path.
        if 'incomplete_path' not in params :
            params['incomplete_path'] = params['complete_path']
        else:
            params['incomplete_path'] = os.path.join(params['incomplete_path'], params['fileName'].encode("utf-8"))
            
        params['totalsize'] = float(self._getTargetFileSize(params))
        params['current_dl_size'] = float(0)
        params['current_percent_dl'] = float(0)
        params['dl_status' ] = self.STATUS_STOPPED
        params['queuePosition'] = self.__queue__._getLastIndex() + 1
        
        # ___ Add element to the queue
        self.__queue__._clearQueue()
        self.__queue__._addToQueue(params['fileName'], params)
        
        if params['async'] == 1:
            xbmc.log("[AdvDownloader] Async", xbmc.LOGDEBUG)
            self._run_async(self._startDownload)            
            xbmc.log("[AdvDownloader] Download added to the queue", xbmc.LOGDEBUG)
        else:
            xbmc.log("[AdvDownloader] Normal", xbmc.LOGDEBUG)
            self._startDownload()
            xbmc.log("[AdvDownloader] Download done", xbmc.LOGDEBUG)
    
    def _processQueueDownload(self):
        item = self.__queue__._getNextItemFromQueue()
         
        if item:
            
            # __ If the progress dialog does not exist, we initialize it.
            if not self.pDialog :
                self.pDialog = xbmcgui.DialogProgressBG()
                self.pDialog.create("Progressbar", "")
            while item:
                # __ Default status = 500
                status = 500
                self._setPaths(item)
                
                # __ Verify parameters in item
                if not "url" in item:
                    xbmc.log("URL missing : %s" % repr(item), xbmc.LOGERROR)
                elif item["url"].find("ftp") > -1 or item["url"].find("http") > -1:
                    # __ Start to download a new item if it is a http or ftp url :
                    #       - Set the 'StopDownloaderQueue' to 'False'
                    #       - Download the file 
                    self.__queue__._setStopFlag(False)                                                
                    status = self._downloadURL(item)
                else:
                    # __ Bad URL
                    xbmc.log("[AdvDownloader] Bad url : "+item["url"], xbmc.LOGERROR)
               
                # __ If status = 200, the download is complete                
                if status == 200:
                    if xbmcvfs.exists(item["incomplete_path"]):
                        # __ Move the file from temp directory to the complete path.
                        xbmc.log("[AdvDownloader] Moving %s to %s" % (repr(item["incomplete_path"]), repr(item["complete_path"])),xbmc.LOGDEBUG)
                        if repr(item["incomplete_path"]) != repr(item["complete_path"]):
                            xbmcvfs.rename(item["incomplete_path"], item["complete_path"])
                        # __ Extract file if necessary
                            # __ Extract rar file
                        if str(item["complete_path"]).endswith(".rar"): 
                            xbmc.executebuiltin("XBMC.Extract("+str(item["complete_path"])+","+item["download_path"].decode("utf-8")+")")
                            
                            # __ Extract all zip file
                        elif str(item["complete_path"]).endswith(".zip"):
                            with zipfile.ZipFile(str(item["complete_path"]), "r") as compressFile:
                                compressFile.extractall(item["download_path"].decode("utf-8"))
                                
                        # __ Display complete message
                        self._showMessage("Download complete", item['fileName'])
                        
                        # __ Launch video if it is asked
                        if 'playAtEnd' in item and int(item['playAtEnd'])==1:
                            if not str(item["complete_path"]).endswith(".rar") and not str(item["complete_path"]).endswith(".zip"):
                                try:
                                    xbmc.Player(xbmc.PLAYER_CORE_AUTO).play(str(item["complete_path"]))
                                except Exception:
                                    xbmc.log("[AdvDownloader] Download complete, play movie failed",xbmc.LOGDEBUG)
                                    self._showMessage("Play movie failed", "ERROR")
                        
                    else:
                        xbmc.log("[AdvDownloader] Download complete, but file %s not found" % repr(item["incomplete_path"]),xbmc.LOGERROR)
                        self._showMessage("Download failed", "ERROR")
                        
                # __ Else if the status = 300, the download is failed
                elif status != 300:
                    xbmc.log("[AdvDownloader] Failure: " + repr(item) + " - " + repr(status),xbmc.LOGERROR)
                    self._showMessage("Download failed", "unknown error")
            
                # __ If status = 300, the download is just stopped.
                if status == 300:
                    item = False
                # __ Else delete incomplete path, and remove the item in the queue.
                else:
                    if xbmcvfs.exists(item["incomplete_path"]) and repr(item["incomplete_path"]) != repr(item["complete_path"]):
                        xbmcvfs.delete(item["incomplete_path"])
                    
                    self.__queue__._removeToQueue(item['fileName'])
                
                    # __ Get the next download
                    item = self.__queue__._getNextItemFromQueue()
            
            xbmc.log("[AdvDownloader] Finished download queue.",xbmc.LOGDEBUG)
            
            # __ Close the progress dialog at the end, if necessary
            if self.pDialog:
                self.pDialog.close()
                xbmc.log("[AdvDownloader] Closed dialog",xbmc.LOGDEBUG)
                self.pDialog = None
                    
                    
    def _downloadURL(self,item):
        """
            Method to download a file from an url
            @param item: the dictionnary with informations about the file to download
                        {'url': url,'incomplete_path': incomplete_path,'complete_path': complete_path,'playAtEnd': playAtEnd }
            
            @note: 
                -add 'old_percent' to item
                -add 'percentforcache' to item
        """
        xbmc.log('[AdvDownloader] '+item["fileName"],xbmc.LOGDEBUG)
        item["dl_status"]=self.STATUS_STARTING
        url = urllib2.Request(item["url"])
        
        shouldRestartDl = False
        params = {"bytes_so_far": 0, "mark": 0.0, "queue_mark": 0.0, "obytes_so_far": 0}
        item["current_percent_dl"] = 0.1
        item["old_percent"] = -1
        
        # __ Set the useragent in the header
        if "useragent" in item:
            url.add_header("User-Agent", item["useragent"])
        else:
            url.add_header("User-Agent", self.HEADER_CFG['User-Agent'])
            
        
        # __ Open the temporary file 'incomplete_path'
        if "current_dl_size" in item and float(item['current_dl_size']) > 0:
            # _ If we resume the download, we open the file with parameters 'ab' for appending bytes
            file = open(item["incomplete_path"], "ab")
        else:
            file = open(item["incomplete_path"], "wb")
            shouldRestartDl = True
        
        # __ If we should resume the download, add in the header "Range" with the file size
        if "current_dl_size" in item and float(item['current_dl_size']) > 0:
            xbmc.log("[AdvDownloader] Current size "+str(item['current_dl_size'])+" / Total size : "+str(item["totalsize"]),xbmc.LOGDEBUG)
            url.add_header("Range","bytes=%s-%s" % (item['current_dl_size'],item["totalsize"]))
            params["bytes_so_far"] = item['current_dl_size']
            
        
        # __ Start the connexion
        con = urllib2.urlopen(url)
    
        # __ Get headers informations, to know if we can resume the download
        responseHeader = con.info()
        
            
        if 'Accept-Ranges' in responseHeader:
            xbmc.log("[AdvDownloader] Accept-Ranges: "+responseHeader['Accept-Ranges'],xbmc.LOGINFO)
            
        if "current_dl_size" in item and 'Accept-Ranges' in responseHeader and responseHeader['Accept-Ranges'] == 'none':
            # ___ If we can't resume the download, we re start the download
            url = urllib2.Request(item["url"])
            # __ Set the useragent in the header
            if "useragent" in item:
                url.add_header("User-Agent", item["useragent"])
            else:
                url.add_header("User-Agent", self.HEADER_CFG["User-Agent"])
            # __ Delete the temporary file 'incomplete_path'
            xbmcvfs.delete(item["incomplete_path"])
            # __ Open the temporary file 'incomplete_path'
            file = open(item["incomplete_path"], "wb")
            # close the current connection
            con.close()
            # __ Restart the connection
            con = urllib2.urlopen(url)
            # __ Set shouldRestartDl to True
            shouldRestartDl = True
            item['current_dl_size'] = float(0)
            
            
        # __ Set the chunk_size
        chunk_size = 1024 * 8  
           
        # __ If we should resume the download, calculate the percent
        if "current_dl_size" in item and float(item['current_dl_size']) > 0 :    
            # __ Calculate the percent
            self._generatePercent(item, params)
            
        try:
            
            # __ Download the file until it is complete or until asking for stop
            item["dl_status"]=self.STATUS_DOWNLOADING
            while (not self.__queue__._shouldStop() ):                
                # Read next 'chunk_size'
                chunk = con.read(chunk_size)    
                # Write             
                file.write(chunk)
                # Increase bytes_so_far
                params["bytes_so_far"] += len(chunk)

                if params["mark"] == 0.0 and params["bytes_so_far"] > 0:
                    params["mark"] = time.time()
                    xbmc.log("[AdvDownloader] Mark set",xbmc.LOGDEBUG)
                
                # __ Calculate the percent
                self._generatePercent(item, params)
                    
                # xbmc.log("recieved chunk: %s - %s" % ( repr(item["percent"] > item["old_percent"]), repr(time.time() - params["queue_mark"])),xbmc.LOGDEBUG)
                   
                if item["current_percent_dl"] > item["old_percent"] or time.time() - params["queue_mark"] > 30:
                    # __ Update the progress bar asynchronous if the download is not for streamer
                    self._run_async(self._updateProgress(item, params))
                    item["old_percent"] = item["current_percent_dl"]

                params["obytes_so_far"] = params["bytes_so_far"]
                
                
                # _ Break when the chunk is None
                if not chunk:
                    break
                           
            # __ Close connection and the file            
            xbmc.log("[AdvDownloader] Loop done",xbmc.LOGDEBUG)            
            con.close()
            file.close()
            
            
        except Exception, e:
            print str(e)
            xbmc.log("Error : "+repr(e),xbmc.LOGERROR)            
            xbmc.log("Download failed.",xbmc.LOGERROR)
            try:
                con.close()
            except:
                xbmc.log("Failed to close download stream")

            try:
                file.close()
            except:
                xbmc.log("Failed to close file handle")

            self._showMessage("Download failed", "ERROR")
                        
            # ___ Set status to stopped
            item['dl_status'] = self.STATUS_ERROR
            
            # __ Return 500 if the download is failed due to an error
            return 500

        
        if self.__queue__._shouldStop() and int(item["current_percent_dl"]) < 99 :
            # __ Return 300 if the download is aborted           
            xbmc.log("[AdvDownloader] Download aborted : "+str(self.__queue__._shouldStop()),xbmc.LOGINFO)

            # ___ Set status to stopped
            item['dl_status'] = self.STATUS_STOPPED  
            self.__queue__._updateQueueItem(item['fileName'],item)          
            return 300
        
        # ___ Set status to stopped
        item['dl_status'] = self.STATUS_FINISHED
        self.__queue__._updateQueueItem(item['fileName'],item)
        
        # __ Return 200 if the download is complete
        xbmc.log("[AdvDownloader] _downloadURL Done",xbmc.LOGERROR)    
        return 200         


    def _setPaths(self, params):
        """"
            _setPaths Method
            Method to set :
                -the 'incomplete_path' in the 'params' variable
                -the 'complete_path' in the 'params' variable
                
            @param params: the dictionnary with informations about the file to download
            
        """
        xbmc.log('[AdvDownloader] '+params['fileName'], xbmc.LOGDEBUG)
        # Check utf-8 stuff here
        xbmc.log("[AdvDownloader] Path incomplete: "+params["incomplete_path"], xbmc.LOGDEBUG)
        xbmc.log("[AdvDownloader] Path complete: "+params["complete_path"], xbmc.LOGDEBUG)

        # __ If the 'complete_path' already exists, delete it
        if xbmcvfs.exists(params["complete_path"]):
            xbmc.log("[AdvDownloader] Removing existing %s" % repr(params["complete_path"]), xbmc.LOGDEBUG)
            xbmcvfs.delete(params["complete_path"])
        
        # __ If the 'incomplete_path' already exists, delete it
        if xbmcvfs.exists(params["incomplete_path"]):
            if self._confirmResume(self.__addon__.getLocalizedString(33207),self.__addon__.getLocalizedString(33208)+params['fileName']):
                xbmc.log("[AdvDownloader] Resuming incomplete %s" % repr(params["incomplete_path"]), xbmc.LOGDEBUG)
                params['current_dl_size']=self._getFileSize(params["incomplete_path"])
            else:
                xbmc.log("[AdvDownloader] Removing incomplete %s" % repr(params["incomplete_path"]), xbmc.LOGDEBUG)
                xbmcvfs.delete(params["incomplete_path"])

        xbmc.log("[AdvDownloader] _setPaths Done", xbmc.LOGDEBUG)
        
    def _generatePercent(self, item, params):
        """
            Method _generatePercent
            @param item: the item for updating the percent
            @param params: all parameters associated with the item
            
        """
        get = params.get
        iget = item.get

        new_delta = False
        if "last_delta" in item:
            if time.time() - item["last_delta"] > 0.2:
                new_delta = True
        else:
            item["last_delta"] = 0.0
            new_delta = True

        item['current_dl_size'] = get("bytes_so_far")
        if item["totalsize"] > 0 and new_delta:
            item["current_percent_dl"] = ( float(get("bytes_so_far")) * 100) / float(item["totalsize"])
        elif iget("duration") and get("mark") != 0.0 and new_delta:
            time_spent = time.time() - get("mark")
            item["current_percent_dl"] = time_spent / int(iget("duration")) * 100
            xbmc.log("[AdvDownloader] Time spent: %s. Duration: %s. Time left: %s (%s)" % (int(time_spent), int(iget("duration")),
                                                                                  int(int(iget("duration")) - time_spent),
                                                                                  self._convertSecondsToHuman(int(iget("duration")) - time_spent)), xbmc.LOGDEBUG)

        elif new_delta:
            xbmc.log("[AdvDownloader] cycle - " + str(time.time() - item["last_delta"]), xbmc.LOGDEBUG)
            delta = time.time() - item["last_delta"]
            if delta > 10 or delta < 0:
                delta = 5

            item["current_percent_dl"] = iget("old_percent") + delta
            if item["current_percent_dl"] >= 100:
                item["current_percent_dl"] -= 100
                item["old_percent"] = item["current_percent_dl"]

        if new_delta:
            item["last_delta"] = time.time()
             
    def _updateProgress(self, item, params):
        """
            Method _updateProgress
            @param item: the current item
            @param params: the dictionnary with informations about the file to download
        """
        get = params.get
        iget = item.get
        queue = False
        new_mark = time.time()
        
        if new_mark == get("mark"):
            speed = 0
        else:
            speed = int((get("bytes_so_far") / 1024) / (new_mark - get("mark")))
                 

        if new_mark - get("queue_mark") > 1.5:
            heading = u"[%s] %sKb/s (%.2f%%)" % (self.__queue__._getLastIndex(), speed, item["current_percent_dl"])
            xbmc.log("[AdvDownloader] Updating %s - %s" % (heading, item['fileName'].encode("utf-8")), xbmc.LOGDEBUG)
            params["queue_mark"] = new_mark
            self.__queue__._updateQueueItem(item['fileName'],item)
        
        
        if xbmc.Player().isPlaying() and xbmc.getCondVisibility("VideoPlayer.IsFullscreen"):
            # __ Hide the progress dialog  if we start to play a movie
            if self.pDialog:
                self.pDialog.close()
                self.pDialog = None
        else:
            # __ Initialize the progress dialog if it is closed
            if not self.pDialog:
                self.pDialog = xbmcgui.DialogProgressBG()
                self.pDialog.create("Preparing download", "")
           
            heading = u"[%s] %s - %.2f%% (%s Kb/s)" % (str(self.__queue__._getLastIndex()), "Downloading", float(item["current_percent_dl"]),speed)
            xbmc.log("[AdvDownloader] Heading : "+heading, xbmc.LOGDEBUG)
            
            # __ Update the progress dialog 
            if iget("Title"):
                self.pDialog.update(int(item["current_percent_dl"]), heading, iget("Title"))
            else:
                xbmc.log("[AdvDownloader] Try to update the dialog",xbmc.LOGDEBUG)
                self.pDialog.update(int(item["current_percent_dl"]), heading, item['fileName'])
        xbmc.log("[AdvDownloader] _updateProgress Done", xbmc.LOGDEBUG)


    def _startDownload(self):
        self._processQueueDownload()
    
    def _stopDownload(self):
        self.__queue__._askStop()
    
    def _pauseDownload(self):
        pass
    
    def _resumeDownload(self):
        pass

    def getQueue(self):
        return self.__queue__._getQueue()
    
    def _run_async(self, func, *args, **kwargs):
        """
            Method _run_async
            @param func: the function to execute asynchronous
            @param *args: the arguments passed into the function called
            @param **kwargs: others arguments
            
            @return the thread started
        """
        from threading import Thread
         
        worker = Thread(target=func, args=args, kwargs=kwargs)
        worker.start()
        return worker   
    
    def _showMessage(self, heading, message):
        """
            Method to show a notification
            @param heading : the heading text
            @param message : the message of the notification            
        """
        xbmc.executebuiltin((u'XBMC.Notification("%s", "%s", %s)' % (heading, message.encode("utf-8"), 2000)).encode("utf-8"))
   
    def _showDialog(self, heading, message): 
        """
            Method to show a "ok" dialog window
            @param heading : the heading text
            @param message : the message of the dialog window            
        """       
        dialog = xbmcgui.Dialog()
        dialog.ok(heading, message)
    
    def _confirmResume(self, heading, line1, line2="", line3=""):
        """
            Method to ask a confirmation for resuming the download
            @param heading: the heading text
            @param line1 : the first line of the confirmation dialog 
            @param line2 : the second line of the confirmation dialog 
            @param line3 : the third line of the confirmation dialog 
            
            @return: true if the user confirm the resume of dialog
        """
        dialog = xbmcgui.Dialog()
        return dialog.yesno(heading, line1, line2, line3)
    
    def _getTargetFileSize(self, item):
        """
            Method to get a size of a file from an url
            @param itemParams: Dictionnary which represents the file. It contains the url to downlaod the file.
            
            @return the item with the size of the file in the parameter 'total_size'
        """
        url = urllib2.Request(item["url"], headers=AdvancedDownloader.HEADER_CFG)        
        
        # __ Set the useragent in the header
        if "useragent" in item:
            url.add_header("User-Agent", item["useragent"])
                
        # __ Start the connexion
        con = urllib2.urlopen(url)

        total_size = 0        

        # __ Set the total size
        if con.info().getheader("Content-Length").strip():
            total_size = int(con.info().getheader("Content-Length").strip()) 
            
        # __ Return the total size
        return  total_size
    
    def _slugify(self, value):
        """
            Method to :
                Normalizes string, converts to lowercase, removes non-alpha characters,
                and converts spaces to hyphens.
        """
        import unicodedata
        extension = value[len(value) - 4:]
        value = value[:len(value) - 4]
        value = value.decode("utf-8")
        value = value.decode('unicode-escape','ignore')
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
        value = unicode(re.sub('[^\w\s\.-]', ' ', value).strip().lower())
        value = re.sub('[-\s]+', ' ', value)
        return value + extension
    
    def _convertSecondsToHuman(self, seconds):
        """
            Method _convertSecondsToHuman
            @param seconds:the number of seconds
            
            @return a number of seconds if the input is inferior of 60 seconds, else return a number of minutes
        """
        seconds = int(seconds)
        if seconds < 60:
            return "~%ss" % (seconds)
        elif seconds < 3600:
            return "~%sm" % (seconds / 60)
    
    def _isStarted(self):
        pass
    

class QueueClass():
    
    """
        Defaut queue class
    """
    def _getQueue(self):
        pass 
    
    def _getNextItemFromQueue(self):
        pass
        
    def _getLastIndex(self):
        pass        
    
    def _addToQueue(self, fileName, params):       
        pass
    
    def _removeToQueue(self, fileName, params={}):
        pass

    def _clearQueue(self):
        pass
    
    def _updateQueueItem(self,fileName,params):
        pass       
        
    def _shouldStop(self):
        pass

    def _askStop(self):
        pass            
     
    def _setStopFlag(self,shouldStop):
        pass   
    
    
class DatabaseQueue(QueueClass):    
    """
        Database queue class
    """
    
    def __init__(self):
        self.__addon__ = xbmcaddon.Addon(id='script.module.seko.downloader')
        self.__addonDir__ = xbmc.translatePath(self.__addon__.getAddonInfo('path'))
        
        # ___ Initialize database
        # ___     db file
        self.__dbFile__ = os.path.join(self.__addonDir__, 'AdvancedDownloader.db')        
        
        try:          
            self.createDatabase()
        except:            
            xbmc.log("[AdvDownloader] Error during connection to the downloader database", xbmc.LOGERROR)
        
        
    def createDatabase(self):              
        
        # ___ Create table with columns:
        # queuePosition INT
        # fileName TEXT
        # url TEXT
        # title TEXT
        # incomplete_path TEXT
        # complete_path TEXT
        # total_size REAL
        # current_dl_size REAL
        # current_percent_dl REAL
        # dl_status INT
        # async INT
        # playAtEnd INT
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            sql_create_db = "CREATE TABLE IF NOT EXISTS AdvDownloader (queuePosition INTEGER, fileName TEXT, url TEXT, title TEXT, incomplete_path TEXT, complet_path TEXT, total_size REAL, current_dl_size REAL, current_percent_dl REAL, dl_status INTEGER, async INTEGER, playAtEnd INTEGER);"
            dbCursor.execute(sql_create_db)
            
            try:
                db.commit()             
                xbmc.log("[AdvDownloader] Database created",xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("[AdvDownloader] Error during creating database with query " + sql_create_db, xbmc.LOGERROR)
    
    def _getQueue(self):        
        
        resultList = []
        # ___ Select sql (12)        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            sql_select = "SELECT * from AdvDownloader;"
            # queuePosition
            # fileName
            # url
            # title
            # incomplete_path
            # complete_path
            # total_size
            # current_dl_size
            # current_percent_dl
            # dl_status
            # async
            # playAtEnd
            try:
                dbCursor.execute(sql_select)
                result = dbCursor.fetchall() 
                if len(result) > 0: 
                    for i in result:              
                        itemJSON = {
                                    'queuePosition': i[0],
                                    'fileName': i[1],
                                    'url':i[2],
                                    'title':i[3],
                                    'destinationFolder':i[5],
                                    'webBrowserId': 0,
                                    'incomplete_path': i[4],
                                    'complete_path': i[5],
                                    'totalsize': float(i[6]),
                                    'current_dl_size': float(i[7]),
                                    'current_percent_dl': float(i[8]),
                                    'dl_status': int(i[9]),
                                    'async': int(i[10]),
                                    'playAtEnd': int(i[11])
                                    }
                        resultList.append(itemJSON)              
                    xbmc.log("[AdvDownloader] Get the queue list success in db" , xbmc.LOGINFO)
                    return resultList
                
            except Exception, e:
                xbmc.log(str(e))
                xbmc.log("[AdvDownloader] Error during select execution in db with query : " + sql_select, xbmc.LOGERROR)
        
        return None 
    
    def _getNextItemFromQueue(self):
            
        # ___ Select sql (12)
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            
            sql_select = "SELECT * FROM AdvDownloader ORDER BY queuePosition ASC;"            
            # queuePosition
            # fileName
            # url
            # title
            # incomplete_path
            # complete_path
            # total_size
            # current_dl_size
            # current_percent_dl
            # dl_status
            # async
            # playAtEnd
            try:
                dbCursor.execute(sql_select)
                result = dbCursor.fetchall() 
                if len(result) > 0: 
                                      
                    itemJSON = {
                                'queuePosition': result[0][0],
                                'fileName': result[0][1],
                                'url':result[0][2],
                                'title':result[0][3],
                                'destinationFolder':result[0][5],
                                'webBrowserId': 0,
                                'incomplete_path': result[0][4],
                                'complete_path': result[0][5],
                                'totalsize': float(result[0][6]),
                                'current_dl_size': float(result[0][7]),
                                'current_percent_dl': float(result[0][8]),
                                'dl_status': int(result[0][9]),
                                'async': int(result[0][10]),
                                'playAtEnd': int(result[0][11])
                                }
                                      
                    xbmc.log("[AdvDownloader] Find next element %s success in db" % (itemJSON['fileName']), xbmc.LOGINFO)
                    return itemJSON
                
            except Exception, e:
                print str(e)
                xbmc.log("[AdvDownloader] Error during select execution in db with query : " + sql_select, xbmc.LOGERROR)
        
        return None
        
        
    def _getLastIndex(self):
        
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            # ___ Select sql  (12)
            sql_select = "SELECT max(queuePosition) from  AdvDownloader;"
            try:
                dbCursor.execute(sql_select)
                result = dbCursor.fetchall() 
                if len(result) > 0: 
                    if result[0][0] == None:
                        maxIndex = 0
                    else:
                        maxIndex = int(result[0][0])                
                    xbmc.log("[AdvDownloader] Find last index %s success in db" % (maxIndex), xbmc.LOGINFO)
                    return maxIndex
                
            except Exception, e:
                print str(e)
                xbmc.log("[AdvDownloader] Error during select execution in db with query : " + sql_select, xbmc.LOGERROR)
        
        return 0
        
    def _searchItem(self,item):
        """
            Method to search an item in the queue
            
            @param item: the item to search
        """
        
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            # ___ Select sql  (12)
            sql_select = "SELECT * from  AdvDownloader WHERE fileName = '"+item['fileName']+"';"
            try:
                dbCursor.execute(sql_select)
                result = dbCursor.fetchall() 
                if len(result) > 0 : 
                    if result[0][0] == None:
                        xbmc.log("[AdvDownloader] No element %s in db" % (item['fileName']), xbmc.LOGINFO)
                        return None
                    else:
                        itemJSON = {
                                'queuePosition': result[0][0],
                                'fileName': result[0][1],
                                'url':result[0][2],
                                'title':result[0][3],
                                'destinationFolder':result[0][5],
                                'webBrowserId': 0,
                                'incomplete_path': result[0][4],
                                'complete_path': result[0][5],
                                'totalsize': float(result[0][6]),
                                'current_dl_size': float(result[0][7]),
                                'current_percent_dl': float(result[0][8]),
                                'dl_status': int(result[0][9]),
                                'async': int(result[0][10]),
                                'playAtEnd': int(result[0][11])
                                }
                        xbmc.log("[AdvDownloader] Find element %s success in db" % (item['fileName']), xbmc.LOGINFO)
                        return itemJSON 
                
            except Exception, e:
                print str(e)
                xbmc.log("[AdvDownloader] Error during select execution in db with query : " + sql_select, xbmc.LOGERROR)
        
        return None
        
        
    def _addToQueue(self, fileName, params):       
        
        
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            if self._searchItem(params) is None:
                index = self._getLastIndex() + 1;
                # ___ Insert value (12)
                # queuePosition
                # fileName
                # url
                # title
                # incomplete_path
                # complete_path
                # total_size
                # current_dl_size
                # current_percent_dl
                # dl_status
                # async
                # playAtEnd
                sql_insert = "INSERT INTO AdvDownloader VALUES ( %s, '%s', '%s', '%s', '%s', '%s', %s, %s, %s, %s, %s, %s);" % (index, fileName, params['url'], params['title'], params['incomplete_path'], params['complete_path'], str(params['totalsize']), 0, 0, 0, int(params['async']), int(params['playAtEnd']))
                dbCursor.execute(sql_insert)
                
                try:
                    db.commit() 
                    
                    xbmc.log("[AdvDownloader] Insert success in db", xbmc.LOGINFO)
                except Exception, e:
                    xbmc.log("[AdvDownloader] Error during insertion execution in db with query : " + sql_insert, xbmc.LOGERROR)
    
    def _removeToQueue(self, fileName, params={}):
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            clause_value = "fileName = '%s'" % (fileName)
            
            if 'url' in params:
                clause_value = clause_value + " AND url = '%s'" % (params['url'])
                
            sql_delete = "DELETE FROM AdvDownloader  WHERE %s ;" % (clause_value)
            
            dbCursor.execute(sql_delete)
            try:
                db.commit() 
                
                xbmc.log("[AdvDownloader] Delete success in db", xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("[AdvDownloader] Error during delete execution in db with query : " + sql_delete, xbmc.LOGERROR)

    def _updateQueueItem(self,fileName,params):  
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            clause_value = "fileName = '%s'" % (fileName)
            
            if 'url' in params:
                clause_value = clause_value + " AND url = '%s'" % (params['url'])
                
            sql_update = "UPDATE AdvDownloader SET "
            sql_update = sql_update+" current_dl_size = "+str(params['current_dl_size'])+ ","
            sql_update = sql_update+" current_percent_dl = "+str(params['current_percent_dl'])+ ","
            sql_update = sql_update+" dl_status = "+str(params['dl_status'])
            sql_update = sql_update+" WHERE %s ;" % (clause_value)
            
            dbCursor.execute(sql_update)
            try:
                db.commit() 
                
                xbmc.log("[AdvDownloader] Update success in db", xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("[AdvDownloader] Error during update execution in db with query : " + sql_update, xbmc.LOGERROR)
        
    def _clearQueue(self):
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            sql_delete = "DELETE FROM AdvDownloader;"
            
            dbCursor.execute(sql_delete)
            try:
                db.commit()             
                xbmc.log("[AdvDownloader] Clear success in db", xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("[AdvDownloader] Error during delete execution in db with query : " + sql_delete, xbmc.LOGERROR) 

    
    def __del__(self):        
        # ___ Destroy object
        pass        
        
    def _shouldStop(self):
        """
            Method _shouldStop
            @return True if we ask to stop all downloads, else return False
        """                
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            # ___ Select sql  (12)
            sql_select = "SELECT * from AdvDownloader WHERE dl_status < 3;"
            try:
                dbCursor.execute(sql_select)
                result = dbCursor.fetchall() 
                if len(result) > 0 : 
                    if result[0][0] == None:
                        xbmc.log("[AdvDownloader] No download started in db", xbmc.LOGINFO)
                        return True
                    else:
                        itemJSON = {
                                'queuePosition': result[0][0],
                                'fileName': result[0][1],
                                'url':result[0][2],
                                'title':result[0][3],
                                'destinationFolder':result[0][5],
                                'webBrowserId': 0,
                                'incomplete_path': result[0][4],
                                'complete_path': result[0][5],
                                'totalsize': float(result[0][6]),
                                'current_dl_size': float(result[0][7]),
                                'current_percent_dl': float(result[0][8]),
                                'dl_status': int(result[0][9]),
                                'async': int(result[0][10]),
                                'playAtEnd': int(result[0][11])
                                }
                        xbmc.log("[AdvDownloader] Find element in download", xbmc.LOGINFO)
                        return False 
                
            except Exception, e:
                print str(e)
                xbmc.log("[AdvDownloader] Error during select execution in db with query : " + sql_select, xbmc.LOGERROR)
        
        return True

    def _askStop(self):
        """
            Method _askStop
            Ask to stop all downloads            
        """        
        
        with sqlite.connect(self.__dbFile__) as db:
            dbCursor = db.cursor()
            
            sql_update = "UPDATE AdvDownloader SET dl_status = 3 WHERE dl_status < 3;"            
            dbCursor.execute(sql_update)
            try:
                db.commit()             
                xbmc.log("[AdvDownloader] Stop download - Update success in db", xbmc.LOGINFO)
            except Exception, e:
                xbmc.log("[AdvDownloader] Error during update execution in db with query : " + sql_update, xbmc.LOGERROR)
            
     
    def _setStopFlag(self,shouldStop):
        pass   
               
class CacheQueue(QueueClass):
    """
        Cache queue class
    """
    def __init__(self):
        # Initialize 'cache' variables
        try:
            import StorageServer
        except:
            import storageserverdummy as StorageServer
        self.cache = StorageServer.StorageServer("AdvDownloader")
        
    def _getQueue(self):        
        """
            Method to get the queue
            @return the queue
            
            @attention: Use this method, only for read the queue
        """        
        queue = self.cache.get("AdvDownloaderQueue")
        try:
            items = eval(queue)
        except:
            items = {}

        xbmc.log("[AdvDownloader] _getQueue Done: " + str(len(items)), xbmc.LOGDEBUG)
        return items 
    
    def moveItemToPosition(self, filename, position):
        """
            Method moveItemToPosition
            @param filename: The name of the file
            @param position: The new index of the item in the queue
        """
        if position > 0 and self.cache.lock("AdvDownloaderQueueLock"):
            items = []
            if filename:
                queue = self.cache.get("AdvDownloaderQueue")
                xbmc.log("[AdvDownloader] Queue loaded : " + repr(queue), xbmc.LOGDEBUG)

                if queue:
                    try:
                        items = eval(queue)
                    except:
                        items = []

                    xbmc.log("[AdvDownloader] Pre items: %s " % repr(items), xbmc.LOGDEBUG)
                    
                    # ___ Move item in the position
                    for index, item in enumerate(items):
                        (item_id, item) = item
                        if item_id == filename:
                            del items[index]                            
                            items = items[:position] + [(filename, item)] + items[position:]
                            break
                    
                    # ___ Recalculate queuePosition
                    for index, itemQueue in enumerate(items):      
                        (item_id, item) = itemQueue
                        item['queuePosition'] = index
                        del items[index]                            
                        items = items[:index] + [(item_id, item)] + items[index:]
                        
                    xbmc.log("[AdvDownloader] Post items: %s " % repr(items), xbmc.LOGDEBUG)

                    self.cache.set("AdvDownloaderQueue", repr(items))

                    self.cache.unlock("AdvDownloaderQueueLock")
                    xbmc.log("[AdvDownloader] moveItemToPosition Done", xbmc.LOGDEBUG)
        else:
            xbmc.log("[AdvDownloader] Couldn't lock AdvDownloaderQueueQueueLock in the method _moveItemToPosition", xbmc.LOGDEBUG)
    
    def _getNextItemFromQueue(self):
        """
            _getNextItemFromQueue : Method to get the next item into the queue
            @return the next item in the queue
                    the item has the format : (filename, params)
        """
        
        if self.cache.lock("AdvDownloaderQueueLock"):
            
            # ___ Initialiaze the items array
            items = []
            
            # ___ Get the current queue
            queue = self.cache.get("AdvDownloaderQueue")
            xbmc.log("[AdvDownloader] Queue loaded : " + repr(queue), xbmc.LOGDEBUG)

            if queue:
                try:
                    items = eval(queue)
                except:
                    items = False

                item = {}
                # ___ If the current queue is not empty, we get the next item
                if len(items) > 0:
                    item = items[0]
                    xbmc.log("[AdvDownloader] Returning : " + item[0], xbmc.LOGDEBUG)

                self.cache.unlock("AdvDownloaderQueueLock")
                if item:
                    (fileName, item) = item
                    return item
                else:
                    return False
            else:
                xbmc.log("[AdvDownloader] Couldn't aquire lock on AdvDownloaderQueueLock in the method _getNextItemFromQueue", xbmc.LOGDEBUG)      
        
    def _getLastIndex(self):
        """
            Method to return the last index of the queue
        """
        return len(self._getQueue())        
    
    def _addToQueue(self, fileName, params):       
        """
            Method _addToQueue
            
            @param filename: the name of the file to download
            @param params: the dictionnary with informations about the file to download
        """        
        if self.cache.lock("AdvDownloaderQueueLock"):        
            items = []
            if filename:
                queue = self.cache.get("AdvDownloaderQueue")
                xbmc.log("[AdvDownloader] Queue loaded : " + repr(queue), xbmc.LOGDEBUG)
        
                if queue:
                    try:
                        items = eval(queue)
                    except:
                        items = []
        
                append = True
                # __ Verify if the item is already into the queue
                for index, item in enumerate(items):
                    (item_id, item) = item
                    if item_id == filename:
                        # __ If the item is already into the queue, we will delete it
                        append = False
                        del items[index]
                        break
        
                # __ If we should add the item in the queue
                if append:
                    items.append((filename, params))
                    xbmc.log("[AdvDownloader] Added: " + filename.decode('utf-8') + " to queue - " + str(len(items)).decode('utf-8'), xbmc.LOGDEBUG)
                # __ Else we should insert the item in the head of the queue
                else:
                    items.insert(1, (filename, params))  # 1 or 0?
                    xbmc.log("[AdvDownloader] Moved " + filename.decode('utf-8') + " to front of queue. - " + str(len(items)).decode('utf-8'), xbmc.LOGDEBUG)
                     
                # __ Set the new queue              
                self.cache.set("AdvDownloaderQueue", repr(items))
             
                # __ Unlock the queue
                self.cache.unlock("AdvDownloaderQueueLock")
                xbmc.log("[AdvDownloader] _addItemToQueue Done", xbmc.LOGDEBUG)
        else:            
            xbmc.log("[AdvDownloader] Couldn't lock AdvDownloaderQueueLock on _addItemToQueue", xbmc.LOGERROR)
    
    def _removeToQueue(self, fileName, params={}):
        """
            _removeToQueue Method
            @param fileName :the filename to remove of the download queue
            @param params : All associate parameters 
        """
        if self.cache.lock("AdvDownloaderQueueLock"):
            items = []

            queue = self.cache.get("AdvDownloaderQueue")
            xbmc.log("[AdvDownloader] Queue loaded : " + repr(queue), xbmc.LOGDEBUG)

            if queue:
                try:
                    items = eval(queue)
                except:
                    items = []

                for index, item in enumerate(items):
                    (item_id, item) = item
                    if item_id == filename:
                        self._removeTempFile(filename, item)
                        del items[index]                        
                        self.cache.set("AdvDownloaderQueue", repr(items))
                        xbmc.log("[AdvDownloader] Removed: " + filename.decode('utf-8') + " from queue", xbmc.LOGDEBUG)

                self.cache.unlock("AdvDownloaderQueueLock")
                xbmc.log("[AdvDownloader] Remove item from queue : Done")
            else:
                xbmc.log("[AdvDownloader] Exception in _removeToQueue", xbmc.LOGDEBUG)
        else:            
            xbmc.log("[AdvDownloader] Couldn't lock AdvDownloaderQueueLock on _removeToQueue", xbmc.LOGERROR)

    def _clearQueue(self):
        """
            _clearQueue Method
        """
        if self.cache.lock("AdvDownloaderQueueLock"):
            items = []
            self.cache.set("AdvDownloaderQueue", repr(items))
            xbmc.log("[AdvDownloader] Clear queue successful ", xbmc.LOGDEBUG)
          
        else:            
            xbmc.log("[AdvDownloader] Couldn't lock AdvDownloaderQueueLock on _clearQueue", xbmc.LOGERROR)

    def _shouldStop(self):
        """
            Method _shouldStop
            @return True if we ask to stop all downloads, else return False
            
            @warning: this method read the cache for the value "StopDownloaderQueue"
        """
        shouldStop = False
        
        shouldStopStr = self.cache.get("AdvDownloaderStop")
        
        if shouldStopStr is not None:
            try:
                """
                    @bug: SyntaxError: ('unexpected EOF while parsing', ('<string>', 0, 0, ''))
                    @note : Not use eval(shouldStopStr) to avoid SyntaxError 
                """
                if shouldStopStr == "True" :
                    shouldStop = True      
            except Exception:
                pass  
        return shouldStop

    def _askStop(self):
        """
            Method _askStop
            Ask to stop all downloads
            
            @warning: this method read and set the cache for the value "AdvDownloaderStop"
        """
        shouldStopStr = self.cache.get("AdvDownloaderStop")
        
        """
            @bug: SyntaxError: ('unexpected EOF while parsing', ('<string>', 0, 0, ''))
            @note : Not use eval(shouldStopStr) to avoid SyntaxError
        """
        if shouldStopStr == "False":
            self.cache.set("AdvDownloaderStop", repr(True))   
            
    
    def _setStopFlag(self,shouldStop):
        """
            Method _setStopFlag
            Ask to set the flag AdvDownloaderStop
            
            @warning: this method read and set the cache for the value "AdvDownloaderStop"
        """
        self.cache.set("AdvDownloaderStop", repr(shouldStop))     