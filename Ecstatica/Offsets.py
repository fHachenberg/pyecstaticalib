# coding: utf-8

#Created on 06.04.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import struct
import itertools
import unittest

class Offsets(object):
    '''
    classdocs
    '''


    def __init__(self, actions, actors, scenes, reperts, sounds, unknown):
        '''
        Constructor
        '''
        self.actions = actions
        self.actors = actors
        self.scenes = scenes
        self.reperts = reperts
        self.sounds = sounds
        self.unknown = unknown
        
        
    def __str__(self):
        outstr = "Offsets collection:"
        outstr += str(len(self.actions)) + " Actions, "
        outstr += str(len(self.actors)) + " Actors, "
        outstr += str(len(self.scenes)) + " Scenes, "
        outstr += str(len(self.reperts)) + " Scenes, "
        outstr += str(len(self.sounds)) + " Sounds, "
        outstr += str(len(self.unknown)) + " Unknowns"
        return outstr
        
        
def loadOffsets(filename):
    fileobj = open(filename, "rb")
    
    scenes  = struct.unpack(">"+"".join(itertools.repeat("I", 1000)), fileobj.read(4*1000))
    actors  = struct.unpack(">"+"".join(itertools.repeat("I", 500)), fileobj.read(4*500))
    actions = struct.unpack(">"+"".join(itertools.repeat("I", 1000)), fileobj.read(4*1000))
    reperts = struct.unpack(">"+"".join(itertools.repeat("I", 150)), fileobj.read(4*150))
    sounds  = struct.unpack(">"+"".join(itertools.repeat("I", 500)), fileobj.read(4*500))
    unknown = struct.unpack(">"+"".join(itertools.repeat("I", 375)), fileobj.read(4*375)) 
    
    fileobj.close()
    
    return Offsets(actions, actors, scenes, reperts, sounds, unknown)

class TestLoadXML(unittest.TestCase):
    def test_load_offsets(self):
        offsets = loadOffsets("test/offsets.")
        print(offsets)
        print(offsets.actors)
        off2 = loadOffsets("test/off2.")
        print(off2)
        print(off2.actors)
        
