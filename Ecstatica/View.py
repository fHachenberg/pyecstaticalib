# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import struct
import itertools

from . import Camera
from . import PixelEncoding
from . import Fixpoint
#import Camera
#import PixelEncoding
#import Fixpoint

class View(object):
    '''
    Represents the combination of color-, z- and camera data for a specific view point
    '''
    def __init__(self, colordata, zdata, camera):
        self.colordata = colordata
        self.zdata = zdata
        self.camera = camera
    
def loadView(camera, viewfileobj):
    assert type(camera) == Camera.Camera
    
    typemark = viewfileobj.read(2)    
    if typemark == "hm":
        bytes_b = viewfileobj.read(30)
        bytes_c = viewfileobj.read(768)
        bytes_d = viewfileobj.read(64000)
        bytes_e = viewfileobj.read(128000)
    
        bufferlen = struct.unpack("<h", viewfileobj.read(2))[0]
        structstr = ">" + "".join(itertools.repeat("h", bufferlen))
        packed_zdata = struct.unpack(structstr, viewfileobj.read(bufferlen*2))
    else:
        len_a = struct.unpack("<i", viewfileobj.read(4))[0]
        len_b = struct.unpack("<i", viewfileobj.read(4))[0]
        #print(len_a, len_b)
                        
        packed_colordta = viewfileobj.read(len_a)
        colordata = PixelEncoding.decodePixels(packed_colordta)
        #str(colordata) is necessary to execute the code in python 2.7
        cdata = struct.unpack("".join(itertools.repeat("B", 320*200)), colordata) 
        packed_depthdta = viewfileobj.read(len_b)        
        depthdta = PixelEncoding.decodePixelsWords(packed_depthdta)
        zdata = list(map(lambda z: Fixpoint.tofloat(z), depthdta))
        
        bufferlen = struct.unpack("<h", viewfileobj.read(2))[0]
        print(bufferlen)
        #TODO(completeness) read in the rest of the file!
        
    return View(cdata, zdata, camera)
        
import unittest

class TestView(unittest.TestCase):
    def test_loadView(self):
        loadView(Camera.Camera((0,0,0),(0,0,0),1.0), open("test/views/0002.raw", "rb"))
