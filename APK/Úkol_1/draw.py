from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # List of polygons (index 0 is outer boundary, rest are holes)
        self.__polygons = [[QPolygonF()]]
        self.__q = QPointF(100, 100)
        self.__add_vertex = True
        self.__highlighted_indices = []

    def mousePressEvent(self, e):
        x = e.position().x()
        y = e.position().y()
        
        if self.__add_vertex:
            # Left click: add vertex
            if e.button() == Qt.MouseButton.LeftButton:
                self.__polygons[-1][-1].append(QPointF(x, y))
                
            # Right click: finish current ring, start drawing a hole
            elif e.button() == Qt.MouseButton.RightButton:
                if not self.__polygons[-1][-1].isEmpty():
                    self.__polygons[-1].append(QPolygonF())
                    
            # Middle click: finish whole polygon, start a completely new one
            elif e.button() == Qt.MouseButton.MiddleButton:
                # Remove last ring if it's empty
                if self.__polygons[-1][-1].isEmpty():
                    self.__polygons[-1].pop()
                # Start new polygon
                if self.__polygons[-1]:
                    self.__polygons.append([QPolygonF()])
        else: 
            # Move point q
            self.__q.setX(x)
            self.__q.setY(y)
                    
        self.repaint()

    def paintEvent(self, e):
        qp = QPainter(self)
        
        for i, complex_pol in enumerate(self.__polygons):
            if not complex_pol or complex_pol[0].isEmpty():
                continue
                
            qp.setPen(Qt.GlobalColor.black)
            
            # Highlight polygon if point is inside
            if i in self.__highlighted_indices:
                qp.setBrush(Qt.GlobalColor.cyan)
            else:
                qp.setBrush(Qt.GlobalColor.yellow)
                
            # Setup path for drawing holes
            path = QPainterPath()
            path.setFillRule(Qt.FillRule.OddEvenFill) 
            
            # Add all rings to path
            for ring in complex_pol:
                if not ring.isEmpty():
                    path.addPolygon(ring)
                    
            qp.drawPath(path)
        
        # Draw point q
        qp.setBrush(Qt.GlobalColor.green)
        r = 10
        qp.drawEllipse(int(self.__q.x() - r), int(self.__q.y() - r), 2 * r, 2 * r)
        
    def changeStatus(self):
        # Switch between drawing and moving point
        self.__add_vertex = not self.__add_vertex
        
    def clearData(self):
        # Clear all data on canvas
        self.__polygons = [[QPolygonF()]]
        self.__highlighted_indices.clear()
        self.__q.setX(-25)
        self.__q.setY(-25)
        self.repaint()
    
    def getQ(self):
        return self.__q
    
    def getPolygons(self):
        return self.__polygons
        
    def setHighlightedPolygons(self, indices):
        self.__highlighted_indices = indices
        self.repaint()
        
    def setPolygons(self, loaded_polygons):
        # Load polygons from external file
        self.__polygons = loaded_polygons
        self.__highlighted_indices.clear()
        self.repaint()