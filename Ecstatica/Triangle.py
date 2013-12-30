# coding: utf-8

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

class Triangle(object):
    def __init__(self, actor, points_indices):
        self._actor = actor
        self._points_indices = points_indices
        
        self._front_color = None
        self._back_color = None
        
    def set_front_color(self, newcolor):
        self._color = newcolor    
    def get_front_color(self):
        return self._front_color    
    color = property(get_front_color, set_front_color)
    
    def set_back_color(self, newcolor):
        self._color = newcolor    
    def get_back_color(self):
        return self._back_color    
    color = property(get_back_color, set_back_color)
    
    def get_actor(self):
        return self._actor
    
    actor = property(get_actor)
    
    def get_points_indices(self):
        return self._points_indices
    
    points_indices = property(get_points_indices)
