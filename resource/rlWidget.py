import sys, scriptEvent
import PySide2
from PySide2 import QtGui, QtCore, QtWidgets

def debugMsg(_str):
    _text = str(_str)
    info_dialog = PySide2.QtWidgets.QMessageBox()
    info_dialog.setWindowTitle('Debug Window')
    info_dialog.setText(_text)
    info_dialog.exec_()

class rlWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(rlWidget, self).__init__(parent=parent)
        self.relatedWidgetList = []
        
    def mouseDoubleClickEvent(self, event):
        super(rlWidget, self).mouseDoubleClickEvent(event)
    
    def hideEvent(self,event):
        super(rlWidget, self).hideEvent(event)
        #debugMsg(self.findChildren(QtWidgets.QWidget, "aaa"))
        '''
        childrenList = self.findChildren(QtWidgets.QWidget)
        for i in range(len(childrenList)):
            childrenList[i].hide()
            #debugMsg(childrenList[i])
        '''
        self.device.stop()
        scriptEvent.StopTimer()
        
        for i in range(len(self.relatedWidgetList)):
            self.relatedWidgetList[i].hide()
        
    def setRelatedWidget(self,widget):
        self.relatedWidgetList.append(widget)

    def setDevice(self,device):
        self.device = device
