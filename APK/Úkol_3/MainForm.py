# Form implementation generated from reading ui file 'form.ui'
# Merged with analysis logic by APK U3

from PyQt6 import QtCore, QtGui, QtWidgets
from draw import Draw
from algorithms import *

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1111, 1015)
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Canvas (Draw widget)
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainWindow.setCentralWidget(self.centralwidget)

        # Menu and StatusBar
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1111, 26))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAnalysis = QtWidgets.QMenu(parent=self.menubar)
        self.menuAnalysis.setObjectName("menuAnalysis")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        self.menuClear = QtWidgets.QMenu(parent=self.menubar)
        self.menuClear.setObjectName("menuClear")
        self.menuSettings = QtWidgets.QMenu(parent=self.menubar)
        self.menuSettings.setObjectName("menuSettings")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        self.toolBar = QtWidgets.QToolBar(parent=MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
       

        #ACTIONS WITH ICONS
        self.actionOpen = QtGui.QAction(parent=MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("images/icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon)
        self.actionOpen.setObjectName("actionOpen")
        
        self.actionExit = QtGui.QAction(parent=MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("images/icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon1)
        self.actionExit.setObjectName("actionExit")
        
        self.actionCreate_DT = QtGui.QAction(parent=MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("images/icons/triangles2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreate_DT.setIcon(icon2)
        self.actionCreate_DT.setObjectName("actionCreate_DT")
        
        self.actionCreateContouLines = QtGui.QAction(parent=MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("images/icons/contours2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionCreateContouLines.setIcon(icon3)
        self.actionCreateContouLines.setObjectName("actionCreateContouLines")
        
        self.actionAnalyzeSlope = QtGui.QAction(parent=MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("images/icons/slope2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyzeSlope.setIcon(icon4)
        self.actionAnalyzeSlope.setObjectName("actionAnalyzeSlope")
        
        self.actionAnalyzeExposition = QtGui.QAction(parent=MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("images/icons/orientation2.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionAnalyzeExposition.setIcon(icon5)
        self.actionAnalyzeExposition.setObjectName("actionAnalyzeExposition")

        # NEW ACTIONS (Bonuses)
        self.actionAnalyzeHypsometry = QtGui.QAction("Analyze Hypsometry", parent=MainWindow)
        self.actionAnalyzeHypsometry.setObjectName("actionAnalyzeHypsometry")
        
        self.actionDT = QtGui.QAction(parent=MainWindow)
        self.actionDT.setCheckable(True)
        self.actionDT.setChecked(True)
        self.actionDT.setObjectName("actionDT")
        
        self.actionContour_lines_2 = QtGui.QAction(parent=MainWindow)
        self.actionContour_lines_2.setCheckable(True)
        self.actionContour_lines_2.setChecked(True)
        self.actionContour_lines_2.setObjectName("actionContour_lines_2")
        
        self.actionSlope = QtGui.QAction(parent=MainWindow)
        self.actionSlope.setCheckable(True)
        self.actionSlope.setObjectName("actionSlope")
        
        self.actionExposition = QtGui.QAction(parent=MainWindow)
        self.actionExposition.setCheckable(True)
        self.actionExposition.setObjectName("actionExposition")

        self.actionHypsometry = QtGui.QAction("Hypsometry Fill", parent=MainWindow)
        self.actionHypsometry.setCheckable(True)
        self.actionHypsometry.setObjectName("actionHypsometry")

        self.action3D = QtGui.QAction("Toggle 3D View", parent=MainWindow)
        self.action3D.setCheckable(True)
        self.action3D.setObjectName("action3D")
        
        self.actionClear_results = QtGui.QAction(parent=MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("images/icons/clear.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_results.setIcon(icon6)
        self.actionClear_results.setObjectName("actionClear_results")
        
        self.actionClear_all = QtGui.QAction(parent=MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("images/icons/clear_all.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon7)
        self.actionClear_all.setObjectName("actionClear_all")

        self.actionParameters = QtGui.QAction(parent=MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("images/icons/settings.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionParameters.setIcon(icon8)
        self.actionParameters.setObjectName("actionParameters")

        # MENU ASSEMBLY
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        
        self.menuAnalysis.addAction(self.actionCreate_DT)
        self.menuAnalysis.addSeparator()
        self.menuAnalysis.addAction(self.actionCreateContouLines)
        self.menuAnalysis.addAction(self.actionAnalyzeSlope)
        self.menuAnalysis.addAction(self.actionAnalyzeExposition)
        self.menuAnalysis.addAction(self.actionAnalyzeHypsometry)
        
        self.menuView.addAction(self.actionDT)
        self.menuView.addAction(self.actionContour_lines_2)
        self.menuView.addAction(self.actionSlope)
        self.menuView.addAction(self.actionExposition)
        self.menuView.addAction(self.actionHypsometry)
        self.menuView.addSeparator()
        self.menuView.addAction(self.action3D)
        
        self.menuClear.addAction(self.actionClear_results)
        self.menuClear.addSeparator()
        self.menuClear.addAction(self.actionClear_all)
        self.menuSettings.addAction(self.actionParameters)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuAnalysis.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuClear.menuAction())
        self.menubar.addAction(self.menuSettings.menuAction())

        # Toolbar
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCreate_DT)
        self.toolBar.addAction(self.actionCreateContouLines)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAnalyzeSlope)
        self.toolBar.addAction(self.actionAnalyzeExposition)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_results)
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionExit)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action3D)
        self.toolBar.addSeparator()

        # GENERATE TERRAIN MENU
        self.menuTerrain = QtWidgets.QMenu("Generate Terrain", parent=self.menuAnalysis)
        self.menuAnalysis.addMenu(self.menuTerrain)
        
        self.actionGenHill = QtGui.QAction("Kupa (Hill)", parent=MainWindow)
        self.actionGenValley = QtGui.QAction("Údolí (Valley)", parent=MainWindow)
        self.actionGenRidge = QtGui.QAction("Hřbet (Ridge)", parent=MainWindow)
        self.actionGenSaddle = QtGui.QAction("Spočinek (Saddle)", parent=MainWindow)
        
        self.menuTerrain.addAction(self.actionGenHill)
        self.menuTerrain.addAction(self.actionGenValley)
        self.menuTerrain.addAction(self.actionGenRidge)
        self.menuTerrain.addAction(self.actionGenSaddle)

        # CONNECTIONS
        self.actionCreate_DT.triggered.connect(self.createDTClick)
        self.actionCreateContouLines.triggered.connect(self.createContourLinesClick)
        self.actionAnalyzeSlope.triggered.connect(self.analyzeSlopeClick)
        self.actionAnalyzeExposition.triggered.connect(self.analyzeExpositionClick)
        self.actionAnalyzeHypsometry.triggered.connect(self.analyzeHypsometryClick)
        self.actionDT.triggered.connect(self.updateViewClick)
        self.actionContour_lines_2.triggered.connect(self.updateViewClick)
        self.actionSlope.triggered.connect(self.updateViewClick)
        self.actionExposition.triggered.connect(self.updateViewClick)
        self.actionHypsometry.triggered.connect(self.updateViewClick)
        self.action3D.triggered.connect(self.updateViewClick)
        self.actionClear_results.triggered.connect(self.Canvas.clearResult)
        self.actionClear_all.triggered.connect(self.Canvas.clearResult)
        self.actionGenHill.triggered.connect(lambda: self.generateTerrainClick("Hill"))
        self.actionGenValley.triggered.connect(lambda: self.generateTerrainClick("Valley"))
        self.actionGenRidge.triggered.connect(lambda: self.generateTerrainClick("Ridge"))
        self.actionGenSaddle.triggered.connect(lambda: self.generateTerrainClick("Saddle"))
        self.actionExit.triggered.connect(MainWindow.close)
        self.actionOpen.triggered.connect(self.openFileClick)
        
        self.retranslateUi(MainWindow)

    def createDTClick(self):
        points = self.Canvas.getPoints()
        polygon = self.Canvas.getPolygon()
        if len(points) < 3: return
        
        a = Algorithms()
        dt_edges, dt_triangles = a.createDT(points)
        
        # polygon clip
        if len(polygon) >= 3:
            dt_edges, dt_triangles = a.clipDT(dt_edges, dt_triangles, polygon)
            
        self.Canvas.setDT(dt_edges, dt_triangles)
        self.Canvas.repaint()

    def createContourLinesClick(self):
        DT_edges = self.Canvas.getDT()
        if not DT_edges:
            self.createDTClick()
            DT_edges = self.Canvas.getDT()
        z_min, z_max, dz = 200, 800, 20
        a = Algorithms()
        contours = a.createContourLines(DT_edges, z_min, z_max, dz)
        self.Canvas.setContours(contours)
        self.Canvas.repaint()

    def analyzeSlopeClick(self):
        self.actionSlope.setChecked(True)
        self.actionExposition.setChecked(False)
        self.actionHypsometry.setChecked(False)
        self.updateViewClick()

    def analyzeExpositionClick(self):
        self.actionSlope.setChecked(False)
        self.actionExposition.setChecked(True)
        self.actionHypsometry.setChecked(False)
        self.updateViewClick()

    def analyzeHypsometryClick(self):
        self.actionSlope.setChecked(False)
        self.actionExposition.setChecked(False)
        self.actionHypsometry.setChecked(True)
        self.updateViewClick()

    def updateViewClick(self):
        dt_vis = self.actionDT.isChecked()
        cont_vis = self.actionContour_lines_2.isChecked()
        slope_vis = self.actionSlope.isChecked()
        aspect_vis = self.actionExposition.isChecked()
        hyp_vis = self.actionHypsometry.isChecked()
        view_3d = self.action3D.isChecked()
        self.Canvas.setViewSettings(dt_vis, cont_vis, slope_vis, aspect_vis, hyp_vis, view_3d)
        self.Canvas.repaint()

    def generateTerrainClick(self, terrain_type):
        a = Algorithms()
        width = self.Canvas.width()
        height = self.Canvas.height()

        # Generate the requested number of points (you can increase the number from 600 if needed)
        points = a.generateTerrain(terrain_type, 600, width, height)

        polygon = self.Canvas.getPolygon()
        # Filter points by polygon (if one is drawn)
        if len(polygon) >= 3:
            filtered_points = []
            for p in points:
                if a.isPointInPolygon(QPointF(p.x(), p.y()), polygon):
                    filtered_points.append(p)
            points = filtered_points

        # WATCH THE INDENTATION: The following code must not be inside the "if len(polygon) >= 3:" block
        
        # 1. Clear old data before loading new points
        self.Canvas.clearResult()
        self.Canvas.getPoints().clear()
        
        # 2. Insert generated points into the canvas
        self.Canvas.getPoints().extend(points)
        self.Canvas.repaint()
        
        # 3. Automatically start triangulation
        self.createDTClick()
            
    def openFileClick(self):
        # 1. Zobrazení systémového dialogu s platným QWidget rodičem (centralwidget)
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.centralwidget, 
            "Otevřít geodetická data", 
            "", 
            "Text Files (*.txt *.csv *.xyz);;All Files (*)"
        )

        # Uživatel dialog zrušil (zavřel křížkem)
        if not file_path:
            return

        try:
            new_points = []
            # 2. Čtení souboru a parsování dat
            with open(file_path, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # Sjednocení oddělovačů pro podporu různých formátů (.csv, .txt)
                    parts = line.replace(',', ' ').split()
                    
                    if len(parts) >= 3:
                        try:
                            x = float(parts[0])
                            y = float(parts[1])
                            z = float(parts[2])
                            new_points.append(QPoint3DF(x, y, z))
                        except ValueError:
                            # Ignorování hlaviček a textových znaků
                            continue

            # 3. Validace počtu bodů a vizualizace
            if len(new_points) >= 3:
                # Očištění předchozích dat přes referenci na seznam z draw_2.py
                self.Canvas.getPoints().clear() 
                self.Canvas.getPoints().extend(new_points)
                self.Canvas.repaint()
                
                # Automatické sestavení Delaunayovy triangulace po načtení
                self.createDTClick()
                
                # Zobrazení informačního okna s platným QWidget rodičem
                QtWidgets.QMessageBox.information(
                    self.centralwidget, 
                    "Data načtena", 
                    f"Úspěšně načteno {len(new_points)} bodů."
                )
            else:
                QtWidgets.QMessageBox.warning(
                    self.centralwidget, 
                    "Neplatná data", 
                    "Soubor musí obsahovat alespoň 3 platné XYZ body."
                )

        except Exception as e:
            # Zachycení neočekávaných I/O chyb (např. chybějící oprávnění ke čtení)
            QtWidgets.QMessageBox.critical(
                self.centralwidget, 
                "Kritická chyba", 
                f"Během načítání souboru došlo k chybě:\n{str(e)}"
            )

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DTM Analysis - APK U3"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAnalysis.setTitle(_translate("MainWindow", "Analysis"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.menuClear.setTitle(_translate("MainWindow", "Clear"))
        self.menuSettings.setTitle(_translate("MainWindow", "Settings"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionCreate_DT.setText(_translate("MainWindow", "Create DT"))
        self.actionCreateContouLines.setText(_translate("MainWindow", "Create contour lines"))
        self.actionAnalyzeSlope.setText(_translate("MainWindow", "Analyze slope"))
        self.actionAnalyzeExposition.setText(_translate("MainWindow", "Analyze exposition"))
        self.actionDT.setText(_translate("MainWindow", "DT Edges"))
        self.actionContour_lines_2.setText(_translate("MainWindow", "Contour lines"))
        self.actionSlope.setText(_translate("MainWindow", "Slope Fill"))
        self.actionExposition.setText(_translate("MainWindow", "Exposition Fill"))
        self.actionClear_results.setText(_translate("MainWindow", "Clear results"))
        self.actionClear_all.triggered.connect(self.Canvas.clearAll)
        self.actionParameters.setText(_translate("MainWindow", "Parameters"))
        self.action3D.setText(_translate("MainWindow", "3D View"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
    
    