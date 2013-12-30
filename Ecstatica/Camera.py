# coding: utf-8

#Created on 04.03.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class Camera(object):
    def __init__(self, position, angles, f):
        self.position = position
        self.angles = angles
        self.f = f
        
    def __str__(self):
        stri =  "Camera\n" + "Position=" + str(self.position) + "\n" + "Angles=" + str(self.angles) + "\n" + "f=" + str(self.f)
        return stri
    
    def __eq__(self, other):
        if self.position != other.position:
            return False
        
        if self.angles != other.angles:
            return False
        
        if self.f != other.f:
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
def createCameraFromText(position_text, angles_text, f_text):
    '''
    Expected following arguments
    position: Vector3-String "<x>,<y>,<z>"
    angles: Vector3-String "<x>,<y>,<z>"
    f: String of floating point number
    '''
    
    position = (float(a) for a in position_text.split(','))
    angles = ( float(a) for a in angles_text.split(','))
    f = float(f_text)
    return Camera(position, angles, f)

    
