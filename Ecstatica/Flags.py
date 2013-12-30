# coding: utf-8

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import types

class Flags(object):
    '''
    Describes a 4byte field containing 32 flags
    '''
    
    def __init__(self, startval=None):
        if startval == None:
            startval = 0
        self.value = startval
        
        self._names = {} #in this dict we collect names for the entries to allow more intuitive access
        
    def __getitem__(self, idx):
        if type(idx) == str:
            assert idx in self.names.keys()
            idx = self._names[idx]
        
        assert idx >= 0 and idx < 32
        return self.value & (1 << idx)
    
    def __setitem__(self, idx, val):
        if type(idx) == str:
            assert idx in self.names.keys()
            idx = self._names[idx]

        assert idx >= 0 and idx < 32
        if val:        
            self.value |= (1 << idx)
        else:
            self.value &= ~(1 << idx)
                
    def __str__(self):
        str = ""
        for i in range(32):
            str += str(self.value & (1 << i))
        return str
    
    def clear(self):
        self.value = 0
        
    def clearSelected(self, vals):
        self.value &= ~vals
        
    def setSelected(self, vals):
        self.value |= vals
        
    def registerName(self, name, entry):
        '''
        allows to register a name for a given entry
        '''
        if name in self.names.keys():
            raise KeyError("Name in use already: " + name + ":" + self._names[name])
        if entry in self.names.values():
            raise ValueError("Entry has name already: " + filter(lambda e: e[1] == entry, self._names.entries())[0] + ":" + entry)
        
        self._names[name] = entry   
        
    def _getNames(self):
        return self._names
    
    def overwrite(self, newval):
        self.value = newval
    
    names = property(_getNames)     
