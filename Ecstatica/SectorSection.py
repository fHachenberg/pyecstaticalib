# coding: utf-8

#Created on 22.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from . import Fixpoint

class SectorSection(object):
    '''
    This is a sector
    '''

    def __init__(self, prio, section, unknown1, cam_idx, y_uk, ymax, codeidx_plus_one, flags):
        '''
        Constructor
        '''
        object.__init__(self)
        self.prio = prio
        self.section = section
        self.unknown1 = unknown1
        self.cam_idx = cam_idx
        self.y_uk = y_uk
        self.ymax = ymax
        self.codeidx_plus_one = codeidx_plus_one
        self.flags = flags
        
    def _getYRange(self):
        '''
        Returns the range [y_uk, ymax] as floating point values
        
        The transformation is based on experiments using Blender.
        It is nontheless independent of Blender!
        '''
        #Why this condition here?
        #I don't completely get it yet, but in Ecstatica by some wrap-around-byte-effect
        #or something like this the effect of getting a height value from the sectorsections
        #results in a behaviour like the following.
        #I got to this by trial-and-error        
        assert self.y_uk >= 0 and self.y_uk < 256
        assert self.ymax >= 0 and self.ymax < 256        
        
        y = Fixpoint.tofloat((128 - self.y_uk) * 128)
        ym = Fixpoint.tofloat((128 - self.ymax ) * 128)                
        assert y <= ym 
        
        return [ym, y]
    yrange = property(_getYRange)
        
    def _isEndOfSequence(self):
        '''
        Returns True, if this SectorSection is the end of a
        sequence of sections
        '''
        return self.codeidx_plus_one & (1<<7)
        
    #True is this is the last section in the sequence of sections
    endofseq = property(_isEndOfSequence)
    
    def _getCollisionInfo(self):
        '''
        Depending on the type of segmentation, returns
        3 different kinds of lists:
            [1, <Bool>] is section is monolithic
            [2, [<x>z>, <x<-z>, <x>=-z>, <x<=z>]] if section is 
                diagonally segmented
            [4, [<x<0,z<0>,<x<0,z>0>,<x>0,z<0>,<x>0,z>0>] if section
                is segmented into quadrants
        '''
        if self.section == 0:
            return [1, False]
        elif self.section == 1:
            return [1, True]
        elif self.section == 2:
            return [2, [True, False, False, False]]
        elif self.section == 3:
            return [2, [False, True, False, False]]
        elif self.section == 4:
            return [2, [False, False, True, False]]
        elif self.section == 5:
            return [2, [False, False, False, True]]
        else: #sector is segmented into quadrants
            return [4, [self.section & 2 != 0,
                        self.section & 8 != 0,
                        self.section & 1 != 0,
                        self.section & 4 != 0]]
                        
    collisioninfo = property(_getCollisionInfo)
            
    def isActive(self, subposition, y):
        '''
        Looks up the structure within this sector 
        @param subposition: The position in sector coordinates
        @return:    True if the position is valid within this sector
                    False else                
        '''        
        if int(128 - y*128) + 1 >= self.y_max:
            return False
        
        if self.section == 0:
            return False
        elif self.section == 1:
            return True
        elif self.section == 2:
            return subposition[0] > subposition[1]
        elif self.section == 3:
            return subposition[0] < -subposition[1]
        elif self.section == 4:
            return subposition[0] >= -subposition[1]
        elif self.section == 5:
            return subposition[0] <= subposition[1]
        else: #sector is segmented into quadrants
            if subposition[0] < 0:
                if subposition[1] < 0:
                    return self.section & 2
                else:
                    return self.section & 8                    
            else:
                if subposition[1] < 0:
                    return self.section & 1
                else:
                    return self.section & 4

    def __hash__(self):
        return object.__hash__(self)
        
    def __eq__(self, other):
        return object.__eq__(self, other)
        
        if self.prio != other.prio:
            return False                
        
        if self.section != other.section:
            return False
        
        if self.unknown1 != other.unknown1:
            return False
        
        if self.unknown2 != other.unknown2:
            return False
        
        if self.y_uk != other.y_uk:
            return False
        
        if self.ymax != other.ymax:
            return False
        
        if self.codeidx_plus_one != other.codeidx_plus_one:
            return False
        
        if self.flags != other.flags:
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)

def getAllSectorSections(sectorsections, sector_index, max_index):    
    assert sector_index <= max_index
    sector_lst = []
    for i in range(sector_index, max_index+1):             
        sector = sectorsections[i]        
        sector_lst.append(sector)
        if sector.endofseq:
            break    
    return sector_lst

def getRelevantSectorSection(sectorsections, sector_index, max_index, subposition, y):
    '''
    Takes the sector_index and returns the relevant section
    @param sectorsections: Array of sector sections
    @param sector_index: valid index into the sectorsections array
    @param max_index: maximum allowed indes in sectorsections array
    @param subposition: subposition within sector given by sector_index.
    @param y: y coordinate
    '''
    sector_lst = getAllSectorSections(sectorsections, sector_index, max_index)
    
    valid_sectors = filter(lambda s: s.isActive(subposition, y), sector_lst)
    max_sector = max(lambda s: s.y_max, valid_sectors)
    return max_sector
    
def getRelevantSector(sectormap, position):
        '''
        @return:    True if the position is inside this sector
                    False else
        '''
        return sectormap[int(position[0]/32.0) + 64 + (int(position[1]/32.0) + 64)*128]
    
