# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

Actions = [None]*1000
Actors = [None]*1000

MainActor = None

class NamesDB(object):
    def __init__(self, nametype):
        self.nametype = nametype
        self.indices = {}
        self.names = []
        
    def addName(self, name):
        '''
        Checks whether name is existing already in the DB and returns
        its index in this case. Otherwise it adds it to the DB and
        returns the new index
        '''
        if name in self.indices.keys():
            return self.indices[name]
        else:
            newindex = len(self.indices)
            self.indices[name] = newindex
            self.names.append(name)
            return newindex
        
    def addNames(self, namelist):
        '''
        Adds a list of names to the DB and returns a number of indices
        '''
        idxs = []
        
        for name in namelist:
            idxs.append(self.addName(name))
            
        return idxs
        
    def __getitem__(self, name):
        '''
        Overload [] operator
        '''
        
        return self.addName(name)  
    
    def __len__(self):
        return len(self.names)      
    
    def append(self, name):
        '''
        Imitate list operation "append"
        '''
        
        return self.addName(name)
        
    def __str__(self):
        liste=[]
        for entry in self.indices.keys():
            liste.append(entry)
        return "\n".join(liste)
    
    def __iter__(self):
        return self.names.__iter__()
    
    def __next__(self):
        return self.names.__next__()
    
    def __eq__(self, other):
        if self.nametype != other.nametype:
            print("Name type not equal")
            return False
        if self.indices != other.indices:
            print("indices not equal")
            return False
        if self.names != other.names:
            print("names not equal")
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
            
partnames = NamesDB('Part')
actornames = NamesDB('Actor')
actionnames = NamesDB('Action')
scenenames = NamesDB('Scene')
pointnames = NamesDB('Point')
trinames = NamesDB('Triangle')
codenames = NamesDB('Code')
repertnames = NamesDB('Repertoire')
soundnames = NamesDB('Sound')
mapareanames = NamesDB('MapArea')

import unittest
                        
class TestNamesDB(unittest.TestCase):
    def testAddName(self):
        db = NamesDB('test')
        for i in range(100):
            string = str(i)
            index = i
            
            name = string
            created_index = db.addName(name)            
            self.assertEqual(created_index, index, "i-th-added string is mapped to i-th position")
            self.assertEqual(db.names[index], string, "i-th-added string appear at i-th position")
                        
