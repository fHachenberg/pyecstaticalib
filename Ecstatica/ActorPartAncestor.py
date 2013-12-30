# coding: utf-8

#Created on 06.10.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import weakref

from . import Flags

class ActorPartAncestor(object):
    '''
    This class is the common ancestor of Actor and Part. It could be possible that Ecstatica didn't actually
    use subclassing but had Part and Actor each have an instance of this class at offset 0x0h...no, that does not
    seem plausible.
    '''

    def __init__(self, index, parent, actor, flags):
        '''
        Constructor
        '''
        self.idx = index
        self.flags = Flags.Flags(flags) #there are 2 bytes of flags at offset +0x02h        
        
        #self.matrix_gbl = (0, 0, 0, 0, 0, 0, 0, 0, 0)   #rotation matrix into global coordinate system
        self.origin_lcl = (0, 0, 0)                     #translatin part into global coordinate system
        self.offset_lcl = (0, 0, 0)
        
        self.sub = None #points to another ActorPartAncestor, which can be an Actor or a Part
        self.actor = actor  #points to the actor this object belongs to. For the actor himself, this pointer is None
                            #(originally, in Ecstatica, it points to the actor objects itself)
        self.rotation = (0, 0, 0)                       #angles to describe the rotation of the object
        self.parent = parent
        
        self.primechild = None
        self.silblings = []
        
        self.typeinfo = None
        
    #Flags at Offset 0x02h    
    flagnames = {"PartIsLoose": 4, 
    "PartIs2PartLimb": 5,
    "PartIsFixed": 6,
    "PartFixedIKZAxis": 7} #Not certain yet what exactly this means
    
    def setFlags(self, flag_word):
        '''
        Activates all flags for which a 1 appears in the flag_word. Does NOT clear flags
        
        @param flag_word: Flags 0-15 to set
        '''
        for i in range(16):
            flagvalue = flag_word & (1 << i)
            if flagvalue == 1:
                self.flagnames[i] = True    
                
    def clearFlags(self, flag_word):
        '''
        Clears all flags for which a 1 appears in the flag_word. Does NOT set flags
        
        @param flag_word: Flags 0-15 to clear
        '''
        for i in range(16):
            flagvalue = flag_word & (1 << i)
            if flagvalue == 1:
                self.flagnames[i] = False
        
    def addChild(self, childpart):             
        assert childpart != None
        assert childpart.parent is self
        assert not childpart is self
        
        if self.primechild != None:
            self.primechild.addSilbling(childpart)
        else:
            self.primechild = childpart
            
    def _getChildren(self):
        if self.primechild == None:
            return []
        else:
            return [self.primechild, ] + self.primechild.silblings
        
    children = property(_getChildren)
            
    def addSilbling(self, silblingpart):
        assert silblingpart != None
        assert silblingpart.parent is self.parent
        assert not silblingpart is self
        
        self.silblings.append(silblingpart)
