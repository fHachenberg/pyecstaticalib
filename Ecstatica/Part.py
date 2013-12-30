# coding: utf-8

#Created on 19.08.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from __future__ import absolute_import

from .ActorPartAncestor import ActorPartAncestor
from .Flags import Flags

class Part(ActorPartAncestor):
    '''
    Represents an ecstatica ellipse
    '''
    def __init__(self, idx, flags, origin_lcl, centre_lcl, offset_lcl, halfaxes, rotation, colour, parent, actor):
        '''
        '''
        ActorPartAncestor.__init__(self, idx, parent, actor, flags)
        
        self.idx = idx
        
        self._origin_lcl = origin_lcl
        self.centre_lcl = centre_lcl
        self.offset_lcl = offset_lcl        
        
        self._rotation = rotation            
        
        self._halfaxes = halfaxes
        self._colour = colour
        
        self.pSub = None
        self.next_silbling = None
        
        self.points = []
        
        self.flags.registerName("unknown_pos_flag_2", 1)        
        self.flags.registerName("joint_is_loose", 4)
        self.flags.registerName("is_2part_limb",  5)
        self.flags.registerName("part_is_fixed", 6)
        self.flags.registerName("unknown_rot_flag_200", 9)        
        self.flags.registerName("unknown_rot_flag_4000", 14)
        
        self.updateflags = Flags()
        self.updateflags.registerName("origin_lcl", 0)
        self.updateflags.registerName("rotation", 1)            
        self.updateflags.registerName("offset_lcl", 2)
        self.updateflags.registerName("centre_lcl", 3)
        self.updateflags.registerName("halfaxes", 4)
        self.updateflags.registerName("colour", 5)
        self.updateflags.registerName("unknown_40", 6)
        self.updateflags.registerName("unknown_80", 7)   
        
        self._rescaled_offset_lcl = map(lambda (x,y): x/y, zip(self.offset_lcl, self.parent.halfaxes))
        
    def _get_origin_lcl(self):
        return self._origin_lcl    
    def _set_origin_lcl(self, newval):
        self._origin_lcl = newval
        self.flags['unknown_pos_flag_2'] = False
        self.flags['part_is_fixed'] = False
        self.updateflags['origin_lcl'] = True
    origin_lcl = property(_get_origin_lcl, _set_origin_lcl)    
        
    def _get_offset_lcl(self):
        return self._offset_lcl    
    def _set_offset_lcl(self, newval):
        self._offset_lcl = newval
        self.updateflags['offset_lcl'] = True
    offset_lcl = property(_get_offset_lcl, _set_offset_lcl)
        
    def _get_rotation(self):
        return self._rotation    
    def _set_rotation(self, newval):
        self._rotation = newval
        self.flags['unknown_rot_flag_200'] = False
        self.flags['unknown_rot_flag_4000'] = False
        self.updateflags['rotation'] = True        
    rotation = property(_get_rotation, _set_rotation)

    def _get_colour(self):
        return self._colour    
    def _set_colour(self, newval):
        self._colour = newval        
        self.updateflags['colour'] = True        
    colour = property(_get_colour, _set_colour)
    
    def _get_halfaxes(self):
        return self._halfaxes 
    def _set_halfaxes(self, newval):
        self._halfaxes = newval
        self.updateflags['halfaxes'] = True
    halfaxes = property(_get_halfaxes, _set_halfaxes)

    def __str__(self):
        flagnames = list(map(lambda item: (item[0], self.flags[item[1]]), Part.flagnames.items()))
        active_flagnames = list(map(lambda item: item[0], filter(lambda item: item[1], flagnames)))
        return "Part object " + "origin_lcl: " + str(self.origin_lcl) + ", " + "centre_lcl: " + str(self.centre_lcl) + ", " + "halfaxes:   " + str(self.halfaxes) + ", " + "colour:     " + str(self.colour) + ", " + "flags: " + ", ".join(active_flagnames)        
    
#these are part flag values
flag_joint_is_loose = 0x10 
flag_is_2part_limb  = 0x20                   
