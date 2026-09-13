from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from random import *
from math import *
from triangle import *

class Draw(QWidget):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__points = []
        self.__DT = []          
        self.__triangles = []   
        self.__contours = []
        self.__polygon = []     # New list for the clipping polygon
        
        self.__view_dt = True
        self.__view_contours = True
        self.__view_slope = False
        self.__view_aspect = False
        self.__view_hypsometry = False
        self.__view_3d = False
        
    def mousePressEvent(self, e):
        x, y = e.position().x(), e.position().y()
        
        # Left click: Add terrain point
        if e.button() == Qt.MouseButton.LeftButton:
            z = random() * 400 + 200 
            self.__points.append(QPoint3DF(x, y, z))
            
        # Right click: Add boundary polygon vertex
        elif e.button() == Qt.MouseButton.RightButton:
            self.__polygon.append(QPointF(x, y))
            
        self.repaint()

    def paintEvent(self, e):
        qp = QPainter(self)
        qp.begin(self)
        qp.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        if self.__view_3d:
            self.draw3D(qp)
            qp.end()
            return
            
        if self.__view_slope: self.drawSlope(qp)
        elif self.__view_aspect: self.drawAspect(qp)
        elif self.__view_hypsometry: self.drawHypsometry(qp)
            
        if self.__view_dt:
            pen = QPen(Qt.GlobalColor.green, 1)
            qp.setPen(pen)
            for edge in self.__DT:
                qp.drawLine(edge.getStart(), edge.getEnd())
            
        if self.__view_contours:
            qp.setFont(QFont("Arial", 8, QFont.Weight.Bold))
            drawn_labels = []
            for c in self.__contours:
                p1, p2 = c.getStart(), c.getEnd()
                z = int(p1.z())
                
                if z % 100 == 0:
                    pen = QPen(Qt.GlobalColor.black, 2)
                    is_major = True
                else:
                    pen = QPen(Qt.GlobalColor.gray, 1)
                    is_major = False
                    
                qp.setPen(pen)
                qp.drawLine(p1, p2)
                
                dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
                if is_major and sqrt(dx**2 + dy**2) > 30:
                    cx, cy = (p1.x() + p2.x()) / 2.0, (p1.y() + p2.y()) / 2.0
                    too_close = any(sqrt((cx - lx)**2 + (cy - ly)**2) < 70 for lx, ly in drawn_labels)
                    
                    if not too_close:
                        drawn_labels.append((cx, cy))
                        angle = atan2(dy, dx) * 180 / pi
                        if angle > 90: angle -= 180
                        elif angle < -90: angle += 180
                        
                        qp.save()
                        qp.translate(cx, cy)
                        qp.rotate(angle)
                        qp.setBrush(Qt.GlobalColor.white)
                        qp.setPen(Qt.PenStyle.NoPen)
                        qp.drawRect(QRectF(-12, -7, 24, 14))
                        qp.setPen(Qt.GlobalColor.black)
                        qp.drawText(QRectF(-15, -10, 30, 20), Qt.AlignmentFlag.AlignCenter, str(z))
                        qp.restore()
        
        # Draw terrain points
        pen = QPen(Qt.GlobalColor.red, 4)
        qp.setPen(pen)
        qp.drawPoints(self.__points)
        
        # Draw the clipping polygon (in blue)
        if self.__polygon:
            pen = QPen(Qt.GlobalColor.blue, 2, Qt.PenStyle.DashLine)
            qp.setPen(pen)
            qp.setBrush(Qt.BrushStyle.NoBrush)
            qp.drawPolygon(QPolygonF(self.__polygon))
            
            pen = QPen(Qt.GlobalColor.blue, 6)
            qp.setPen(pen)
            for p in self.__polygon:
                qp.drawPoint(int(p.x()), int(p.y()))
                
        qp.end()

    def projectTo3D(self, p, w, h):
        cx, cy = w / 2.0, h / 2.0
        scale = 0.5 
        x = (p.x() - cx) * scale
        y = (p.y() - cy) * scale
        z = p.z() * scale
        iso_x = (x - y) * cos(pi/6)
        iso_y = (x + y) * sin(pi/6) - z
        return QPointF(iso_x + cx, iso_y + cy + 100)

    def draw3D(self, qp):
        if not self.__triangles: return
        w, h = self.width(), self.height()
        
        # Třídění Malířovým algoritmem pomocí exaktního 2D těžiště
        # OPRAVA: reverse=False vykreslí nejprve vzdálené trojúhelníky a až nakonec ty blízké
        sorted_triangles = sorted(self.__triangles, key=lambda t: 
    (t.getP1().x() + t.getP2().x() + t.getP3().x()) / 3.0 + 
    (t.getP1().y() + t.getP2().y() + t.getP3().y()) / 3.0 +
    (t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0, 
    reverse=True
)
        
        z_min = min((t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0 for t in sorted_triangles)
        z_max = max((t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0 for t in sorted_triangles)
        dz = max(z_max - z_min, 1.0)
        
        qp.setPen(QPen(Qt.GlobalColor.black, 1)) 
        
        for t in sorted_triangles:
            # OPRAVA: Odstranění "sliver triangles" - výpočet délky 2D hran
            dx1, dy1 = t.getP1().x() - t.getP2().x(), t.getP1().y() - t.getP2().y()
            dx2, dy2 = t.getP2().x() - t.getP3().x(), t.getP2().y() - t.getP3().y()
            dx3, dy3 = t.getP3().x() - t.getP1().x(), t.getP3().y() - t.getP1().y()
            
            dist1 = (dx1**2 + dy1**2)**0.5
            dist2 = (dx2**2 + dy2**2)**0.5
            dist3 = (dx3**2 + dy3**2)**0.5
            
            # Zvýšený limit na 350 - odfiltruje pouze extrémní hraniční trojúhelníky
            if dist1 > 350 or dist2 > 350 or dist3 > 350:
                continue

            # Promítnutí do 3D (izometrie)
            p1_3d = self.projectTo3D(t.getP1(), w, h)
            p2_3d = self.projectTo3D(t.getP2(), w, h)
            p3_3d = self.projectTo3D(t.getP3(), w, h)
            
            # Výpočet barvy na základě výšky
            avg_z = (t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0
            norm_z = (avg_z - z_min) / dz
            hue = int(120 - norm_z * 120)
            saturation = 255 if norm_z <= 0.8 else int(255 * (1.0 - (norm_z - 0.8) * 5))
            color = QColor.fromHsv(max(0, min(359, hue)), max(0, min(255, saturation)), 255)
            
            qp.setBrush(QBrush(color))
            qp.drawPolygon(QPolygonF([p1_3d, p2_3d, p3_3d]))

    def drawHypsometry(self, qp):
        if not self.__triangles: return
        z_min = min((t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0 for t in self.__triangles)
        z_max = max((t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0 for t in self.__triangles)
        dz = max(z_max - z_min, 1.0)
        
        for t in self.__triangles:
            avg_z = (t.getP1().z() + t.getP2().z() + t.getP3().z()) / 3.0
            norm_z = (avg_z - z_min) / dz
            hue = int(120 - norm_z * 120)
            saturation = 255 if norm_z <= 0.8 else int(255 * (1.0 - (norm_z - 0.8) * 5))
            color = QColor.fromHsv(max(0, min(359, hue)), max(0, min(255, saturation)), 255)
            self.fillTriangle(qp, t, color)

    def drawSlope(self, qp):
        if not self.__triangles: return
        
        # Determine the true slope extremes in the current terrain
        s_min = min(t.getSlope() for t in self.__triangles)
        s_max = max(t.getSlope() for t in self.__triangles)
        ds = max(s_max - s_min, 0.1) 
        
        for t in self.__triangles:
            slope = t.getSlope()
            
            # Normalize slope to the range <0.0, 1.0>
            norm_s = (slope - s_min) / ds
            
            # Use HSV model for a brighter, more vivid color scale
            # Hue 120 = green, Hue 60 = yellow, Hue 30 = orange, Hue 0 = red
            hue = int(120 - norm_s * 120)
            
            # Set saturation and value to maximum (255) for bright colors
            color = QColor.fromHsv(max(0, min(120, hue)), 255, 255)
            
            self.fillTriangle(qp, t, color)

    def drawAspect(self, qp):
        for t in self.__triangles:
            aspect = t.getAspect()
            color = Qt.GlobalColor.white if aspect == -1 else QColor.fromHsv(int(aspect), 255, 255)
            self.fillTriangle(qp, t, color)

    def fillTriangle(self, qp, t, color):
        qp.setBrush(QBrush(color))
        qp.setPen(Qt.PenStyle.NoPen)
        qp.drawPolygon(QPolygonF([t.getP1(), t.getP2(), t.getP3()]))

    def setDT(self, DT_edges, DT_triangles):
        self.__DT = DT_edges
        self.__triangles = DT_triangles
        
    def getDT(self): return self.__DT
    def getPoints(self): return self.__points
    def getPolygon(self): return self.__polygon # New getter
    def setContours(self, contours): self.__contours = contours

    def setViewSettings(self, dt, contours, slope, aspect, hypsometry, view_3d):
        self.__view_dt = dt
        self.__view_contours = contours
        self.__view_slope = slope
        self.__view_aspect = aspect
        self.__view_hypsometry = hypsometry
        self.__view_3d = view_3d

    def clearResult(self):
        # clear only the results
        self.__DT.clear()
        self.__triangles.clear()
        self.__contours.clear()
        self.repaint()

    def clearAll(self):
        # comlete erase Clear All
        self.clearResult()
        self.__points.clear()
        self.__polygon.clear() 
        self.repaint()

    