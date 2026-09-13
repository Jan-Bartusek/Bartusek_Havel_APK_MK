from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from qpoint3df import *
from math import *

class Triangle:
    def __init__(self, p1: QPoint3DF, p2: QPoint3DF, p3: QPoint3DF):
        self.__p1 = p1
        self.__p2 = p2
        self.__p3 = p3
        
        # Default values
        self.__slope = 0.0   
        self.__aspect = -1.0 
        
        # Automatic geometry calculation immediately after triangle creation
        self.calculateGeometry()
        
    def calculateGeometry(self):
        # 1. Compute direction vectors for two triangle edges
        ux = self.__p2.x() - self.__p1.x()
        uy = self.__p2.y() - self.__p1.y()
        uz = self.__p2.z() - self.__p1.z()
        
        vx = self.__p3.x() - self.__p1.x()
        vy = self.__p3.y() - self.__p1.y()
        vz = self.__p3.z() - self.__p1.z()
        
        # 2. Cross product to get the surface normal (perpendicular to the triangle)
        nx = uy * vz - uz * vy
        ny = uz * vx - ux * vz
        nz = ux * vy - uy * vx
        
        norm_xy = sqrt(nx**2 + ny**2)
        
        # 3. Compute slope in degrees
        if nz != 0:
            self.__slope = atan(norm_xy / abs(nz)) * (180 / pi)
        else:
            self.__slope = 90.0 # Vertical wall
            
        # 4. Compute aspect (azimuth) in degrees
        if norm_xy > 1e-9:
            aspect_rad = atan2(nx, ny)
            self.__aspect = aspect_rad * (180 / pi)
            # Convert to positive angles (0 - 360)
            if self.__aspect < 0:
                self.__aspect += 360
        else:
            # A flat plane has no aspect
            self.__aspect = -1.0

    # Getters to retrieve values
    def getP1(self): return self.__p1
    def getP2(self): return self.__p2
    def getP3(self): return self.__p3
    def getAspect(self): return self.__aspect
    def getSlope(self): return self.__slope