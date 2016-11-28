import PySide2

from qtRangeSlider import *

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import *

class VerticalSliderSpinner(QWidget):
    def __init__(self, parentWidget, label, degrees, _x, _y, _max, _min, smooth = False, mute = False, range = False, multiply = False ):
        # QWidget will be self
        QWidget.__init__(self)
        # setGeometry(x_pos, y_pos, width, height)
        # upper left corner coordinates (x_pos, y_pos)
        #self.setGeometry(300, 100, 520, 520)
        #self.setWindowTitle('Testing text rotation ...')
        self.value = 0
        
        #self.qRangeSlider = QHRangeSlider(slider_range = [0.0, 1.0, 0.5], values = [-2.5, 2.5])
        self.multiplyValue = 1
        
        self.parentWidget = parentWidget
        
        self.max = _max
        self.min = _min
        
        self.x = _x
        self.y = _y
        
        self.label = label
        self.degrees = degrees
        vboxLayout = PySide2.QtWidgets.QVBoxLayout()
        vboxLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout( vboxLayout )
        
        self.sliderContainer = PySide2.QtWidgets.QWidget()
        hboxLayout = PySide2.QtWidgets.QHBoxLayout()
        self.sliderContainer.setLayout( hboxLayout )
        
        self.layout().addWidget( self.sliderContainer )
        
        self.labelUi = PySide2.QtWidgets.QLabel()
        
        self.slider = PySide2.QtWidgets.QSlider(QtCore.Qt.Vertical)
        
        self.muteButton = PySide2.QtWidgets.QToolButton()
        self.smoothButton = PySide2.QtWidgets.QToolButton()
        self.rangeButton = PySide2.QtWidgets.QToolButton()
        
        #self.layout().addWidget( self.slider )
        self.sliderContainer.layout().addWidget( self.labelUi )
        self.sliderContainer.layout().addWidget( self.slider )
        
        self.buttonGroup = PySide2.QtWidgets.QWidget()
        hboxLayout = PySide2.QtWidgets.QHBoxLayout()
        self.buttonGroup.setLayout( hboxLayout )
        self.buttonGroup.layout().setContentsMargins(0,0,0,0)
        
        self.spinnerGroup = PySide2.QtWidgets.QWidget()
        hboxLayout = PySide2.QtWidgets.QHBoxLayout()
        self.spinnerGroup.setLayout( hboxLayout )
        self.spinnerGroup.layout().setContentsMargins(0,0,0,0)

        self.layout().addWidget( self.spinnerGroup )
        self.spinner = PySide2.QtWidgets.QSpinBox()
        self.multiplySpinner = PySide2.QtWidgets.QDoubleSpinBox()
        
        self.spinnerLabel = PySide2.QtWidgets.QLabel()
        
        self.spinnerGroup.layout().addWidget( self.multiplySpinner )
        self.spinnerGroup.layout().addWidget( self.spinnerLabel )
        self.spinnerGroup.layout().addWidget( self.spinner )
        
        
        self.spinnerLabel.setText("X")
        
        self.layout().addWidget( self.buttonGroup )
        self.buttonGroup.layout().addWidget( self.muteButton )
        self.buttonGroup.layout().addWidget( self.smoothButton )
        self.buttonGroup.layout().addWidget( self.rangeButton )
        
        self.muteButton.setText("M")
        self.muteButton.setCheckable(True)
        self.smoothButton.setText("S")
        self.rangeButton.setText("R")
        #self.smoothButton.setCheckable(True)
        
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.spinner.valueChanged.connect(self.spinnerValueChanged)
        
        self.spinner.setMaximum(self.max)
        self.spinner.setMinimum(self.min)
        self.spinner.setValue( 0 )
        
        self.multiplySpinner.setMaximum(3)
        self.multiplySpinner.setMinimum(0)
        self.multiplySpinner.setSingleStep(0.1)
        self.multiplySpinner.setValue( self.multiplyValue )
        
        self.slider.setMaximum(self.max)
        self.slider.setMinimum(self.min)
        self.slider.setValue( 0 )
        
        if ( smooth ):
            self.smoothButton.show()
        else:
            self.smoothButton.hide()
        
        if ( range ):
            self.rangeButton.show()
        else:
            self.rangeButton.hide()
        
        if ( mute ):
            self.muteButton.show()
        else:
            self.muteButton.hide()
            
        if ( multiply ):
            self.multiplySpinner.show()
            self.spinnerLabel.show()
            self.spinner.setEnabled(False)
            self.slider.setEnabled(False)
        else:
            self.multiplySpinner.hide()
            self.spinnerLabel.hide()
            self.spinner.setEnabled(True)
            self.slider.setEnabled(True)
        
        self.rangeButton.clicked.connect(self.showRangeDlg)
        self.smoothButton.clicked.connect(self.showSmoothDlg)
        self.muteButton.clicked.connect(self.muteClick)
        
        self.multiplySpinner.valueChanged.connect(self.multiplySpinnerChanged)
    
    def setMultiplyValue(self,value):
        self.multiplyValue = value
        self.multiplySpinner.setValue(self.multiplyValue)
    
    def multiplySpinnerChanged(self):
        self.multiplyValue = self.multiplySpinner.value()
    
    def muteClick(self):
        self.muteClick = self.muteButton.ckecked
    
    def showRangeDlg(self):
        '''
        dialog = QRangeSliderDialog(title_text = "Range Slider",
                                    slider_range = [0,1,0.1],
                                    values = [0, 1])
        
        dialog.open()
        dialog.exec_()
        '''
        None
        
    def showSmoothDlg(self):
        None
    
    def setValue(self,value):
        self.value = value
        self.spinner.setValue( value )
        self.slider.setValue( value )
        self.parentWidget.onValueChanged(self.value)
        
    def spinnerValueChanged(self):
        #print "spinner"
        self.value = self.spinner.value()
        self.slider.setValue( self.spinner.value() )
        
    def sliderValueChanged(self):
        #print "slider"
        self.value = self.slider.value()
        self.spinner.setValue( self.slider.value() )
        self.parentWidget.onValueChanged(self.value)
    
    def paintEvent(self, event):
        '''
        the method paintEvent() is called automatically
        the QPainter class does the low-level painting
        between its methods begin() and end()
        '''
        qp = QtGui.QPainter()
        qp.begin(self)
        # set text color, default is black
        qp.setPen('black')
        # QFont(family, size)
        #qp.setFont(QFont('Decorative', 12))
        # start text at point (x, y)
        #print self.height()
        x = self.x
        y = self.height() - self.y
        qp.translate(x, y)
        qp.rotate(self.degrees)
        qp.drawText(0, 0, self.label)
        qp.end()