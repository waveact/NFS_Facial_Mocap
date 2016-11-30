import script, scriptEvent, socket, sys, os, struct, PySide2, imp, Queue
from PySide2 import QtGui
from PySide2.QtWidgets import QWidget
from PySide2 import shiboken2
from PySide2 import QtCore
from PySide2.QtWidgets import QWidget
from PySide2.QtUiTools import QUiLoader
from PySide2.shiboken2 import wrapInstance 

from PySide2.QtCore import QThread
from PySide2 import QtGui
from PySide2 import QtCore

from PySide2.QtWidgets import *

import os.path

#import rlWidget


import json, math, random

ExcuteParentPath = os.path.abspath(os.path.join(sys.executable, os.pardir))
ResPath = ExcuteParentPath + "\FM2"
sys.path.insert(0, ResPath) # or sys.path.append('/path/to/application/app/folder')

mainUI = ResPath + "\\resource\FM_mainWindow.ui"
mappingUI = ResPath + "\\resource\FM_mapping.ui"
dataSourceUI = ResPath + "\\resource\FM_dataSource.ui"
dataSmoothUI = ResPath + "\\resource\FM_smooth.ui"
dataRangeUI = ResPath + "\\resource\FM_range.ui"

#import VerticalSliderSpinner
#import rlWidget
from resource.smooth import *
import resource.rlWidget
import resource.VerticalSliderSpinner
#from resource import rlWidget
reload(resource.rlWidget)
reload(resource.VerticalSliderSpinner)

from resource.VerticalSliderSpinner import VerticalSliderSpinner

globalStrength = 100

tempData = []
#sgFilterContainer = [tempData,tempData,tempData,tempData,tempData,tempData,tempData,tempData,tempData,tempData]
smoothFilterContainer = []

'''
import rlSlider
reload(rlSlider)
'''

##########################
## GLOBAL VARIABLES 
##########################

rlSliderRegularContainer = []
rlSliderCustomContainer = []
rlSliderEyeLContainer = []
rlSliderEyeRContainer = []
rlSliderHeadContainer = []
rlSliderBoneContainer = []

device = None

testBool = False

oldToNew = [1,2,3,4,5,6,7,8,33,34,35,27,32,9,10,12,13,14,15,17,18,21,22,24,25,26,31,11,16,19,20,23,28,29,30,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]

facewareList = [ "01.mouth_rightMouth_stretch", "02.mouth_leftMouth_narrow", "03.mouth_up", "04.mouth_leftMouth_stretch", "05.mouth_rightMouth_narrow", "06.mouth_down", "07.mouth_upperLip_left_up", "08.mouth_upperLip_right_up", "09.mouth_lowerLip_left_down", "10.mouth_lowerLip_right_down", "11.mouth_leftMouth_frown", "12.mouth_rightMouth_frown", "13.mouth_leftMouth_smile", "14.mouth_rightMouth_smile", "15.eyes_lookRight", "16.eyes_lookLeft", "17.eyes_lookDown", "18.eyes_lookUp", "19.eyes_leftEye_blink", "20.eyes_rightEye_blink", "21.eyes_leftEye_wide", "22.eyes_rightEye_wide", "23.brows_leftBrow_up", "24.brows_leftBrow_down", "25.brows_rightBrow_up", "26.brows_rightBrow_down", "27.brows_midBrows_up", "28.brows_midBrows_down", "29.jaw_open", "30.jaw_left", "31.jaw_right", "32.mouth_phoneme_oh_q", "33.mouth_right", "34.mouth_left", "35.mouth_phoneme_mbp", "36.mouth_phoneme_ch", "37.mouth_phoneme_fv", "38.head_up", "39.head_down", "40.head_left", "41.head_right", "42.head_LeftTilt", "43.head_RightTilt" ]

#brow 1~8
#eye 9~15
#nose 16~20
#mouth and cheek 21~60

feRegularList = [ "01.Brow Raise Inner L", "02.Brow Raise Inner R", "03.", "04.", "05.Brow Drop L", "06.Brow Drop R", "07.Brow Raise L", "08.Brow Raise R", "09.", "10.Eye Blink L", "11.Eye Blink R", "12.Eye Wide L", "13.Eye Wide R", "14.Eye Squint L", "15.Eye Squint R", "16.Nose Scrunch", "17.Nose Flanks Raise", "18.Nose Flank Raise L", "19.Nose Flank Raise R", "20.Nose Nostrils Flare", "21.Cheek Raise L", "22.Cheek Raise R", "23.Cheeks Suck", "24.", "25.", "26.", "27.Mouth Smile L", "28.Mouth Smile R", "29.Mouth Frown", "30.Mouth Frown L", "31.Mouth Frown R", "32.", "33.Mouth Pucker", "34.Mouth Pucker Open", "35.Mouth Widen", "36.", "37.Mouth Dimple L", "38.Mouth Dimple R", "39.Mouth Plosive", "40.", "41.", "42.", "43.", "44.Mouth Bottom Lip Down", "45.Mouth Top Lip Up", "46.Mouth Top Lip Under", "47.", "48.Mouth Snarl Upper L", "49.Mouth Snarl Upper R", "50.Mouth Snarl Lower L", "51.Mouth Snarl Lower R", "52.Mouth Bottom Lip Bite", "53.Mouth Down", "54.Mouth Up", "55.Mouth L", "56.Mouth R", "57.Mouth Lips Jaw Adjust", "58.Mouth Bottom Lip Trans", "59.Mouth Skewer", "60.Mouth Open" ]

feCustomList = [ "01.xx", "02.xx", "03.xx", "04.xx", "05xx.", "06.xx", "07.xx", "08.xx", "09.xx", "10.xx", "11.xx", "12.xx", "13.xx", "14.xx", "15.xx", "16.xx", "17.xx", "18.xx", "19.xx", "20.xx", "21.xx", "22.xx", "23.xx", "24.xx" ]

feEyeL = ["rightLeft_l", "downUp_l"]

feEyeR = ["rightLeft_r", "downUp_r"]

#[head_up_down,head_right_left,head_tilt]
feHead = ["head_up_down", "head_right_left", "head_tilt"]
#7:JawRotateY, 8:JawRotateZ, 9:JawRotateX 10:JawMoveX, 11:JawMoveY, 12:JawMoveZ
#feBone = ["01", "02", "03", "04", "05", "06", "07.JawRotateY", "08.JawRotateZ", "09.JawRotateX", "10.JawMoveX", "11.JawMoveY", "12.JawMoveZ"]
feBone = ["07.JawRotateY", "08.JawRotateZ", "09.JawRotateX", "10.JawMoveX", "11.JawMoveY", "12.JawMoveZ"]

feRegularData = []
for i in range(0,60): 
    feRegularData.append(0.0)
    
feCustomData = []
for i in range(0,24): 
    feCustomData.append(0.0)

feEyeLData = []
for i in range(0,2): 
    feEyeLData.append(0.0)
    
feEyeRData = []
for i in range(0,2): 
    feEyeRData.append(0.0)

feHeadData = []
for i in range(0,3): 
    feHeadData.append(0.0)
    
feBoneData = []
for i in range(0,6): 
    feBoneData.append(0.0)


sourceData = []
#VerticalSliderSpinner = reload(VerticalSliderSpinner)

##########################
## CLASSES 
##########################

class CacheBuffer():
    def __init__(self):
        self.queue = Queue.Queue(maxsize = 10)
        self.lock = False
        
    def setData( self, dataX ):
        if self.queue.qsize() == 10:
            return
        while self.lock == True:
            pass
        self.lock = True
        print 'setData'
        self.queue.put(dataX)
        print self.queue.qsize()
        self.lock = False
        
    def getData(self):
        if self.queue.qsize() == 0:
            return None
        self.lock = True
        while self.queue.qsize() != 0:
            data = self.queue.get()
        self.lock = False
        return data
        
streamCacheBuf = CacheBuffer()
        
class DataThread(QThread):
    def __init__(self,subData,parent=None):
        QThread.__init__(self,parent)
        self.subData = subData
    
    def __del__(self):
        self.quit()
        self.wait()
    
    def run(self):
        while True:
            self.subData.streamCacheBuffer.setData( self.subData.sock.recv(64*1024) )
            #self.subData.loop()
        #self.sleep(0)

class Faceware():

    def __init__(self, *args, **kwargs):
        global facewareList
        self.sock = None
        self.thread = None
        self.serverExiting = False
        
    def run(self):
        global streamCacheBuf
        if self.sock != None:
            self.streamData = self.sock.recv(64*1024)
            streamCacheBuf.setData( self.streamData )
    
    def start(self):
        self.count = 0
        self.bool = True
        if self.sock == None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            facewareSock_server_address = ('127.0.0.1', 802)
            #facewareSock_server_address = ('10.10.10.184', 802)
            self.sock.settimeout(5)
            try:
                self.streamCacheBuffer = CacheBuffer()
                self.sock.connect(facewareSock_server_address)
                self.thread = DataThread(self)
                self.thread.start()
                self.loop()
                if self.serverExiting == False:
                    self.serverExiting = True
            except socket.timeout:
                self.serverExiting = False
        
    def stop(self):
        #print "stop"
        self.count = 0
        if ( self.thread != None ):
            #print "thread is" + str(self.thread.isRunning())
            self.thread.terminate()
            self.thread.wait()
            #print "thread is " + str(self.thread.isRunning())
            self.thread = None
        if ( self.sock != None ):
            self.sock.close()
            self.sock = None
        self.serverExiting = False
    
    def loop(self):
        received = self.streamCacheBuffer.getData()
        if (received != None):
            self.extractData(received)
    
    def extractData(self, received):
        try:
            reciv=received[0]+received[1]+received[2]+received[3]
        except:
            stop()
            debugMsg("disconnect")
        blockSize = struct.unpack('i', reciv)[0]
        
        if (len(received)) >= blockSize:
            dataType = "i"
            for i in range(len(received)-4, 0, -1):
                dataType = dataType+"c"
            dataStream = struct.unpack(dataType, received)
            data = ""
            for i in range(1, blockSize, 1):
                data = data + dataStream[i]
            data = data + "}"
            decodejson = json.loads(data)
            self.analystData(data)
    
    
    def renameKeys(self,iterable):
        if type(iterable) is dict:
            for key in iterable.keys():
                iterable[key.lower()] = iterable.pop(key)
                if type(iterable[key.lower()]) is dict or type(iterable[key.lower()]) is list:
                    iterable[key.lower()] = renameKeys(iterable[key.lower()])
        elif type(iterable) is list:
            for item in iterable:
                item = renameKeys(item)
        return iterable
    
    def analystData(self,_json):
        print "analystData"
        
        global globalStrength
        
        packer = struct.Struct('iifffffffffffffffffffffffffffffffffffffffffffffffff')
        bufferSize = struct.calcsize('iifffffffffffffffffffffffffffffffffffffffffffffffff')
        
        decodejson = json.loads(_json)
        dataFromFaceware = decodejson["animationValues"]
        
        self.value = []
        
        dataFromFaceware = self.renameKeys(dataFromFaceware)
        
        temp = []
        
        global sourceData
        '''
        for i in range(len(sourceData)):
            #debugMsg(sourceData[i])
            #debugMsg(sourceData[i]["id"])
            tempName = sourceData[i].name.lower()
            data_name = (tempName.split(".")[1]).lower()
            try:
                #data_name = (name.split(".")[1]).lower()
                #debugMsg(dataFromFaceware[dataSource["id"].lower()])
                #dataFromFaceware[data_name] = dataFromFaceware[data_name]*sourceData[i].container.multiplyValue*globalStrength/100
                dataFromFaceware[data_name] = dataFromFaceware[data_name]
                #debugMsg(dataFromFaceware[dataSource["id"].lower()])
            except:
                None
        '''
        
        #smoothFilterContainer.pop(0);
        #smoothFilterContainer.append(dataFromFaceware);

        for name in facewareList:
            data_name = (name.split(".")[1]).lower()
            try:
                #debugMsg(data_name)
                self.value.append(dataFromFaceware[data_name])
                #self.value.append(0)
            except:
                self.value.append(0)
        
        #self.value[1] = 100
        '''
        global testBool
        if (testBool==False):
            debugMsg(dataFromFaceware)
            testBool = True
        '''
        #debugMsg(dataFromFaceware)
        global data

        #debugMsg(data)
        
        iCloneRegularData = []
        iCloneCustomData = []
        iCloneEyeRData = []
        iCloneEyeLData = []
        iCloneBoneData = []
        iCloneHeadData = []
        
        for i in range (60):
            iCloneRegularData.append(0)
        for i in range (24):
            iCloneCustomData.append(0)
        for i in range (2):
            iCloneEyeRData.append(0)
        for i in range (2):
            iCloneEyeLData.append(0)
        for i in range (12):
            iCloneBoneData.append(0)
        for i in range (3):
            iCloneHeadData.append(0)
        
        #data.reverse()
        #debugMsg(data)
        
        #brow 1~8
        #eye 9~15
        #nose 16~20
        #mouth and cheek 21~60
        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"] == facewareList[i] ):
                    for k in range(len(data[j]["feRegularData"])):
                        iCloneRegularData[k] = iCloneRegularData[k] + (data[j]["feRegularData"][k]*self.value[i])
                        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"] == facewareList[i] ):
                    for k in range(len(data[j]["feCustomData"])):
                        iCloneCustomData[k] = iCloneCustomData[k] + (data[j]["feCustomData"][k]*self.value[i])
        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"] == facewareList[i] ):
                    for k in range(len(data[j]["feBoneData"])):
                        iCloneBoneData[k+6] = iCloneBoneData[k+6] + (data[j]["feBoneData"][k]*self.value[i])
                        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"] == facewareList[i] ):
                    for k in range(len(data[j]["feEyeLData"])):
                        iCloneEyeLData[k] = iCloneEyeLData[k] + (data[j]["feEyeLData"][k]*self.value[i])
                        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"] == facewareList[i] ):
                    for k in range(len(data[j]["feEyeRData"])):
                        iCloneEyeRData[k] = iCloneEyeRData[k] + (data[j]["feEyeRData"][k]*self.value[i])
                        
        for i in range(len(facewareList)):
            for j in range(len(data)):
                if ( data[j]["id"].lower() == facewareList[i].lower() ):
                    for k in range(len(data[j]["feHeadData"])):
                        if ( data[j]["feHeadData"][k]):
                            iCloneHeadData[k] = iCloneHeadData[k] + ((data[j]["feHeadData"][k])*self.value[i])
        
        #strength
        for i in range(len(iCloneRegularData)):
            global oldToNew
            #oldToNew = [1,2,3,4,5,6,7,8,
            #33,34,35,27,32,9,10,12,13,14,15,17,18,21,22,24,25,26,31,11,16,19,20,23,28,29,30,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
            #brow 1~8
            #eye 9~15
            #nose 16~20
            #mouth and cheek 21~60
            if ( i >=0 and i <= 7 ):
                iCloneRegularData[oldToNew[i]-1] = iCloneRegularData[oldToNew[i]-1]*fmMainUi.qtBrowStrengthSlider.value()/100
            
            if ( i >=8 and i <= 14 ):
                iCloneRegularData[oldToNew[i]-1] = iCloneRegularData[oldToNew[i]-1]*fmMainUi.qtEyeStrengthSlider.value()/100
                
            if ( i >=15 and i <= 19 ):
                None
                #iCloneRegularData[i] = iCloneRegularData[i]*fmMainUi.qtEyeStrengthSlider.value()/100
                
            if ( i >=20 and i <= 59 ):
                iCloneRegularData[oldToNew[i]-1] = iCloneRegularData[oldToNew[i]-1]*fmMainUi.qtMouthStrengthSlider.value()/100
        
        for i in range(len(iCloneBoneData)):
            iCloneBoneData[i] = iCloneBoneData[i]*fmMainUi.qtMouthStrengthSlider.value()/100
            
        for i in range(len(iCloneHeadData)):
            iCloneHeadData[i] = iCloneHeadData[i]*fmMainUi.qtHeadStrengthSlider.value()/100
        
        for i in range(len(iCloneBoneData)):
            iCloneBoneData[i] = iCloneBoneData[i]*fmMainUi.qtMouthStrengthSlider.value()/100
            
        for i in range(len(iCloneHeadData)):
            iCloneHeadData[i] = iCloneHeadData[i]*fmMainUi.qtHeadStrengthSlider.value()/100
        
        
        #smooth
        global smoothFilterContainer
        if ( len(smoothFilterContainer) < 20 ):
            smoothFilterContainer.append([iCloneRegularData,iCloneBoneData,iCloneHeadData])
        else:
            smoothFilterContainer.pop(0)
            smoothFilterContainer.append([iCloneRegularData,iCloneBoneData,iCloneHeadData])
        
        if ( len(smoothFilterContainer) == 20 ):
            
            for i in range(len(iCloneRegularData)):
                global oldToNew
                newIndex = oldToNew[i]-1
                temp = []
                for j in range(len(smoothFilterContainer)):
                    temp.append(smoothFilterContainer[j][0][newIndex])
                
                if ( i >=0 and i <= 7 ):
                    smoothData = smoothList(temp,fmMainUi.qtBrowSmoothSlider.value())
                    iCloneRegularData[newIndex] = smoothData[len(smoothData)-1]
                if ( i >=8 and i <= 14 ):
                    smoothData = smoothList(temp,fmMainUi.qtEyeSmoothSlider.value())
                    iCloneRegularData[newIndex] = smoothData[len(smoothData)-1]
                if ( i >=15 and i <= 19 ):
                    None
                if ( i >=20 and i <= 59 ):
                    smoothData = smoothList(temp,fmMainUi.qtMouthSmoothSlider.value())
                    iCloneRegularData[newIndex] = smoothData[len(smoothData)-1]
                    
            for i in range(len(iCloneBoneData)):
                temp = []
                for j in range(len(smoothFilterContainer)):
                    temp.append(smoothFilterContainer[j][1][i])
                smoothData = smoothList(temp,fmMainUi.qtMouthSmoothSlider.value())
                iCloneBoneData[i] = smoothData[len(smoothData)-1]
                
            for i in range(len(iCloneHeadData)):
                temp = []
                for j in range(len(smoothFilterContainer)):
                    temp.append(smoothFilterContainer[j][2][i])
                smoothData = smoothList(temp,fmMainUi.qtHeadSmoothSlider.value())
                iCloneHeadData[i] = smoothData[len(smoothData)-1]
        
        #tag = True
        if (self.bool):
            #debugMsg(iCloneRegularData)
            self.bool = False
        
        global sourceData
        for i in range(len(sourceData)):
            #sourceData[i].container.setValue(self.value[i])
            data_name = ((sourceData[i].name).split(".")[1]).lower()
            #debugMsg(data_name)
            #debugMsg(dataFromFaceware[data_name])
            try:
                sourceData[i].container.setValue(dataFromFaceware[data_name]*100)
            except:
                None
        
        script.SetFacePuppetKeyWithName( script.GetPickedObjectName(),script.ConvertTimeToFrame(script.GetCurrentTimeScript()),iCloneHeadData,iCloneEyeLData,iCloneEyeRData,iCloneBoneData,iCloneRegularData,iCloneCustomData )
        #script.SetFacePuppetKeyWithName( script.GetPickedObjectName(),0,iCloneHeadData,iCloneEyeLData,iCloneEyeRData,iCloneBoneData,iCloneRegularData,iCloneCustomData )

class DataSourceID:
    def __init__(self, name, id, parentWidget, multiplyValue = 1 ):
        self.name = name
        self.id = id
        self.multiplyValue = multiplyValue
        self.parentWidget = parentWidget

        self.container = VerticalSliderSpinner(self,self.name,-90,80, 70, 100, 0, smooth = True, mute = True, range = True, multiply = True)
        self.container.setMultiplyValue(self.multiplyValue)
        #hboxLayout = PySide2.QtWidgets.QVBoxLayout()
        #self.container.setLayout( hboxLayout )
        self.parentWidget.layout().addWidget(self.container)
        
        #self.container.smoothButton.clicked(self.onSmoothClicked)
        #self.container.rangeButton.clicked(self.onRangeClicked)
    
    def onSmoothClicked(self):
        None
        '''
        global dataSmoothUI
        dataSmoothUI.show()
        '''
        
    def onRangeClicked(self):
        None
        '''
        global dataRangeUI
        dataRangeUI.show()
        '''
        
    def onValueChanged(self,value):
        None
    
    
class FacialID:
    def __init__(self, name, id, parentWidget, type ):
        self.name = name
        self.id = id
        #self.type = type
        self.type = type

        self.parentWidget = parentWidget

        self.container = VerticalSliderSpinner(self,self.name,-90, 25, 50, 200, -200 )
        #hboxLayout = PySide2.QtWidgets.QVBoxLayout()
        #self.container.setLayout( hboxLayout )
        self.parentWidget.layout().addWidget(self.container)
        
        #self.container.mouseDoubleClickEvent.connect(self.onMouseDoubleClick)
        #self.container.connect(self.container, SIGNAL('doubleClicked()'), self.onMouseDoubleClick)
    
    def valueNormalize(self,table):
        for i in range(len(table)):
            table[i] = table[i]/100.0
    
    def onValueChanged(self,value):
        #debugMsg(value)
        global data

        #debugMsg(fmMappingUi.qtExpressionComboBox.currentIndex())
        if (self.type == "feRegularData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feRegularData"][self.id] = value/100.0
            
        elif (self.type == "feCustomData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feCustomData"][self.id] = value/100.0
            
        elif (self.type == "feBoneData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feBoneData"][self.id] = value/100.0
            
        elif (self.type == "feEyeLData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeLData"][self.id] = value/100.0
            
        elif (self.type == "feEyeRData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeRData"][self.id] = value/100.0
            
        elif (self.type == "feHeadData"):
            data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feHeadData"][self.id] = value/100.0
            
        else:
            None
        
        feRegularData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feRegularData"]
        feCustomData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feCustomData"]
        feBoneData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feBoneData"]
        feEyeLData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeLData"]
        feEyeRData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeRData"]
        feHeadData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feHeadData"]
        
        #debugMsg(feRegularData)
        script.SetFacePuppetKeyWithName( script.GetPickedObjectName(),0,feHeadData,feEyeLData,feEyeRData,[0,0,0,0,0,0,feBoneData[0],feBoneData[1],feBoneData[2],feBoneData[3],feBoneData[4],feBoneData[5]],feRegularData,feCustomData )
        #debugMsg(feRegularData)
        
##########################
## FUNCTION
##########################

def debugMsg(_str):
    _text = str(_str)
    info_dialog = PySide2.QtWidgets.QMessageBox()
    info_dialog.setWindowTitle('Debug Window')
    info_dialog.setText(_text)
    info_dialog.exec_()

def toJson(serialized):
    """Return JSON string from given native Python datatypes."""
    return json.dumps(serialized, encoding="utf-8", indent=4)


def fromJson(jsonString):
    """Return native Python datatypes from JSON string."""
    return json.loads(jsonString, encoding="utf-8")
    
def openMappingDlg():
    fmMappingUi.show()
    feRegularData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feRegularData"]
    feCustomData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feCustomData"]
    feBoneData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feBoneData"]
    feEyeLData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeLData"]
    feEyeRData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feEyeRData"]
    feHeadData = data[fmMappingUi.qtExpressionComboBox.currentIndex()]["feHeadData"]
    script.SetFacePuppetKeyWithName( script.GetPickedObjectName(),0,feHeadData,feEyeLData,feEyeRData,[0,0,0,0,0,0,feBoneData[0],feBoneData[1],feBoneData[2],feBoneData[3],feBoneData[4],feBoneData[5]],feRegularData,feCustomData )
    #fmMappingUi.hide()

def zeroAll():
    for i in range(len(rlSliderRegularContainer)):
        rlSliderRegularContainer[i].container.setValue(0)
    for i in range(len(rlSliderCustomContainer)):
        rlSliderCustomContainer[i].container.setValue(0)
    for i in range(len(rlSliderEyeLContainer)):
        rlSliderEyeLContainer[i].container.setValue(0)
    for i in range(len(rlSliderEyeRContainer)):
        rlSliderEyeRContainer[i].container.setValue(0)
    for i in range(len(rlSliderHeadContainer)):
        rlSliderHeadContainer[i].container.setValue(0)
    for i in range(len(rlSliderBoneContainer)):
        rlSliderBoneContainer[i].container.setValue(0)

data = []

def initDataStructure():
    global data
    data = []
    for i in range(len(facewareList)):
        tempData = {
            "id":facewareList[i],
            "feRegularData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "feCustomData": [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
            "feBoneData": [0,0,0,0,0,0],
            "feEyeLData": [0,0],
            "feEyeRData": [0,0],
            "feHeadData": [0,0,0],
        }
        data.append(tempData)
    #debugMsg(data[0]["feRegularData"])
    
initDataStructure()
    
def setData():
    global data
    for i in range(len(facewareList)):
        if (data[i]["id"] == fmMappingUi.qtExpressionComboBox.currentText()):
            #debugMsg(data[i]["id"])
            data[i]["feRegularData"] = feRegularData
            data[i]["feCustomData"] = feCustomData
            data[i]["feBoneData"] = feBoneData
            data[i]["feEyeLData"] = feEyeLData
            data[i]["feEyeRData"] = feEyeRData
            data[i]["feHeadData"] = feHeadData
            break
    #debugMsg(id)
    #data[id]
    
def saveData():
    filePath, _ = PySide2.QtWidgets.QFileDialog.getSaveFileName(
                None,
                "Save Scene to JSON",
                os.path.join(QtCore.QDir.homePath(), "mapping_data.json"),
                "JSON File (*.json)"
            )
    if filePath:
        global data
        global sourceData
        #debugMsg(data)
        with open(filePath, "w") as f:
            #f.write(toJson(data) + "\n")
            for source in sourceData:
                temp = {}
                temp["id"] = source.name
                temp["strength"] = source.container.multiplyValue
                data.append(temp)
                #temp[source.name]["strength"] = source.container.multiplyValue
            #f.write(toJson(temp) + "\n")
            #totalData = data + temp
            f.write(toJson(data) + "\n")
            
            
def loadDefaultData():
    filePath = ResPath + "\\resource\default_mapping_data.json"
    if filePath:
        fileData = []
        with open(filePath) as f:
            fileData = (fromJson(f.read()))
        #debugMsg(fileData)
        global data
        data = fileData
        changeData()
        #debugMsg(data)
            
def loadData():
    filePath, _ = PySide2.QtWidgets.QFileDialog.getOpenFileName(
                None,
                "Open Scene JSON File",
                os.path.join(QtCore.QDir.homePath(), "mapping_data.json"),
                "JSON File (*.json)"
            )
    if filePath:
        fileData = []
        with open(filePath) as f:
            fileData = (fromJson(f.read()))
        #debugMsg(fileData)
        global data
        data = fileData
        changeData()

def showSlider():
    if (fmMappingUi.qtShowAllSliderCheckBox.checkState()):
        for i in range (len(rlSliderRegularContainer)):
            temp = rlSliderRegularContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        for i in range (len(rlSliderCustomContainer)):
            temp = rlSliderCustomContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        for i in range (len(rlSliderBoneContainer)):
            temp = rlSliderBoneContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        for i in range (len(rlSliderEyeLContainer)):
            temp = rlSliderEyeLContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        for i in range (len(rlSliderEyeRContainer)):
            temp = rlSliderEyeRContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        for i in range (len(rlSliderHeadContainer)):
            temp = rlSliderHeadContainer[i].container
            if (temp.value == 0):
                temp.hide()
            else:
                temp.show()
        '''
        rlSliderCustomContainer = []
        rlSliderEyeLContainer = []
        rlSliderEyeRContainer = []
        rlSliderHeadContainer = []
        rlSliderBoneContainer = []
        '''
        #setMaximumSize(0,0)
        #debugMsg("True")
    else:
        #debugMsg("False")
        for i in range (len(rlSliderRegularContainer)):
            temp = rlSliderRegularContainer[i].container
            if (temp.value == 0):
                temp.show()
        for i in range (len(rlSliderCustomContainer)):
            temp = rlSliderCustomContainer[i].container
            if (temp.value == 0):
                temp.show()
        for i in range (len(rlSliderBoneContainer)):
            temp = rlSliderBoneContainer[i].container
            if (temp.value == 0):
                temp.show()
        for i in range (len(rlSliderEyeLContainer)):
            temp = rlSliderEyeLContainer[i].container
            if (temp.value == 0):
                temp.show()
        for i in range (len(rlSliderEyeRContainer)):
            temp = rlSliderEyeRContainer[i].container
            if (temp.value == 0):
                temp.show()
        for i in range (len(rlSliderHeadContainer)):
            temp = rlSliderHeadContainer[i].container
            if (temp.value == 0):
                temp.show()
         
    
def changeData():
    #showSlider()
    global data
    #debugMsg(fmMappingUi.qtExpressionComboBox.currentText())
    #debugMsg(data[0]["feRegularData"])
    for i in range(len(facewareList)):
        if (data[i]["id"] == fmMappingUi.qtExpressionComboBox.currentText()):
            #debugMsg(data[i]["id"])
            #debugMsg(data[i]["feRegularData"])
            '''
            feRegularData = data[i]["feRegularData"]
            feCustomData = data[i]["feCustomData"]
            feBoneData = data[i]["feBoneData"]
            feEyeLData = data[i]["feEyeLData"]
            feEyeRData = data[i]["feEyeRData"]
            feHeadData = data[i]["feHeadData"]
            '''
            for j in range(60):
                #debugMsg(rlSliderRegularContainer[j].id)
                rlSliderRegularContainer[j].container.setValue(data[i]["feRegularData"][oldToNew[j]-1]*100)
                #rlSliderRegularContainer[j].container.setValue(data[i]["feRegularData"][j]*100)
            for j in range(24):
                rlSliderCustomContainer[j].container.setValue(data[i]["feCustomData"][j]*100)
            for j in range(6):
                rlSliderBoneContainer[j].container.setValue(data[i]["feBoneData"][j]*100)
            for j in range(2):
                rlSliderEyeLContainer[j].container.setValue(data[i]["feEyeLData"][j]*100)
            for j in range(2):
                rlSliderEyeRContainer[j].container.setValue(data[i]["feEyeRData"][j]*100)
            for j in range(3):
                rlSliderHeadContainer[j].container.setValue(data[i]["feHeadData"][j]*100)
            
            break
    
    global sourceData
            
    for i in range(len(sourceData)):
        for j in range(len(data)):
            if ( data[j]["id"] == sourceData[i].name ):
                try:
                    #debugMsg(data[j]["strength"])
                    sourceData[i].container.setMultiplyValue(data[j]["strength"])
                    #debugMsg(sourceData[i].container.multiplyValue)
                    #debugMsg(sourceData[i].container.multiplyValue)
                except:
                    None
    
    showSlider()
    #debugMsg(data)
    
def loop():
    device.loop()
            
def startPreview():
    #debugMsg("startPreview")
    global device
    #debugMsg(device)
    device.start()
    scriptEvent.Append("Timer","loop()",[1, -1])
    script.Play()
            
            
def startRecord():
    stop()
    script.Stop()

def stop():
    device.stop()
    scriptEvent.StopTimer()

def showDataSource():
    fmDataSourceUi.show()

def sliderStrengthChanged():
    global globalStrength
    globalStrength = fmMappingUi.qtGlobalStrengthSlider.value()
    fmMappingUi.qtGlobalStrengthSpinBox.setValue(globalStrength)
    #debugMsg(globalStrength)
def spinboxStrengthChanged():
    global globalStrength
    globalStrength = fmMappingUi.qtGlobalStrengthSpinBox.value()
    fmMappingUi.qtGlobalStrengthSlider.setValue(globalStrength)

def smoothFactor(type):
    if (type=="head"):
        '''
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],2))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],3))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],4))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],5))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],6))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],7))
        debugMsg(smoothList([1,2,3,4,5,6,7,8,9,10,11],8))
        '''
        None
    elif (type=="brow"):
        None
    elif (type=="eye"):
        None
    elif (type=="mouth"):
        None
    else:
        None
    
    
def headSmooth():
    smoothFactor("head")

def browSmooth():
    smoothFactor("brow")

def eyeSmooth():
    smoothFactor("eye")

def mouthSmooth():
    smoothFactor("mouth")


    
    
    
#init
app = PySide2.QtWidgets.QApplication.instance()
if not app:
    app = PySide2.QtWidgets.QApplication ([])

loader = QUiLoader()
file = PySide2.QtCore.QFile(mainUI)
file.open(PySide2.QtCore.QFile.ReadOnly)
fmMainUi = loader.load(file)

mainWidget = resource.rlWidget.rlWidget()
hboxLayout = PySide2.QtWidgets.QVBoxLayout()
mainWidget.setLayout( hboxLayout )
mainWidget.layout().addWidget( fmMainUi )
mainWidget.show()

#fmMainUi.show()
fmMainUi.qtMappingToolButton.clicked.connect(openMappingDlg)
fmMainUi.qtRecordPushButton.clicked.connect(startRecord)
fmMainUi.qtPreviewPushButton.clicked.connect(startPreview)


fmMainUi.qtHeadSmoothSlider.valueChanged.connect(headSmooth)
fmMainUi.qtBrowSmoothSlider.valueChanged.connect(browSmooth)
fmMainUi.qtEyeSmoothSlider.valueChanged.connect(eyeSmooth)
fmMainUi.qtMouthSmoothSlider.valueChanged.connect(mouthSmooth)

loader = QUiLoader()
file = PySide2.QtCore.QFile(mappingUI)
file.open(PySide2.QtCore.QFile.ReadOnly)
fmMappingUi = loader.load(file)
#fmMappingUi.show()
fmMappingUi.qtZeroAllPushButton.clicked.connect(zeroAll)
fmMappingUi.qtSavePushButton.clicked.connect(saveData)
fmMappingUi.qtLoadPushButton.clicked.connect(loadData)
fmMappingUi.qtShowAllSliderCheckBox.clicked.connect(showSlider)
fmMappingUi.qtDataSourcePushButton.clicked.connect(showDataSource)
fmMappingUi.qtGlobalStrengthSlider.valueChanged.connect(sliderStrengthChanged)
fmMappingUi.qtGlobalStrengthSpinBox.valueChanged.connect(spinboxStrengthChanged)


#fmMappingUi.qtLoadPushButton.clicked.connect(loadData)
#fmMappingUi.qtZeroAllPushButton.connect(zeroAll)
mainWidget.setRelatedWidget(fmMappingUi)

loader = QUiLoader()
file = PySide2.QtCore.QFile(dataSourceUI)
file.open(PySide2.QtCore.QFile.ReadOnly)
fmDataSourceUi = loader.load(file)
mainWidget.setRelatedWidget(fmDataSourceUi)

#fmDataSourceUi.show()
loader = QUiLoader()
file = PySide2.QtCore.QFile(dataSmoothUI)
file.open(PySide2.QtCore.QFile.ReadOnly)
fmDataSmoothUi = loader.load(file)
mainWidget.setRelatedWidget(fmDataSmoothUi)
#
loader = QUiLoader()
file = PySide2.QtCore.QFile(dataRangeUI)
file.open(PySide2.QtCore.QFile.ReadOnly)
fmDataRangeUi = loader.load(file)
mainWidget.setRelatedWidget(fmDataRangeUi)


def initUi():
    
    global sourceData
    #initDataStructure()
    for i in range (len(facewareList)):
        temp = DataSourceID(facewareList[i], i, fmDataSourceUi.qtScrollAreaWidgetContents, 1)
        sourceData.append(temp)
    
    
    fmMappingUi.qtExpressionComboBox.addItems(facewareList)
    #debugMsg(fmMappingUi.qtExpressionComboBox.currentText())
    #fmMappingUi.qtSetDataPushButton.clicked.connect(setData)
    
    fmMappingUi.qtExpressionComboBox.currentTextChanged.connect(changeData)
    
    for i in range (len(oldToNew)):
        temp = FacialID(feRegularList[i], oldToNew[i]-1, fmMappingUi.qtMuscleContextWidget, "feRegularData")
        rlSliderRegularContainer.append(temp)

    for j in range(24):
        temp = FacialID(feCustomList[j], j, fmMappingUi.qtCustomContextWidget, "feCustomData")
        rlSliderCustomContainer.append(temp)

    for i in range (len(feBone)):
        temp = FacialID(feBone[i], i, fmMappingUi.qtBoneContextWidget, "feBoneData")
        rlSliderBoneContainer.append(temp)
   
    for i in range (len(feEyeL)):
        temp = FacialID(feEyeL[i], i, fmMappingUi.qtHeadEyeContextWidget, "feEyeLData")
        rlSliderEyeLContainer.append(temp)
    
    for i in range (len(feEyeR)):
        temp = FacialID(feEyeR[i], i, fmMappingUi.qtHeadEyeContextWidget, "feEyeRData")
        rlSliderEyeRContainer.append(temp)
    
    for i in range (len(feHead)):
        temp = FacialID(feHead[i], i, fmMappingUi.qtHeadEyeContextWidget, "feHeadData")
        rlSliderHeadContainer.append(temp)
    
    global device
    device = Faceware()
    
initUi()

mainWidget.setDevice(device)

loadDefaultData()

def zeroExpressionData():
    tempRegularData = []
    for i in range(60):
        tempRegularData.append(0)
    
    tempCustomData = []
    for i in range(24):
        tempCustomData.append(0)

    script.SetFacePuppetKeyWithName( script.GetPickedObjectName(),0,[0,0,0],[0,0],[0,0],[0,0,0,0,0,0,0,0,0,0,0,0],tempRegularData,tempCustomData )

zeroExpressionData()
'''
MainWindowptr = script.GetMainWindow()
MainWindow = wrapInstance( MainWindowptr, PySide2.QtWidgets.QMainWindow )
#print Myui.qtMappingContextWidget

#
Widgetptr  = script.GetWidget(":/plugin/ICVPL/VPLDlg.ui")

MainWindowptr = script.GetMainWindow()
Widget  = wrapInstance( Widgetptr, PySide2.QtWidgets.QWidget )

MainWindow = wrapInstance( MainWindowptr, PySide2.QtWidgets.QMainWindow )
'''