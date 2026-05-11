from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *
import shapefile

class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(1043, 948)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1043, 33))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuInput = QtWidgets.QMenu(parent=self.menubar)
        self.menuInput.setObjectName("menuInput")
        self.menuAnalyze = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalyze.setObjectName("menuAnalyze")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        
        self.actionPoint_polygon = QtGui.QAction(parent=MainForm)
        self.actionPoint_polygon.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/pointpol.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPoint_polygon.setIcon(icon2)
        self.actionPoint_polygon.setObjectName("actionPoint_polygon")
        
        self.actionClear = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear.setIcon(icon3)
        self.actionClear.setObjectName("actionClear")
        
        self.actionRay_Crossing = QtGui.QAction(parent=MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/ray.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionRay_Crossing.setIcon(icon4)
        self.actionRay_Crossing.setObjectName("actionRay_Crossing")
        
        self.actionWinding_Number = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/winding.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWinding_Number.setIcon(icon5)
        self.actionWinding_Number.setObjectName("actionWinding_Number")
        
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuInput.addAction(self.actionPoint_polygon)
        self.menuInput.addSeparator()
        self.menuInput.addAction(self.actionClear)
        self.menuAnalyze.addAction(self.actionRay_Crossing)
        self.menuAnalyze.addAction(self.actionWinding_Number)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuInput.menuAction())
        self.menubar.addAction(self.menuAnalyze.menuAction())
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionRay_Crossing)
        self.toolBar.addAction(self.actionWinding_Number)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionPoint_polygon)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear)

        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)
        
        # Connect buttons to functions
        self.actionOpen.triggered.connect(self.openFileClick)
        self.actionPoint_polygon.triggered.connect(self.changeStatusClick)
        self.actionClear.triggered.connect(self.clearClick)
        self.actionRay_Crossing.triggered.connect(self.analyzePointAndPositionClick)
        self.actionWinding_Number.triggered.connect(self.analyzeWindingNumberClick)
                
    def changeStatusClick(self, *args):
        self.Canvas.changeStatus()
        
    def clearClick(self):
        self.Canvas.clearData()    

    def analyzePointAndPositionClick(self, *args):
        self.runAnalysis("Ray Crossing")

    def analyzeWindingNumberClick(self, *args):
        self.runAnalysis("Winding Number")
        
    def openFileClick(self):
        # Open shapefile dialog
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Open Shapefile", "", "Shapefiles (*.shp)")
        if not file_name:
            return

        try:
            # Read shapefile
            sf = shapefile.Reader(file_name)
            shapes = sf.shapes()
            
            loaded_polygons = []
            
            # Get bounding box to calculate scale
            min_x, min_y, max_x, max_y = sf.bbox
            width = max_x - min_x
            height = max_y - min_y
            
            # Prevent division by zero
            if width == 0: width = 1
            if height == 0: height = 1
            
            # Calculate scale to fit 800x800 window
            scale_x = 800 / width
            scale_y = 800 / height
            scale = min(scale_x, scale_y) * 0.95 
            
            for shape in shapes:
                # ShapeType 5 is Polygon
                if shape.shapeType != 5:
                    continue
                    
                points = shape.points
                parts = list(shape.parts)
                parts.append(len(points)) 
                
                complex_pol = []
                for i in range(len(parts) - 1):
                    start_idx = parts[i]
                    end_idx = parts[i+1]
                    ring_points = points[start_idx:end_idx]
                    
                    ring = QtGui.QPolygonF()
                    for px, py in ring_points:
                        # Translate, scale and flip Y axis
                        screen_x = (px - min_x) * scale + 20
                        screen_y = 850 - ((py - min_y) * scale + 20) 
                        ring.append(QtCore.QPointF(screen_x, screen_y))
                        
                    complex_pol.append(ring)
                    
                loaded_polygons.append(complex_pol)
                
            # Send polygons to canvas
            self.Canvas.setPolygons(loaded_polygons)
            
            mb = QtWidgets.QMessageBox(self.centralwidget)
            mb.setWindowTitle('Success')
            mb.setText(f'Successfully loaded {len(loaded_polygons)} polygons.')
            mb.exec()
            
        except Exception as e:
            error_box = QtWidgets.QMessageBox(self.centralwidget)
            error_box.setWindowTitle("Error")
            error_box.setText(f"Failed to load shapefile: {str(e)}")
            error_box.exec()

    def runAnalysis(self, algorithm_name):
        # Run selected algorithm for all polygons
        try:
            q = self.Canvas.getQ()
            polygons = self.Canvas.getPolygons()
            a = Algorithms()
            
            highlighted_indices = []
            status_messages = []
            
            for i, complex_pol in enumerate(polygons):
                if not complex_pol or complex_pol[0].isEmpty():
                    continue
                    
                # Skip if point is outside bounding box
                if not a.isInBoundingBox(q, complex_pol):
                    continue 
                    
                if algorithm_name == "Ray Crossing":
                    result = a.getPointPolygonPositionRC(q, complex_pol)
                else:
                    result = a.getPointPolygonPositionWN(q, complex_pol)
                
                # Save results
                if result == 1:
                    highlighted_indices.append(i)
                    status_messages.append("inside")
                elif result == -1:
                    highlighted_indices.append(i)
                    status_messages.append("on the edge")
                elif result == -2:
                    highlighted_indices.append(i)
                    status_messages.append("on the vertex")
                elif result is None:
                    print(f"{algorithm_name} found None on the polygon {i+1}.")
            
            # Highlight found polygons
            self.Canvas.setHighlightedPolygons(highlighted_indices)
            
            # Show message box
            mb = QtWidgets.QMessageBox(self.centralwidget)
            mb.setWindowTitle(f'Results: {algorithm_name}')
            
            if highlighted_indices:
                msg = "Point is:\n"
                for idx, status in zip(highlighted_indices, status_messages):
                    msg += f"- {status} of polygon {idx + 1}\n"
                mb.setText(msg)
            else: 
                mb.setText("Point is outside all polygons.") 
                
            mb.exec()
            
        except Exception as e:
            error_box = QtWidgets.QMessageBox(self.centralwidget)
            error_box.setWindowTitle("Error")
            error_box.setText(f"Something went wrong: {str(e)}")
            error_box.exec()

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Analyze point and polygon position"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuInput.setTitle(_translate("MainForm", "Input"))
        self.menuAnalyze.setTitle(_translate("MainForm", "Analyze"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionOpen.setToolTip(_translate("MainForm", "Open file"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionExit.setToolTip(_translate("MainForm", "Close application"))
        self.actionPoint_polygon.setText(_translate("MainForm", "Point / polygon"))
        self.actionPoint_polygon.setToolTip(_translate("MainForm", "Switch point / polygon input"))
        self.actionClear.setText(_translate("MainForm", "Clear"))
        self.actionClear.setToolTip(_translate("MainForm", "Clear data"))
        self.actionRay_Crossing.setText(_translate("MainForm", "Ray Crossing"))
        self.actionRay_Crossing.setToolTip(_translate("MainForm", "Analyze point and polygon position using Ray Crossing algorithm"))
        self.actionWinding_Number.setText(_translate("MainForm", "Winding Number"))
        self.actionWinding_Number.setToolTip(_translate("MainForm", "Analyze point and polygon position using Winding Number algorithm"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())