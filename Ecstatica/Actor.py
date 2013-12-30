# coding: utf-8

#Created on 12.04.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from __future__ import absolute_import

from . import Event

from .ActorPartAncestor import ActorPartAncestor

class Actor(ActorPartAncestor):
    def __init__(self, idx, flags, position, rotation):
        ActorPartAncestor.__init__(self, idx, None, None, flags)
        
        self.position = position
        self.rotation = rotation
        
        self.flags.registerName("updprttrafo_uk", 5)
        self.flags.registerName("unknown_flag_400", 10)
        
        self.points = {}
        self.triangles = {}

def extractActorDefinitions(events):
    '''
    provides an iterator over a sequence of actor definitions. Returns Actor Definition event lists (sublists)
    '''
    actrdeflist = None
    for event in events:   
        if event.event_type == Event.ev_ADD_THING:
            if actrdeflist != None:                
                yield actrdeflist
            actrdeflist = [event]            
        else:
            if actrdeflist == None:
                continue
            actrdeflist.append(event)
    if actrdeflist != None:                
        yield actrdeflist
        
import unittest
        
class Test_extractActorDefinitions(unittest.TestCase):
    def test_ADD_THING_included(self):
        '''
        The opening ADD_THING-Event is always included in the list of actor definition events
        '''
        events = [Event.Event(0, Event.ev_ADD_THING, 0, 0, 0), Event.Event(0, Event.ev_ADD_THING, 0, 0, 0)]
        output = list(extractActorDefinitions(events))
        correct_output = [[events[0]], [events[1]]]
        self.assertEqual(output, correct_output, "")
