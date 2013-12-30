# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class Sound(object):
    def __init__(self, index, length, unknown, unknown1, data, flags):
        self.index = index
        self.length = length
        self.unknown = unknown
        self.unknown1 = unknown1
        self.data = data
        self.flags = flags
        
        #print "created sound object of size", len(self.data)
        
    def __eq__(self, other):
        if self.index != other.index:
            print("indices deviate")
            return False
        
        if self.length != other.length:
            print("length deviates")
            return False
        
        if self.unknown != other.unknown:
            print("unknown deviates")
            return False
        
        if self.unknown1 != other.unknown1:
            print("unknown1 deviates:", self.unknown1, " vs ", other.unknown1)
            return False
        
        if self.data != other.data:
            print("data deviates")
            return False
        
        if self.flags != other.flags:
            print("flags deviate")
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)            
