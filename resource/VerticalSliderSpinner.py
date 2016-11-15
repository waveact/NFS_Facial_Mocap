""" ps_draw_text_rotated.py
draw a rotated text with PySide's QPainter class
download PySide (LGPL-licensed version of PyQT) from:
http://qt-project.org/wiki/PySide
or Windows binary from:
http://www.lfd.uci.edu/~gohlke/pythonlibs/
tested with Python27/34 and PySide122   by  vegaseat  26oct2014
"""
import PySide2

from PySide2 import QtGui
from PySide2 import QtCore
from PySide2.QtWidgets import *

class VerticalSliderSpinner(QWidget):
    def __init__(self, parentWidget, label, degrees, _x, _y, _max, _min):
        # QWidget will be self
        QWidget.__init__(self)
        # setGeometry(x_pos, y_pos, width, height)
        # upper left corner coordinates (x_pos, y_pos)
        #self.setGeometry(300, 100, 520, 520)
        #self.setWindowTitle('Testing text rotation ...')
        self.value = 0
        
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
        #self.layout().addWidget( self.slider )
        self.sliderContainer.layout().addWidget( self.labelUi )
        self.sliderContainer.layout().addWidget( self.slider )
        
        self.spinner = PySide2.QtWidgets.QSpinBox()
        self.layout().addWidget( self.spinner )
        
        self.slider.valueChanged.connect(self.sliderValueChanged)
        self.spinner.valueChanged.connect(self.spinnerValueChanged)
        
        self.spinner.setMaximum(self.max)
        self.spinner.setMinimum(self.min)
        self.spinner.setValue( 0 )
        
        self.slider.setMaximum(self.max)
        self.slider.setMinimum(self.min)
        self.slider.setValue( 0 )
    
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