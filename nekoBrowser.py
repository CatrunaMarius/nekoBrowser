import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import  *
import common
import os, shlex, subprocess
from bookmark_manager import Bookmarks_Dialog, Add_Bookmark_Dialog, icon_dir
from import_export import *
 

class WebEngineView(QWebEngineView,QMainWindow,QWebEngineProfile):
  
    tabs = []

    def __init__(self, Main, parent=None):
        super(QWebEngineView, self).__init__(parent)
        self.mainWindow = Main
       
    def createWindow(self, QWebEnginePage_WebWindowType):
   
        self.tab = Tab()
        self.tab.initTab.setCentralWidget(self.tab.initTab.browser)
        self.tabs.append(self.tab.initTab)
        self.mainWindow.addNewTab(self.tab.initTab)     
        self.tab.initTab.browser.page().fullScreenRequested.connect(self.FullscreenRequest)
           
        return self.tab.initTab.browser
    def FullscreenRequest(self, request):

       request.accept()
       if(request.toggleOn()):
         
          self.tab.initTab.browser.setParent(None)
          self.tab.initTab.browser.showFullScreen()

       else:
           
           self.tab.initTab.setCentralWidget(self.tab.initTab.browser)
           self.tab.initTab.browser.showNormal()
           
    



class Ui_MainWindow(QMainWindow):
    #def __init__(self, parent=None):
    def __init__(self, main, parent=None):
        super(Ui_MainWindow,self).__init__(parent)
        self.mainWindow =main
        ###############################################################
        

        self.tbNavigate = QtWidgets.QToolBar()
        self.tbNavigate.setOrientation(QtCore.Qt.Horizontal)
        self.tbNavigate.setObjectName("tbNavigate")
        self.addToolBar(QtCore.Qt.TopToolBarArea, self.tbNavigate)
        self.tbNavigate.setStyleSheet("background-color:#2D2D30")
        self.tbNavigate.setMovable(False)
        
        self.browser=WebEngineView(self.mainWindow)
        
        self.browser.load(QUrl('https://youtube.com'))
    
        self.setCentralWidget(self.browser)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        QWebEngineSettings.globalSettings().setAttribute(QWebEngineSettings.JavascriptEnabled,True)
        self.browser.page().fullScreenRequested.connect(self.FullscreenRequest)
     

       # #############################################################

        #butonul back
        self.actionBack = QtWidgets.QAction("Back")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icone/back.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionBack.setIcon(icon1)
        self.actionBack.setObjectName("actionBack")

        #butonul inaite
        self.actionForward = QtWidgets.QAction("Forward")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icone/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionForward.setIcon(icon2)
        self.actionForward.setObjectName("actionForward")

        

        #butonul refresh
        self.actionRefresh = QtWidgets.QAction("Reload this page")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icone/baseline_refresh_black_18dp.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionRefresh.setIcon(icon4)
        self.actionRefresh.setObjectName("actionRefresh")

        #Butonul home
        self.actionHome = QtWidgets.QAction("Home")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icone/home (1).png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHome.setIcon(icon5)
        self.actionHome.setObjectName("actionHome")
        
        self.actionFileClose = QtWidgets.QAction()
        self.actionFileClose.setObjectName("actionFileClose")

     
        #functinare butonelor pe bara de navigare
        self.tbNavigate.addAction(self.actionBack)
        self.tbNavigate.addAction(self.actionForward)
        self.tbNavigate.addAction(self.actionRefresh)
        self.tbNavigate.addAction(self.actionHome)
        
        
        #self.tbNavigate.addSeparator()
      
        self.actionBack.triggered.connect( self.browser.back)
        self.actionForward.triggered.connect(self.browser.forward)
        self.actionRefresh.triggered.connect(self.browser.reload)
        self.actionHome.triggered.connect(self.navigateHome)
  
#############################################################

          #Sll icon or no-sll
        self.httpsicon = QLabel()
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icone/lock.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        #self.httpsicon.setIcon(icon6)
        self.httpsicon.setObjectName("httpsicon")
        self.tbNavigate.addWidget(self.httpsicon)
       ###############################################
        
    
        self.addressbar =QLineEdit()
        
        #################
        self.addressbar.returnPressed.connect(self.navigate_to_url)
        ##################
        self.tbNavigate.addWidget(self.addressbar)
        self.addressbar.setStyleSheet("color:white")
        #citeste url
        self.browser.urlChanged.connect(self.updateUrlBar)
##############################################################
        self.meniul =QPushButton()
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icone/camera-settings-cogwheel.png"), QtGui.QIcon.Normal,QtGui.QIcon.Off)
        self.meniul.setIcon(icon7)
        self.exitAct =QAction("exit", self)
        self.tbNavigate.addWidget(self.meniul)
        
        self.mainMenu = QMenu()
        self.mainMenu.addAction("red")       
        self.meniul.setMenu(self.mainMenu)
        #self.meniu.triggered.connect(lambda action:print(action.text()))

        self.newWindo =QAction("New Window")
        self.newWindo.triggered.connect(self.new_win)
        self.newWindo.setShortcut("Ctrl+N")
        self.mainMenu.addAction(self.newWindo)
        self.addAction(self.newWindo)

        ##self.tab = Tab()
        ##self.setCentralWidget(self.browser)
        self.newTab =QAction("New Tab")
        self.newTab.triggered.connect(self.addNewTab)
        self.newTab.setShortcut("Ctrl+T")
        self.mainMenu.addAction(self.newTab)
        self.addAction(self.newTab)   

########################################################
        #butonul da a adauga marcaje
       
        #self.tbNavigate.addWidget(Tab.initTab.addbookmarkBtn)
                ############################################################
        #marcaje
  
        self.bookmarks = importBookmarks("bookmarks.txt")
        self.favourites = importFavourites('favourites.txt')



 #butonul da a adauga marcaje
        self.addbookmarkBtn = QToolButton(self)
        self.addbookmarkBtn.setIcon(QIcon(":/add-bookmark.png"))
        self.addbookmarkBtn.setToolTip("Add Bookmark")        
        self.tbNavigate.addWidget(self.addbookmarkBtn)
        self.addbookmarkBtn.clicked.connect(self.addbookmark)

      

                #Butonul cu menegerul de marcaje
        self.bookmarkBtn = QPushButton(QIcon(":/bookmarks.png"), "", self)
        self.bookmarkBtn.setToolTip("Manage Bookmarks\n         [Alt+B]")
        self.bookmarkBtn.setShortcut("Alt+B")
        self.tbNavigate.addWidget(self.bookmarkBtn)
        self.bookmarkBtn.clicked.connect(self.managebookmarks)
        
################ New Function #####################


    def GoTo(self, url):
        URL = QUrl.fromUserInput(url)
        self.browser.load(URL)
        
    
    
     #SALVEAZA IN BARA DE MARCAJE
    def addbookmark(self):
        """ Opens add bookmark dialog and gets url from url box"""
        dialog = QDialog(self)
        addbmkdialog = Add_Bookmark_Dialog()
        addbmkdialog.setupUi(dialog)
        
        ##############################################
         #asta prea titlul pagini
   
        addbmkdialog.titleEdit.setText(self.browser.title())
        
           #asta prea linkul din adresa
        addbmkdialog.addressEdit.setText(self.addressbar.text())
        ###################################
    
        if (dialog.exec_() == QDialog.Accepted):
            url = addbmkdialog.addressEdit.text()
            bmk = [addbmkdialog.titleEdit.text(), url] 
            self.bookmarks = importBookmarks("bookmarks.txt")
            self.bookmarks.insert(0, bmk)
            exportBookmarks("bookmarks.txt", self.bookmarks)

    #AICI ESTE FUNCTIA CARE DESCHIDE MENEGERUL DE MARCAJE 
    def managebookmarks(self):
        """ Opens Bookmarks dialog """
        dialog = QDialog(self)
        bmk_dialog = Bookmarks_Dialog()
        bmk_dialog.setupUi(dialog, self.bookmarks, self.favourites)
       
        bmk_dialog.bookmarks_table.doubleclicked.connect(self.GoTo)

        dialog.exec_()
 

    def updateUrlBar(self, q, browser=None):  

        if q.scheme() == 'https':
            self.httpsicon.setPixmap(QPixmap("icone/ssl.png"))
   
        else:
            self.httpsicon.setPixmap(QPixmap("icone/lock.png"))
        
        self.addressbar.setText(q.toString())
        self.addressbar.setCursorPosition(0) 
###############################################################


    def navigateHome(self):
        
        self.browser.setUrl(QUrl("https://www.youtube.com"))

    def navigate_to_url(self):  
        q = QUrl(self.addressbar.text())
        t=self.addressbar.text()
        if "." not in t:
            t="http://www.google.com/search?q="+t
            self.browser.setUrl(QUrl(t))
        elif q.scheme() == "":
            q.setScheme("https")

            self.browser.setUrl(q)
        else:
            self.browser.setUrl(q)

    def addNewTab(self,main):
        tab =Tab()
        tab.addBlankTab()
        
    #################################################
    #nefunctionala momentan
    def new_win(self,main):
        #windo = Ui_MainWindow(main)
        windo = Tab()
        windo.show() 
    ########################################

    def FullscreenRequest(self, request):
       
       
       request.accept()
       if(request.toggleOn()):
       
          self.browser.setParent(None)
          self.browser.showFullScreen()
         
       else:
     
           self.setCentralWidget(self.browser)
           self.browser.showNormal()
    
        





class Tab(QMainWindow):
    def __init__(self):

        super().__init__()
        self.initTab()
        
        self.setStyleSheet("background-color:#2D2D30")
        self.tabs.setUsesScrollButtons(True)
        self.tabs.currentChanged.connect(self.currentTabChanged)


       

        self.show()
    def initTab(self):

        self.setWindowTitle("Neko")
        self.setWindowIcon(QIcon("icone/cat_A-512.png"))
        self.resize(1200, 800)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setMovable(True)
 
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.closeCurrentTab)
        self.setCentralWidget(self.tabs)
        self.tabs.setStyleSheet("QTabBar::tab {height: 30px;  background: '#2D2D50' } QTabWidget::pane{border: 0 solid bleak;margin: -2px -4px -4px -4 px;}")
        self.tabs.setTabShape(QTabWidget.Triangular)
        self.initTab =Ui_MainWindow(self)
        self.addNewTab(self.initTab)


        self.tabs.setCornerWidget(QToolButton(
                self
                ,
                text="+",
                icon=QIcon.fromTheme("color:white"),
                clicked=lambda: self.addBlankTab()
          
                
            ),corner=Qt.TopLeftCorner)

    
    def addBlankTab(self):
        blankTab = Ui_MainWindow(self)
     
        self.addNewTab(blankTab)
  
    def addNewTab(self,tab):
        i = self.tabs.addTab(tab,"")
        self.tabs.setCurrentIndex(i)

        tab.browser.titleChanged.connect(lambda title: (self.tabs.setTabText(i, title),
                                                        self.tabs.setTabToolTip(i, title)))

    def closeCurrentTab(self,i):
        if self.tabs.count()<1:
            return
        self.tabs.tabCloseRequested.connect(
            lambda index: self.tabs.widget(index).deleteLater())
    
    def currentTabChanged(self, idx):
        if self.tabs.widget(idx) is None:
            return self.close()  

 

app = QtWidgets.QApplication(sys.argv)
ui =Tab()
app.exec_()