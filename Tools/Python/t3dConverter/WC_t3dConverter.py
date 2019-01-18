import t3dUtilityFunctions as t
import sys
import uuid
import io
import StringIO
from PySide import QtGui, QtCore

class Window(QtGui.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.textWindow = ""
        self.initUI()
        
    def initUI(self):
        self.setGeometry(300, 300, 400, 300)
        self.setWindowTitle("Wildcard Python Tools")
        
        # Text window
        self.txtWidget = QtGui.QTextEdit(self)
        self.txtWidget.createStandardContextMenu()
        self.setCentralWidget(self.txtWidget)
        
        # Toolbar
        self.convertMatAction = QtGui.QAction('Convert Material', self)
        self.convertMatAction.setShortcut('Ctrl+E')
        self.convertMatAction.setStatusTip('Convert Material to Ark or Unreal engine')
        self.convertMatAction.triggered.connect(self.convertMat)

        self.getPointPosAction = QtGui.QAction('Get Point Position', self)
        self.getPointPosAction.setShortcut('Ctrl+P')
        self.getPointPosAction.setStatusTip('Get point position from t3d data')
        self.getPointPosAction.triggered.connect(self.getPointPos)

        self.getPointRotAction = QtGui.QAction('Get Point Rotation', self)
        self.getPointRotAction.setShortcut('Ctrl+R')
        self.getPointRotAction.setStatusTip('Get point position from t3d data')
        self.getPointRotAction.triggered.connect(self.getPointRot)
        
        self.exitAction = QtGui.QAction('Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("&File")
        fileMenu.addAction(self.exitAction)

        fileMenu = menubar.addMenu("&Points")
        fileMenu.addAction(self.getPointPosAction)
        fileMenu.addAction(self.getPointRotAction)

        fileMenu = menubar.addMenu("&Materials")
        fileMenu.addAction(self.convertMatAction)

        # Footer
        self.statusBar()
        
        self.show()
        
    # Returns correctly formatted t3d data for unreal or ark engine    
    def convertMat(self):
        fileString = self.txtWidget.toPlainText()
        stringList = t.createStringList(fileString)
        isFromArkEngine = t.isFromArkEngine(stringList)
        nodeList = t.generateNodeList(stringList, isFromArkEngine)
        
        if isFromArkEngine:
            output = t.unrealFormat(nodeList)
        else:
            output = t.arkFormat(nodeList)
            
        self.txtWidget.setText(output)

    # Extract point positions from t3d data as csv
    def getPointPos(self):
        fileString = self.txtWidget.toPlainText()
        stringList = t.createStringList(fileString)
        output = ""
        
        for line in stringList:
            if "RelativeLocation" in line:
                line = line[32:-2]
                lineList = line.replace("Y=", "").replace("Z=", "").split(",")
                output += "{0},{1},{2}\n".format(lineList[0], lineList[2], lineList[1])
        self.txtWidget.setText(output)
    
    def getPointRot(self):
        fileString = self.txtWidget.toPlainText()
        stringList = t.createStringList(fileString)
        output = ""
        
        for line in stringList:
            if "RelativeRotation" in line:
                line = line[36:-2]
                lineList = line.replace("Yaw=", "").replace("Roll=", "").split(",")
                output += "{0},{1},{2}\n".format(lineList[0], lineList[2], lineList[1])
        self.txtWidget.setText(output)

def main():
    app = QtGui.QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
    
main()