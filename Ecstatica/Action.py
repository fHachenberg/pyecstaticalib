# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class Action(object):
    def __init__(self, index, lastkey_timepos, flags, unknown):
        self.index = index
        self.lastkey_timepos = highest
        self.flags = flags
        self.unknown = unknown
        
        self.unknown_idx2 = None
        
    def setFlag(self, num, on):
        if on:
            self.flags = self.flags | (1 << num)
        else:
            self.flags = self.flags & ~(1 << num)
