from maya import OpenMayaUI as omui
from PySide.QtCore import *
from PySide.QtGui import *
from PySide.QtUiTools import *
from shiboken import wrapInstance
from sys import path as pythonPath
from SkeletonFix import skeletonFix

def getMayaWin():
    #obtain a reference to the maya window
    mayaWinPtr = omui.MQtUtil.mainWindow()
    mayaWin    = wrapInstance(long(mayaWinPtr), QWidget)

def loadUI(uiName):
    """Returns QWidget with the UI"""
    # object to load ui files
    loader = QUiLoader()
    # file name of the ui created in Qt Designer
    # directory name (we will update this until we find the file)
    dirIconShapes = ""
    # buffer to hold the XML we are going to load
    buff = None
    # search in each path of the interpreter
    for p in pythonPath:
        fname = p + '/' + uiName
        uiFile = QFile(fname)
        # if we find the "ui" file
        if uiFile.exists():
            # the directory where the UI file is
            dirIconShapes = p
            uiFile.open(QFile.ReadOnly)
            # create a temporary array so we can tweak the XML file
            buff = QByteArray( uiFile.readAll() )
            uiFile.close()
            # the filepath where the ui file is: p + uiname
            break
    else:
        print 'UI file not found'
    # fix XML
    fixXML(buff, p)
    qbuff = QBuffer()
    qbuff.open(QBuffer.ReadOnly|QBuffer.WriteOnly)
    qbuff.write(buff)
    qbuff.seek(0)
    ui = loader.load(qbuff, parentWidget = getMayaWin())
    ui.path = p
    return ui


def fixXML(qbyteArray, path):
    # first replace forward slashes for backslashes
    if path[-1] != '/':
        path = path + '/'
    path = path.replace("/","\\")
    
    # construct whole new path with <pixmap> at the begining
    tempArr = QByteArray( "<pixmap>" + path + "\\")
    
    # search for the word <pixmap>
    lastPos = qbyteArray.indexOf("<pixmap>", 0)
    while ( lastPos != -1 ):
        qbyteArray.replace(lastPos,len("<pixmap>"), tempArr)
        lastPos = qbyteArray.indexOf("<pixmap>", lastPos+1)
    return 

class UIController(QObject):
    def __init__(self, ui):
        QObject.__init__(self)
        ui.setWindowFlags(ui.windowFlags() | Qt.WindowStaysOnTopHint)
        self.fix = skeletonFix()
        
        # connect each signal to it's slot (handler) one by one
        ui.setMocap.clicked.connect(self.SetMocap)
        ui.mocapAddJoint.clicked.connect(self.AddMocapJoint)
        ui.setTarget.clicked.connect(self.SetTarget)
        ui.targetAddJoint.clicked.connect(self.AddTargetJoint)
        
        ui.reoirentTarget.clicked.connect(self.ReoirentTarget)
        ui.transferAnimation.clicked.connect(self.TransferAnimation)
        ui.removeJoint.clicked.connect(self.RemoveJoint)
        ui.dismiss.clicked.connect(self.Dismiss)
        
        self.ui = ui
        self.ui.show()
        
        self.currentMocapList = []
        self.currentTargetList = []   
        self.shortestList = 0;
        
    def showUI(self):
        self.ui.show()
        
    def hideUI(self):
        self.ui.hide()
        
    # Mocap
    def SetMocap(self):
        mocapList = self.fix.getJointNames()
        for i in range(len(mocapList)):
            mocapList[i] = "%s" % (mocapList[i])
            self.ui.mocapList.addItem(mocapList[i])
        self.UpdateCount()
        
    def AddMocapJoint(self):
        mocapList = self.fix.getJointSelection()
        for i in range(len(mocapList)):
            mocapList[i] = "%s" % (mocapList[i])
            self.ui.mocapList.addItem(mocapList[i])
        self.UpdateCount()
        
    # Target
    def SetTarget(self):
        targetList = self.fix.getJointNames()
        for i in range(len(targetList)):
            targetList[i] = "%s" % (targetList[i])
            self.ui.targetList.addItem(targetList[i])
        self.UpdateCount()
        
    def AddTargetJoint(self):
        targetList = self.fix.getJointSelection()
        for i in range(len(targetList)):
            targetList[i] = "%s" % (targetList[i])
            self.ui.targetList.addItem(targetList[i])
        self.UpdateCount()
            
    # Other
    def ReoirentTarget(self):
        listLength = self.GetLists()
        self.fix.reorient(self.currentMocapList, self.currentTargetList, listLength)        
        
    def TransferAnimation(self):
        listLength = self.GetLists()
        self.fix.transfere(self.currentMocapList, self.currentTargetList, listLength)
        
    def RemoveJoint(self):
        for selectedItem in self.ui.targetList.selectedItems():
            self.ui.targetList.takeItem(self.ui.targetList.row(selectedItem))
        for selectedItem in self.ui.mocapList.selectedItems():
            self.ui.mocapList.takeItem(self.ui.mocapList.row(selectedItem))
        self.UpdateCount()
        
    def GetLists(self):
        listLength = min(self.ui.mocapList.count(), self.ui.targetList.count())
        for i in range(listLength):  
            self.currentMocapList.append(self.ui.mocapList.item(i).text())
            self.currentTargetList.append(self.ui.targetList.item(i).text())
        return listLength
            
    def UpdateCount(self):
        self.ui.mocapJointCount.setText("Joint\nCount: " + str(self.ui.mocapList.count()))
        self.ui.targetJointCount.setText("Joint\nCount: " + str(self.ui.targetList.count()))
        
    def Dismiss(self):
        self.ui.close()
        

        
 
            
    

# usage example from Maya window
##reload(loadXMLUI)
##from loadXMLUI import *
##UIController is loadXMLUI.UIController
##cont = UIController(loadUI('iconshapes.ui'))