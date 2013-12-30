# coding: utf-8

#Created on 13.06.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import struct

class Graphic(object):
    '''
    Eine RAW-Grafik
    '''

    def __init__(self, width, height, xoff, yoff, palette, pixeldata):
        '''
        Constructor
        '''
        self.width = width
        self.height = height
        self.xoff = xoff
        self.yoff = yoff
        self.palette = palette
        self.pixeldata = pixeldata
        
        
def loadPalette(binary_dta):
    '''
    Eats 768 bytes and extract a RGB-tuple for every entry 
    '''
    assert len(binary_dta) == 768
    
    palette = []    
    for i in range(256):
        palette.append(struct.unpack("BBB", binary_dta[i*3:i*3+3]))
        
    return palette
        
        
def loadGraphic(filename):
    file = open(filename, "rb")
    header = file.read(8)
    width = struct.unpack(">h", file.read(2))[0]
    print(width)
    height = struct.unpack(">h", file.read(2))[0]
    print(height)
    unknown = file.read(20)
    palette = loadPalette(file.read(768))
    pixeldta = file.read(width*height)
    file.close()
    
    return Graphic(width, height, 0, 0, palette, pixeldta)

import unittest
        
class TestFANTFileLoader(unittest.TestCase):
    def testLoadGraphic(self):
        graphic = loadGraphic("test/title2.raw")
