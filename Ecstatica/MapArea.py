# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class MapArea(object):
    '''
    classdocs
    '''

    def __eq__(self, other):
        if self.index != other.index:
            return False
        
        if self.values != other.values:
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)

    def __init__(self, index, values):
        '''
        Constructor
        '''
        self.index = index
        self.values = values
