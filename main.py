from asyncio import constants
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType

import sys
import os

import matplotlib
from matplotlib import image
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

import numpy as np
import cv2 as cv

from math import pow, log


class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, dpi=100):
        fig = Figure(dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)

MainUi,_ = loadUiType('GUI.ui')
class Main(QMainWindow, MainUi):
    def __init__(self,parent=None):
        super(Main,self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.Handle_Buttons()
        self.Handle_Themes()
        
        

    image = None
    imagePath = None
    outputImage = None
    accomulatedEffects = []
    
    firstTime = True
    firstTime2 = True
    
    def Handle_Buttons(self):
        self.actionBrowse.triggered.connect(self.browse_image)
        self.actionSave_Image.triggered.connect(self.saveImage)
        
        self.toGray.clicked.connect(self.convert2Gray)
        self.Threshold.clicked.connect(self.threshold)
        self.resampleUp.clicked.connect(self.resample_Up)
        self.subSample.clicked.connect(self.sub_Sample)
        self.changeGrayLevel.clicked.connect(self.change_Gray_Level)
        self.negativeTransform.clicked.connect(self.negative_Transform)
        self.logTransform.clicked.connect(self.log_Transform)
        self.powerLaw.clicked.connect(self.power_Law)
        self.Contrast.clicked.connect(self.contrast)
        self.sliceGrayLevel.clicked.connect(self.slice_Gray_Level)
        self.addConstant.clicked.connect(self.add_Constant)
        self.subtractConstant.clicked.connect(self.subtract_Constant)
        self.subtractImage.clicked.connect(self.subtract_Image)
        self.bitPlaneSlice.clicked.connect(self.bit_Plane_Slice)
        self.specificBitPlaneSlice.clicked.connect(self.specific_Bit_Plane_Slice)
        self.equalizeImage.clicked.connect(self.equalize_Image)
        self.applyAverageFilter.clicked.connect(self.apply_Average_Filter)
        self.applyMinFilter.clicked.connect(self.apply_Min_Filter)
        self.applyMaxFilter.clicked.connect(self.apply_Max_Filter)
        self.applyMedianFilter.clicked.connect(self.apply_Median_Filter)
        self.applyweightedAverageFilter.clicked.connect(self.apply_weightedAverage_Filter)
        self.applysharpening1stDerivativeFilter.clicked.connect(self.apply_sharpening1stDerivative_Filter)
        self.applysharpening2ndDerivativeCompositeLaplacianFilter.clicked.connect(self.apply_sharpening2ndDerivativeCompositeLaplacian_Filter)
        self.applySobelOperatorsFilter.clicked.connect(self.apply_SobelOperators_Filter)
        self.applyRobertsOperatorsFilter.clicked.connect(self.apply_RobertsOperators_Filter)
        self.revertButton.clicked.connect(self.revert)
        self.revertButton2.clicked.connect(self.revert)
    
    def browse_image(self):
        self.imagePath = None
        self.imagePath = QFileDialog.getOpenFileName(self, 'Open Image', './', 'Image Files (*.png *.jpg *.jpeg)')[0]
        if self.imagePath != None and self.imagePath != '':
            self.image = self.RGB2GRAY(imagePATH = self.imagePath)
            self.accomulatedEffects.append(self.image)
            
            self.plotOriginalImage()
            self.showOriginalImage()
    
    def saveImage(self):
        text, okPressed = QInputDialog.getText(self, "Save Image", "<html style='font-size:10pt; color:red;'>Enter Image Name:</html>", QLineEdit.Normal, "")
        if okPressed:
            if not os.path.exists('Output'):
                os.makedirs('Output')
            if os.path.exists('output/output_image.png'):
                os.remove('output/output_image.png')
            cv.imwrite(f'output/{text}.png', np.array(self.outputImage))
    
    def revert(self):
        print(len(self.accomulatedEffects))
        if len(self.accomulatedEffects) == 1:
            print("less than 1")
            self.outputImage = self.accomulatedEffects[-1]
            self.image = self.outputImage
            self.plotOutputImage(False)
            self.showOutputImage()
            
        elif len(self.accomulatedEffects) > 1:
            print("higher than 1")
            self.accomulatedEffects = self.accomulatedEffects[:-1] 
            self.outputImage = self.accomulatedEffects[-1]
            self.image = self.outputImage
            self.plotOutputImage(False)
            self.showOutputImage()
            if len(self.accomulatedEffects) == 1:
                self.revertButton.setEnabled(False)
                self.revertButton2.setEnabled(False)
    
    def RGB2GRAY(self, image = None,imagePATH = None):
        if imagePATH != None:
            image = cv.imread(imagePATH)
    
        newImage = []
        for row in image:
            tmpRow = []
            for pixel in row:
                tmpRow.append(int(sum(pixel)/3))
            newImage.append(tmpRow)
        return newImage
    
    def getImageMap(self, image):
        numberList = list(range(0,256))
        valMap = {}
        for row in image:
            for pixel in row:
                if pixel in valMap.keys():
                    valMap[pixel] += 1
                else:
                    valMap[pixel] = 1
                    numberList.remove(pixel)
                    
        for n in numberList:
            valMap[n] = 0
            
        return valMap
    
    def plotOriginalImage(self):
        valMap = self.getImageMap(self.image)
        
        sc = MplCanvas(dpi=100)
        sc.axes.stem(list(valMap.keys()), list(valMap.values()))
        sc.axes.set_xlabel('Pixel Value')
        sc.axes.set_ylabel('Frequency')
        
        if self.firstTime:
            self.layoutVert1 = QVBoxLayout()
            self.layoutVert1.addWidget(sc)
            self.groupBox.setLayout(self.layoutVert1)
            self.firstTime = False
        else:
            self.layoutVert1.replaceWidget(self.groupBox.layout().itemAt(0).widget(), sc)
    
    def showOriginalImage(self):
        #self.originalImage.setScaledContents(True)
        self.original_Image.setPixmap(QPixmap(self.imagePath))
        
    def plotOutputImage(self, addOutput = True):
        if addOutput:
            self.accomulatedEffects.append(self.outputImage)
            self.image = self.outputImage
            if len(self.accomulatedEffects) > 1:
                self.revertButton.setEnabled(True)
                self.revertButton2.setEnabled(True)
        
        valMap = self.getImageMap(self.outputImage)
    
        sc2 = MplCanvas(dpi=100)
        sc2.axes.stem(list(valMap.keys()), list(valMap.values()))
        sc2.axes.set_xlabel('Pixel Value')
        sc2.axes.set_ylabel('Frequency')
        
        if self.firstTime2:
            self.layoutVert2 = QVBoxLayout()
            self.layoutVert2.addWidget(sc2)
            self.groupBox_4.setLayout(self.layoutVert2)
            self.firstTime2 = False
        else:
            self.layoutVert2.replaceWidget(self.groupBox_4.layout().itemAt(0).widget(), sc2)
    
    def showOutputImage(self):
        #self.originalImage.setScaledContents(True)
        if not os.path.exists('temp'):
            os.makedirs('temp')
        if os.path.exists('temp/tmp.png'):
            os.remove('temp/tmp.png')
            
        cv.imwrite('temp/tmp.png', np.array(self.outputImage))
        self.output_Image.setPixmap(QPixmap('temp/tmp.png'))  
    
    def convert2Gray(self):
        self.outputImage = self.image
        self.plotOutputImage()
        self.showOutputImage()
    
    def threshold(self):
        myMap = self.getImageMap(self.image)
        width, heigth = np.array(self.image).shape
        pixels = width * heigth
        comulativeSum = 0
        threshold = None
        
        for i in range(256):
            if comulativeSum < (pixels/2):
                comulativeSum += myMap[i]
            else:
                threshold = i
                break
                
        newImage = []
        for row in self.image:
            tmpRow = []
            for pixel in row:
                tmpRow.append(255 if pixel > threshold else 0)
            newImage.append(tmpRow)
            
        self.outputImage = newImage
        self.plotOutputImage()
        self.showOutputImage()

def main():
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()