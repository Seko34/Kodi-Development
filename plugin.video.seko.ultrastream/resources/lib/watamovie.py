# -*- coding: utf-8 -*-
#---------------------------------------------------------------------
'''
Created on 11 Nov 2016

@author: Seko
@summary: Filmou class

'''
#---------------------------------------------------------------------

# ____________________     I M P O R T       ____________________
import xbmcgui
import xbmc
import re
import urllib
import urllib2
import webUtil
import strUtil
import traceback
import urlresolver
import pyxbmct
import cookielib
import constant
import miscFunctions
import metadata
from BeautifulSoup import BeautifulSoup
import src_mod as sources
from item import StreamItem


# ____________________     C L A S S       ____________________

class Filmou(pyxbmct.AddonDialogWindow):
    """
        Class Filmou
        
        Used for search a movie from watamovie
    """
    
    def __init__(self):
        """
            Constructor
        """
        
        # ___ Init cookiejat & urlOpener
        self.cookiejar = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
    
        # ___ Set the pyxbmct skin to estuary
        if constant.__addon__.getSetting('estuary_watamovie') == 'true':
            pyxbmct.skin.estuary = True
        else:
            pyxbmct.skin.estuary = False
        
        # ___ Call the base class' constructor.
        super(Filmou, self).__init__(constant.__addon__.getLocalizedString(80000))
        
        # ___ Set window width, height and grid resolution
            # ___ Get the current screenresolution
        resolution = xbmc.getInfoLabel('System.ScreenResolution')
        resolutionPattern = re.compile('(.*)(x)(.*)(@)(.*)')
        match  = resolutionPattern.match(resolution)
        xmax = int(match.group(1))
        ymax = int(match.group(3))
            # ___ Calculate the width an height
        xGeometry = int( xmax*0.75)
        yGeometry = int( ymax*0.75)
        xGeometry = min(500,xGeometry)
            # ___ Set the width height and grid
        self.setGeometry(xGeometry, yGeometry, 15, 2)
        
        # ___ Init variable
        self.choices = [constant.__addon__.getLocalizedString(80010),constant.__addon__.getLocalizedString(80011),constant.__addon__.getLocalizedString(80012)]
        
        # ___ Set and add controls to  the window
        self.set_controls()
        # ___ Define the navigation between control
        self.set_navigation()
        
        # Connect Backspace button to close our window.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        
    def set_controls(self):
        """
            Set up UI controls
        """        
        # ___ Init all choice button            
        self.choice1 = None
        self.choice2 = None
        self.choice3 = None
        self.choice4 = None
        self.choice5 = None
        self.choice6 = None
        self.choice7 = None
        self.choice8 = None
        self.choice9 = None
        self.choice10 = None
        self.choiceArray = [
                            self.choice1,
                            self.choice2,
                            self.choice3,
                            self.choice4,
                            self.choice5,
                            self.choice6,
                            self.choice7,
                            self.choice8,
                            self.choice9,
                            self.choice10]
        # __ Filter label
        self.filterArray = [
                        {'title':'Romantique','value':''},
                        {'title':'Violent','value':''},
                        {'title':'Drôle','value':''},
                        {'title':'Action','value':''},
                        {'title':'Scénario orignal','value':''},
                        {'title':'Compliqué','value':''},
                        {'title':'Fait peur','value':''},
                        {'title':'Fin surprenante','value':''},
                        {'title':'Emotions','value':''},
                        {'title':'Populaire','value':''}
                        ]
        
        # ___ Add all radio button to the grid and connect the function 'choice_update'  
            # Romantique
        self.choiceArray[0] = pyxbmct.RadioButton(self.filterArray[0]['title'])
        self.placeControl(self.choiceArray[0], 0, 0, 1, 2)   
        self.connect(self.choiceArray[0], lambda: self.choice_update(0))  
        
            # Violent
        self.choiceArray[1] = pyxbmct.RadioButton(self.filterArray[1]['title'])
        self.placeControl(self.choiceArray[1], 1, 0, 1, 2)   
        self.connect(self.choiceArray[1], lambda: self.choice_update(1))  
        
            # Drôle
        self.choiceArray[2] = pyxbmct.RadioButton(self.filterArray[2]['title'])
        self.placeControl(self.choiceArray[2], 2, 0, 1, 2)   
        self.connect(self.choiceArray[2], lambda: self.choice_update(2))   
        
            # Action
        self.choiceArray[3] = pyxbmct.RadioButton(self.filterArray[3]['title'])
        self.placeControl(self.choiceArray[3], 3, 0, 1, 2)   
        self.connect(self.choiceArray[3], lambda: self.choice_update(3)) 
        
            # Scénario original
        self.choiceArray[4] = pyxbmct.RadioButton(self.filterArray[4]['title'])
        self.placeControl(self.choiceArray[4], 4, 0, 1, 2)   
        self.connect(self.choiceArray[4], lambda: self.choice_update(4))   
        
            # Compliqué
        self.choiceArray[5] = pyxbmct.RadioButton(self.filterArray[5]['title'])
        self.placeControl(self.choiceArray[5], 5, 0, 1, 2)   
        self.connect(self.choiceArray[5], lambda: self.choice_update(5))   
        
            # Fait peur
        self.choiceArray[6] = pyxbmct.RadioButton(self.filterArray[6]['title'])
        self.placeControl(self.choiceArray[6], 6, 0, 1, 2)   
        self.connect(self.choiceArray[6], lambda: self.choice_update(6))   
        
            # Fin surprenante
        self.choiceArray[7] = pyxbmct.RadioButton(self.filterArray[7]['title'])
        self.placeControl(self.choiceArray[7], 7, 0, 1, 2)   
        self.connect(self.choiceArray[7], lambda: self.choice_update(7))   
        
            # Emotions
        self.choiceArray[8] = pyxbmct.RadioButton(self.filterArray[8]['title'])
        self.placeControl(self.choiceArray[8], 8, 0, 1, 2)   
        self.connect(self.choiceArray[8], lambda: self.choice_update(8))  
        
            # Populaire
        self.choiceArray[9] = pyxbmct.RadioButton(self.filterArray[9]['title'])
        self.placeControl(self.choiceArray[9], 9, 0, 1, 2)   
        self.connect(self.choiceArray[9], lambda: self.choice_update(9))   
        
            # Année : De .... à ....
        self.anneeLabel = pyxbmct.Label('Année de sortie')        
        self.placeControl(self.anneeLabel, 10, 0) 
        self.anneeMin =  pyxbmct.Edit('1918')  
        self.placeControl(self.anneeMin, 11, 0) 
        self.anneeMin.setText('1918')       
        self.anneeMax =  pyxbmct.Edit('2016')        
        self.placeControl(self.anneeMax, 11, 1)
        self.anneeMax.setText('2016') 
        
            # Durée : De .. min à  .. min
        self.dureeLabel = pyxbmct.Label('Durée (min)')        
        self.placeControl(self.dureeLabel, 12, 0) 
        self.dureeMin =  pyxbmct.Edit('60')        
        self.placeControl(self.dureeMin, 13, 0) 
        self.dureeMin.setText('60')
        self.dureeMax =  pyxbmct.Edit('300')        
        self.placeControl(self.dureeMax, 13, 1) 
        self.dureeMax.setText('300')
        
        # Search button
        self.search_button = pyxbmct.Button(constant.__addon__.getLocalizedString(80013))
        self.placeControl(self.search_button, 14, 0)
            # Connect search button
        self.connect(self.search_button, self.search)
        
        # Close button
        self.close_button = pyxbmct.Button(constant.__addon__.getLocalizedString(80014))
        self.placeControl(self.close_button, 14, 1)
            # Connect close button
        self.connect(self.close_button, self.close)
        

    def set_navigation(self):
        """
            Set up keyboard/remote navigation between controls.
        """
        
        for index in range(0,10):
            
            self.choiceArray[index].controlRight(self.search_button)
            self.choiceArray[index].controlLeft(self.search_button)
            if index == 0:
                self.choiceArray[index].controlUp(self.dureeMin)
                self.choiceArray[index].controlDown(self.choiceArray[index+1])
            elif index == 9:
                self.choiceArray[index].controlUp(self.choiceArray[index-1])
                self.choiceArray[index].controlDown(self.anneeMin)
            else:
                self.choiceArray[index].controlUp(self.choiceArray[index-1])
                self.choiceArray[index].controlDown(self.choiceArray[index+1])
                
         
        self.anneeMin.controlLeft(self.search_button)
        self.anneeMin.controlRight(self.anneeMax)
        self.anneeMin.controlDown(self.dureeMin)
        self.anneeMin.controlUp(self.choiceArray[9])
        self.anneeMax.controlLeft(self.anneeMin)
        self.anneeMax.controlDown(self.dureeMin)
        
        
        self.dureeMin.controlLeft(self.search_button)
        self.dureeMin.controlRight(self.dureeMax)
        self.dureeMin.controlDown(self.choiceArray[0])
        self.dureeMin.controlUp(self.anneeMin)
        self.dureeMax.controlLeft(self.dureeMin)
        self.dureeMax.controlDown(self.choiceArray[0])
        self.anneeMax.controlUp(self.anneeMin)
        
        self.search_button.controlRight(self.close_button)
        self.search_button.controlLeft(self.choiceArray[0])
        self.close_button.controlLeft(self.search_button)
        self.close_button.controlRight(self.choiceArray[0])
               
        
        # ___ Set initial focus.
        self.setFocus(self.choiceArray[0])
        
                    
    def choice_update(self,index):
        """
            Method called to choice a filter value
        """
        if self.choiceArray[index].isSelected():
            dialog = xbmcgui.Dialog()
            selection = dialog.select('Watamovie - '+self.filterArray[index]['title'], self.choices)
            if selection >= 0 :
                self.choiceArray[index].setLabel(self.filterArray[index]['title']+' - '+self.choices[selection])
                self.filterArray[index]['value'] = self.choices[selection]
        else:
            self.choiceArray[index].setLabel(self.filterArray[index]['title'])
            
    def getPostValue(self,value):
        """
            Method to convert filter value for the post request
            @param value: the selected value
            @return the value for post data
        """
        if value == 'Pas du tout':
            return 'moins'
        if value == 'Moyen':
            return 'neutre'
        if value == 'Beaucoup':
            return 'plus'
    
        return None
            
    def search(self):
        """
            Method to search a movie
        """
        
        post_href = 'http://watamoovie.com/filmou.php'
        data = {'envoi':'Lancer'}
        
        # ___ Init data
        # _ Amour
        if self.choiceArray[0].isSelected():
            data['Amour']='on'
            data['amour']=self.getPostValue(self.filterArray[0]['value'])+'_amour'
        # _ Violence
        if self.choiceArray[1].isSelected():
            data['Violence']='on'
            data['violence']=self.getPostValue(self.filterArray[1]['value'])+'_violence'
        # _ Rire
        if self.choiceArray[2].isSelected():
            data['Rire']='on'
            data['rire']=self.getPostValue(self.filterArray[2]['value'])+'_rire'
        # _ Action
        if self.choiceArray[3].isSelected():
            data['Action']='on'
            data['action']=self.getPostValue(self.filterArray[3]['value'])+'_action'
        # _ Histoire
        if self.choiceArray[4].isSelected():
            data['Histoire']='on'
            data['histoire']=self.getPostValue(self.filterArray[4]['value'])+'_histoire'
        # _ Difficulte
        if self.choiceArray[5].isSelected():
            data['Difficulte']='on'
            data['difficulte']=self.getPostValue(self.filterArray[5]['value'])+'_difficulte'
        # _ Peur
        if self.choiceArray[6].isSelected():
            data['Peur']='on'
            data['peur']=self.getPostValue(self.filterArray[6]['value'])+'_peur'
        # _ Fin
        if self.choiceArray[7].isSelected():
            data['Fin']='on'
            data['fin']=self.getPostValue(self.filterArray[7]['value'])+'_fin'
        # _ Emotion
        if self.choiceArray[8].isSelected():
            data['Emotion']='on'
            data['emotion']=self.getPostValue(self.filterArray[8]['value'])+'_emotion'        
        # _ Popularite
        if self.choiceArray[9].isSelected():
            data['Popularite']='on'
            data['popularite']=self.getPostValue(self.filterArray[9]['value'])+'_popularite'
     
        data['amount']='de '+self.anneeMin.getText()+' à '+self.anneeMax.getText()
        data['amount_duree']='de '+self.dureeMin.getText()+' min à '+self.dureeMax.getText()+' min'
       
            
        # ___ Send request
        request = urllib2.Request(post_href, urllib.urlencode(data), headers=webUtil.HEADER_CFG)
        responseHttp = None   
        try: 
            responseHttp = self.urlOpener.open(request)            
        except:
            traceback.print_exc()
            
        # ___ If request is not None
        if responseHttp is not None:    
                
            # ___ Read the source
            content = responseHttp.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)  
            responseHttp.close()
            
            # ___ Get the title and the thumbnail
            movie = soup.find('div',{'id':'legendefilm'}).find('img')
            img = movie['src']
            title = movie['alt']
            
            # ___ Translate movie title
            google_href = 'https://www.google.fr/search?q='+webUtil.encodeStr(title)
            request = urllib2.Request(google_href, headers=webUtil.HEADER_CFG)
            responseTitle = None 
            try: 
                responseTitle = self.urlOpener.open(request)            
            except:
                traceback.print_exc()
            if responseTitle is not None and responseTitle.getcode() == 200:
                contentTitme = responseTitle.read()
                soupTitle = BeautifulSoup(contentTitme)
                responseTitle.close()
                titleTranslate = soupTitle.find('div',{'class':'kno-ecr-pt kno-fb-ctx'})
                if titleTranslate is not None:
                    title = titleTranslate.text.encode('utf-8')
            
            # ___ Open a dialog to show result
            watamovie = FilmouResults(title,img,data,self)
            watamovie.doModal()
            del watamovie
        
            
            

class FilmouResults(pyxbmct.AddonDialogWindow):
    """
        Class FilmouResults
        AddonDialogWindow to show a result from watamovie
    """
    
    def __init__(self,title,thumbnail,data,parent):
        """
            Constructor
            @param title: the movie title found
            @param thumbnail: the movie's thumbnail
            @param data: the data used with the post request
            @param parent: the parent window
        """
        # ___ Init cookiejar and urlOpener        
        self.cookiejar = cookielib.CookieJar()
        self.urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookiejar))
        
        # ___ Set the pyxbmct window skin to estuary
        if constant.__addon__.getSetting('estuary_watamovie') == 'true':
            pyxbmct.skin.estuary = True
        else:
            pyxbmct.skin.estuary = False
    
        # ___ Call the base class' constructor.
        super(FilmouResults, self).__init__(constant.__addon__.getLocalizedString(80020))
        
        # ___ Init variable
        self.parent = parent
        self.title = title
        self.thumbnail = 'http://watamoovie.com/'+thumbnail
        self.data = data        
        self.parent.close()
        
        # ___ Set window width, height and grid resolution.
        resolution = xbmc.getInfoLabel('System.ScreenResolution')
        resolutionPattern = re.compile('(.*)(x)(.*)(@)(.*)')
        match  = resolutionPattern.match(resolution)
        xmax = int(match.group(1))
        ymax = int(match.group(3))        
        xGeometry = int( xmax*0.75)
        yGeometry = int( ymax*0.75)
        xGeometry = min(500,xGeometry)
        self.setGeometry(xGeometry, yGeometry, 10, 2)
        
        # ___ Set controls
        self.set_controls()
        # ___ Set navigation between controls
        self.set_navigation()
        # Connect Backspace button to close our addon.
        self.connect(pyxbmct.ACTION_NAV_BACK, self.close)
        
    def set_controls(self):
        """
            Set up UI controls
        """
        # __ Movie title
        self.labelTitle = pyxbmct.Label(self.title, alignment=pyxbmct.ALIGN_CENTER)
        self.placeControl(self.labelTitle,0,0,1,2)        
        # ___ Movie thumbnail
        self.thumnailImg = pyxbmct.Image(self.thumbnail, aspectRatio=2)
        self.placeControl(self.thumnailImg,1,0,8,2)
        
        # ___ OK button
        self.ok_button = pyxbmct.Button('OK')
        self.placeControl(self.ok_button, 9, 0)
            # Connect OK button
        self.connect(self.ok_button, self.closePopup)
        
        # ___ Search again button
        self.search_button = pyxbmct.Button(constant.__addon__.getLocalizedString(80021))
        self.placeControl(self.search_button, 9, 1)
            # Connect Search again 
        self.connect(self.search_button, self.searchAgain)
        
        # ___ Set initial focus.
        self.setFocus(self.ok_button)
        
    
    def set_navigation(self):
        """
            Set up keyboard/remote navigation between controls.
        """
        self.ok_button.controlRight(self.search_button)
        self.ok_button.controlLeft(self.search_button)
        self.search_button.controlLeft(self.ok_button)
        self.search_button.controlRight(self.ok_button)
        # Set initial focus.
        self.setFocus(self.ok_button)    
    
    def searchAgain(self):
        """
            Method to search an other movie
        """
        post_href = 'http://watamoovie.com/filmou.php'
        request = urllib2.Request(post_href, urllib.urlencode(self.data), headers=webUtil.HEADER_CFG)
        responseHttp = None   
        try: 
            responseHttp = self.urlOpener.open(request)            
        except:
            traceback.print_exc()
        if responseHttp is not None:    
                
            # ___ Read the source
            content = responseHttp.read()
            # ___ Initialize BeautifulSoup       
            soup = BeautifulSoup(content)  
            responseHttp.close()
            
            # ___ Get the movie title and thumbnail
            movie = soup.find('div',{'id':'legendefilm'}).find('img')
            img = movie['src']
            title = movie['alt']
            
            
            # ___ Translate movie title
            google_href = 'https://www.google.fr/search?q='+webUtil.encodeStr(title)
            request = urllib2.Request(google_href, headers=webUtil.HEADER_CFG)
            responseTitle = None 
            try: 
                responseTitle = self.urlOpener.open(request)            
            except:
                traceback.print_exc()
            if responseTitle is not None and responseTitle.getcode() == 200:
                contentTitme = responseTitle.read()
                soupTitle = BeautifulSoup(contentTitme)
                responseTitle.close()
                titleTranslate = soupTitle.find('div',{'class':'kno-ecr-pt kno-fb-ctx'})
                if titleTranslate is not None:                    
                    title = titleTranslate.text.encode('utf-8')            
            
            self.labelTitle.setLabel(title)
            self.thumnailImg.setImage('http://watamoovie.com/'+img)
            self.title = title
                
    def closePopup(self):
        """
            Method to close the current popup and search link
        """
        
        streamItem = StreamItem(strUtil.remove_special_char(self.title))
        streamItem.setType(StreamItem.TYPE_MOVIE)
        streamItem.setAction(StreamItem.ACTION_MORE_LINKS)
        streamItem.setIconImage(self.thumbnail)
        
        self.close()
        
        progress = xbmcgui.DialogProgress()
        progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70007)) 
        
        listItems = sources.getMoreLinks(constant.__addon__.getSetting('default_stream_src'), streamItem,True)
        for item in listItems:
            item.setMetadata(streamItem.getMetadata())
        
        # ___ Update the list of elements 
        selectItems = []
        if listItems is not None and len(listItems) > 0 :
            if progress is not None:
                progress.update(0,constant.__addon__.getLocalizedString(70008))
            listItems = metadata.getMetadataForList(StreamItem.TYPE_MOVIE, listItems,progress)
        
            
            for index in range(0,len(listItems)):
                item = listItems[index]
                item.regenerateKodiTitle()
                selectItems.append(item.getKodiTitle())
                
        if progress is not None:
            progress.close()
        
        # ___ Display all StreamItem
        dialog = xbmcgui.Dialog()
        result = dialog.select(constant.__addon__.getLocalizedString(80030), selectItems)
        error = False
        while result > -1 or error: 
            result = -1           
            # ___ Resolve url
            playableUrl = False
            progress = xbmcgui.DialogProgress()
            progress.create(constant.__addon__.getLocalizedString(70006),constant.__addon__.getLocalizedString(70009))
            try:
                playableUrl = urlresolver.resolve(listItems[result].getHref())
            except:
                # ___ If the url is not resolved, display link choice again.
                error = True   
                listItems[result].setKOLinkStatus()
                listItems[result].regenerateKodiTitle()
                selectItems[result] = listItems[result].getKodiTitle()
                result = dialog.select(constant.__addon__.getLocalizedString(80030), selectItems)
            progress.close()     

            # ___If the url is resolved, display the the list of possibilities (Open in web browser, Play, Download or Download & Play )
            if playableUrl != False  and isinstance(playableUrl,unicode) :        
                listItems[result].setPlayableUrl(playableUrl)
                miscFunctions.playVideo(listItems[result])
            else:
                # ___ If the url is not resolved, display link choice again.
                error = False                
                listItems[result].setKOLinkStatus()
                listItems[result].regenerateKodiTitle()
                selectItems[result] = listItems[result].getKodiTitle()
                result = dialog.select(constant.__addon__.getLocalizedString(80030), selectItems)