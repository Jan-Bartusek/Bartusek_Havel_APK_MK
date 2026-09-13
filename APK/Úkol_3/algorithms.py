from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from math import *
from edge import *
from triangle import *
import random

class Algorithms:
    
    def __init__(self):
        pass
    
    def getPointLinePosition(self, a, b, p):
        tolerance = 1.0e-6
        ux = b.x() - a.x()
        uy = b.y() - a.y()
        vx = p.x() - a.x()
        vy = p.y() - a.y()
        t = ux*vy - vx*uy
        if t > tolerance: return 1
        if t < -tolerance: return 0
        return -1
        
    def getNearestPoint(self, p, points):
        p_nearest = None
        d_min = inf
        for p_i in points:
            if p != p_i:            
                dx = p.x() - p_i.x()
                dy = p.y() - p_i.y()
                dist = sqrt(dx**2 + dy**2)
                if dist < d_min:
                    d_min = dist
                    p_nearest = p_i
        return p_nearest
    
    def get2LinesAngle(self, p1:QPointF, p2:QPointF, p3:QPointF, p4:QPointF):
        ux = p2.x() - p1.x()    
        uy = p2.y() - p1.y()
        vx = p4.x() - p3.x()
        vy = p4.y() - p3.y()    
        dot = ux*vx + uy*vy
        nu = (ux**2 + uy**2)**0.5
        nv = (vx**2 + vy**2)**0.5
        if nu * nv == 0: return 0
        arg = dot/(nu*nv)
        arg = max(-1, min(1,arg)) 
        return acos(arg)
    
    def findDelaunayPoint(self, p1, p2, points):
        p_dt = None
        phi_max = 0
        for p_i in points:
            if p_i != p1 and p_i != p2:
                if self.getPointLinePosition(p_i, p1, p2) == 1:
                    phi = self.get2LinesAngle(p_i, p2, p_i, p1)
                    if phi > phi_max:
                        phi_max = phi
                        p_dt = p_i
        return p_dt
                    
    def createDT(self, points):
        DT_edges = []
        DT_triangles = []
        AEL = [] 
        if len(points) < 3: return DT_edges, DT_triangles
        
        q = min(points, key=lambda k: k.y())   
        qn = self.getNearestPoint(q, points)       
        if qn is None: return DT_edges, DT_triangles
        
        e = Edge(q, qn)
        es = Edge(qn, q)  
        AEL.append(e)
        AEL.append(es) 
        
        while AEL:
            e1 = AEL.pop()
            e1s = e1.switchOrientation()
            p_dt = self.findDelaunayPoint(e1s.getStart(), e1s.getEnd(), points)
            
            if p_dt is None: continue
            
            e2 = Edge(e1s.getEnd(), p_dt)
            e3 = Edge(p_dt, e1s.getStart())
            
            DT_edges.extend([e1s, e2, e3])
            t = Triangle(e1s.getStart(), e1s.getEnd(), p_dt)
            DT_triangles.append(t)
                 
            self.updateAEL(e2, AEL)
            self.updateAEL(e3, AEL)
            
        return DT_edges, DT_triangles
    
    def updateAEL(self, e, AEL):
        es = e.switchOrientation()
        if es in AEL: AEL.remove(es)
        else: AEL.append(e) 
            
    def getContourPoint(self, p1, p2, z):
        xb = (p2.x() - p1.x())/(p2.z() - p1.z()) * (z - p1.z()) + p1.x()
        yb = (p2.y() - p1.y())/(p2.z() - p1.z()) * (z - p1.z()) + p1.y()
        return QPoint3DF(xb, yb, z)
    
    def createContourLines(self, DT, z_min, z_max, dz):
        contour_lines = []
        for z in range(z_min, z_max, dz):
            for i in range(0, len(DT), 3):
                if i+2 >= len(DT): break
                p1 = DT[i].getStart()
                p2 = DT[i+1].getStart()
                p3 = DT[i+1].getEnd()
                
                dz1, dz2, dz3 = z - p1.z(), z - p2.z(), z - p3.z()
                
                if dz1 == 0 and dz2 == 0 and dz3 == 0: continue
                elif dz1 == 0 and dz2 == 0: contour_lines.append(DT[i])
                elif dz2 == 0 and dz3 == 0: contour_lines.append(DT[i+1])
                elif dz3 == 0 and dz1 == 0: contour_lines.append(DT[i+2])
                elif (dz1*dz2 <= 0) and (dz2*dz3 <= 0): self.createContourLineSegment(p1, p2, p3, z, contour_lines)   
                elif (dz2*dz3 <= 0) and (dz3*dz1 <= 0): self.createContourLineSegment(p2, p3, p1, z, contour_lines)
                elif (dz3*dz1 <= 0) and (dz1*dz2 <= 0): self.createContourLineSegment(p3, p1, p2, z, contour_lines)
        return contour_lines
    
    def createContourLineSegment(self, p1, p2, p3, z, contour_lines):
        try:
            a = self.getContourPoint(p1, p2, z)
            b = self.getContourPoint(p2, p3, z)
            e = Edge(a, b)
            contour_lines.append(e)
        except ZeroDivisionError:
            pass

    def generateTerrain(self, terrain_type: str, num_points: int, width: float, height: float) -> list:
        points = []
        cx = width / 2.0
        cy = height / 2.0
        z_base = 300.0
        
        for _ in range(num_points):
            x = random.uniform(0, width)
            y = random.uniform(0, height)
            z = z_base
            
            if terrain_type == "Hill":
                amplitude = 250.0
                sigma = min(width, height) / 4.0
                z = z_base + amplitude * exp(-(((x - cx)**2 + (y - cy)**2) / (2 * sigma**2)))
            elif terrain_type == "Valley":
                amplitude = 150.0
                sigma_y = height / 4.0
                z = z_base + 150.0 - amplitude * exp(-((y - cy)**2 / (2 * sigma_y**2)))
                z -= (x / width) * 50.0
            elif terrain_type == "Ridge":
                amplitude = 200.0
                sigma_x = width / 2.0
                sigma_y = height / 8.0
                dx = (x - cx) * cos(pi/4) - (y - cy) * sin(pi/4)
                dy = (x - cx) * sin(pi/4) + (y - cy) * cos(pi/4)
                z = z_base + amplitude * exp(-((dx**2 / (2 * sigma_x**2)) + (dy**2 / (2 * sigma_y**2))))
            elif terrain_type == "Saddle":
                a = width / 3.0
                b = height / 3.0
                z = z_base + 35.0 * (((x - cx)**2 / (a**2 + 1e-6)) - ((y - cy)**2 / (b**2 + 1e-6)))
                
            z += random.uniform(-2.0, 2.0)
            points.append(QPoint3DF(x, y, z))
            
        return points
    
    def isPointInPolygon(self, p: QPointF, polygon: list) -> bool:
        # Ray-Casting algorithm for point in polygon test
        inside = False
        n = len(polygon)
        if n < 3: 
            return True # If polygon is not fully formed, treat as inside
        
        p1x, p1y = polygon[0].x(), polygon[0].y()
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n].x(), polygon[i % n].y()
            
            # Check if ray intersects the polygon edge
            if p.y() > min(p1y, p2y):
                if p.y() <= max(p1y, p2y):
                    if p.x() <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (p.y() - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or p.x() <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
            
        return inside
        
    def clipDT(self, dt_edges, dt_triangles, polygon):
        # Clip Delaunay Triangulation by non-convex polygon
        if len(polygon) < 3:
            return dt_edges, dt_triangles
            
        clipped_triangles = []
        
        for t in dt_triangles:
            # Calculate triangle centroid
            cx = (t.getP1().x() + t.getP2().x() + t.getP3().x()) / 3.0
            cy = (t.getP1().y() + t.getP2().y() + t.getP3().y()) / 3.0
            centroid = QPointF(cx, cy)
            
            # Keep triangle if its centroid is inside the polygon
            if self.isPointInPolygon(centroid, polygon):
                clipped_triangles.append(t)
                
        # Reconstruct edges list from the kept triangles
        edges_set = []
        for t in clipped_triangles:
            e1 = Edge(t.getP1(), t.getP2())
            e2 = Edge(t.getP2(), t.getP3())
            e3 = Edge(t.getP3(), t.getP1())
            
            for e in (e1, e2, e3):
                # duplicate check
                is_duplicate = False
                for existing_e in edges_set:
                    if e == existing_e or e == existing_e.switchOrientation():
                        is_duplicate = True
                        break
                if not is_duplicate:
                    edges_set.append(e)
                    
        return edges_set, clipped_triangles
    
    def isPointInPolygon(self, p, polygon: list) -> bool:
        # Ray-Casting algorithm for point in polygon test
        inside = False
        n = len(polygon)
        if n < 3: 
            return True # If polygon is not fully formed, treat as inside
        
        p1x, p1y = polygon[0].x(), polygon[0].y()
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n].x(), polygon[i % n].y()
            
            # Check if ray intersects the polygon edge
            if p.y() > min(p1y, p2y):
                if p.y() <= max(p1y, p2y):
                    if p.x() <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (p.y() - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or p.x() <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
            
        return inside
        
    def clipDT(self, dt_edges, dt_triangles, polygon):
        # Clip Delaunay Triangulation by non-convex polygon
        if len(polygon) < 3:
            return dt_edges, dt_triangles
            
        clipped_triangles = []
        
        for t in dt_triangles:
            # Calculate triangle centroid
            cx = (t.getP1().x() + t.getP2().x() + t.getP3().x()) / 3.0
            cy = (t.getP1().y() + t.getP2().y() + t.getP3().y()) / 3.0
            from PyQt6.QtCore import QPointF
            centroid = QPointF(cx, cy)
            
            # Keep triangle if its centroid is inside the polygon
            if self.isPointInPolygon(centroid, polygon):
                clipped_triangles.append(t)
                
        # Reconstruct edges list from the kept triangles
        edges_set = []
        for t in clipped_triangles:
            # Assuming Edge class is accessible here
            e1 = Edge(t.getP1(), t.getP2())
            e2 = Edge(t.getP2(), t.getP3())
            e3 = Edge(t.getP3(), t.getP1())
            
            for e in (e1, e2, e3):
                # Simple duplicate check
                is_duplicate = False
                for existing_e in edges_set:
                    if e == existing_e or e == existing_e.switchOrientation():
                        is_duplicate = True
                        break
                if not is_duplicate:
                    edges_set.append(e)
                    
        return edges_set, clipped_triangles