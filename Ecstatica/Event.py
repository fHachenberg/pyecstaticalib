# coding: utf-8

#Created on 18.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import itertools

class EventType(object):
    def __init__(self, typeid, index_type, value1_type, value2_type, value3_type, priority):
        self.typeid = typeid
        
        self.index_type = index_type
        self.value1_type = value1_type
        self.value2_type = value2_type
        self.value3_type = value3_type  

EventTypeName = {       "ev_NO_EVENT":          EventType(0, None, None, None, None,    0),
                        "ev_ROTATE":            EventType(1, None, None, None, None,    0),
                        "ev_OFFSET":            EventType(2, None, None, None, None,    0),
                        "ev_COLOUR":            EventType(3, None, None, None, None,    0),
                        "ev_VECTOR1":           EventType(4, None, None, None, None,    0),
                        "ev_VECTOR2":           EventType(5, None, None, None, None,    0),
                        "ev_VECTOR3":           EventType(6, None, None, None, None,    0),
                        "ev_ADD_PART":          EventType(7, None, None, None, None,    -1),
                        "ev_ADD_THING":         EventType(8, None, None, None, None,    0),
                        "ev_TYPE":              EventType(9, None, None, None, None,    0),
                        "ev_ADD_PART_TO_THING": EventType(10, None, None, None, None,   0),
                        "ev_PSEUDO_ACTION":     EventType(11, None, None, None, None,   0),
                        "ev_PSEUDO_KEY":        EventType(12, None, None, None, None,   0),
                        "ev_DISP_PNT":          EventType(13, None, None, None, None,   0),
                        "ev_FLAGS":             EventType(14, None, None, None, None,   0),
                        "ev_MOVE_ACT":          EventType(15, None, None, None, None,   0),
                        "ev_RAND_ACT":          EventType(16, None, None, None, None,   0),
                        "ev_RAND_INFO":         EventType(17, None, None, None, None,   0),
                        "ev_ROTATE_THING":      EventType(18, None, None, None, None,   0),
                        "ev_MOVE_THING":        EventType(19, None, None, None, None,   0),
                        "ev_START_POSITION":    EventType(20, None, None, None, None,   0),
                        "ev_THING_FLAGS":       EventType(21, None, None, None, None,   0),
                        "ev_SCRIPT_MOVE":       EventType(22, None, None, None, None,   1),
                        "ev_SCRIPT_TURN":       EventType(23, None, None, None, None,   1),
                        "ev_SPAWN_ACTION":      EventType(24, None, None, None, None,   0),
                        "ev_PSEUDO_SCENE":      EventType(25, None, None, None, None,   0),
                        "ev_PSEUDO_SCRIPT":     EventType(26, None, None, None, None,   0),
                        "ev_NEXT_SCENE":        EventType(27, None, None, None, None,   0),
                        "ev_ANCHOR_PART":       EventType(28, None, None, None, None,   -1),
                        "ev_LOOSEN_JOINT":      EventType(29, None, None, None, None,   -1),
                        "ev_UNLOOSEN_JOINT":    EventType(30, None, None, None, None,   -1),
                        "ev_POSITION":          EventType(31, None, None, None, None,   0),
                        "ev_2_PART_LIMB":       EventType(32, None, None, None, None,   -1),
                        "ev_FIX_PART":          EventType(33, None, None, None, None,   -1),
                        "ev_UNFIX_PART":        EventType(34, None, None, None, None,   -1),
                        "ev_UNMAKE_LIMB":       EventType(35, None, None, None, None,   -1),
                        "ev_REORIENT_THING":    EventType(36, None, None, None, None,   -1),
                        "ev_PSEUDO_ADJUNCT":    EventType(37, None, None, None, None,   0),
                        "ev_PSEUDO_ADJUNCT_2":  EventType(38, None, None, None, None,   0),
                        "ev_ABSOLUTE_POS":      EventType(39, None, None, None, None,   0),                   
                        "ev_ABSOLUTE_ROT":      EventType(40, None, None, None, None,   0),
                        "ev_ADD_POINT":         EventType(41, None, None, None, None,   0),
                        "ev_OFFSET_POINT":      EventType(42, None, None, None, None,   0),
                        "ev_ADD_TRIANGLE":      EventType(43, None, None, None, None,   0),
                        "ev_COLOUR_TRIANGLE":   EventType(44, None, None, None, None,   0),
                        "ev_TRIANGLE_FLAGS":    EventType(45, None, None, None, None,   0),                        
                        "ev_INTERACT":          EventType(46, None, None, None, None,   0),                        
                        "ev_PSEUDO_ACTION_2":   EventType(47, None, None, None, None,   0),
                        "ev_POINT_TO_POINT":    EventType(48, None, None, None, None,   0),
                        "ev_HELD_OFFSET":       EventType(49, None, None, None, None,   -1),
                        "ev_HELD_ROTATE":       EventType(50, None, None, None, None,   0),                        
                        "ev_BACKGROUND":        EventType(51, None, None, None, None,   -1),
                        "ev_PSEUDO_SCENE_2":    EventType(52, None, None, None, None,   0),
                        "ev_PSEUDO_REP":        EventType(53, None, None, None, None,   0),
                        "ev_REP_ENTRY":         EventType(54, None, None, None, None,   0),
                        "ev_ACTOR_REP":         EventType(55, None, None, None, None,   0),
                        "ev_DEF_ROTATE":        EventType(56, None, None, None, None,   -1),
                        "ev_DEF_OFFSET":        EventType(57, None, None, None, None,   -1),
                        "ev_DEF_VECTOR1":       EventType(58, None, None, None, None,   -1),
                        "ev_DEF_VECTOR2":       EventType(59, None, None, None, None,   -1),
                        "ev_DEF_COLOUR":        EventType(60, None, None, None, None,   -1),
                        "ev_DEF_FLAGS":         EventType(61, None, None, None, None,   2),
                        "ev_DEF_POSITION":      EventType(62, None, None, None, None,   0),
                        "ev_CUT_PART":          EventType(63, None, None, None, None,   0),
                        "ev_HELD_OFF_LEFT":     EventType(64, None, None, None, None,   0),
                        "ev_HELD_ROT_LEFT":     EventType(65, None, None, None, None,   0),
                        "ev_THING_CODE":        EventType(66, None, None, None, None,   0)
             }

event_names = [
"ev_NO_EVENT",
"ev_ROTATE",
"ev_OFFSET",
"ev_COLOUR",
"ev_VECTOR1",
"ev_VECTOR2",
"ev_VECTOR3",
"ev_ADD_PART",
"ev_ADD_THING",
"ev_TYPE",
"ev_ADD_PART_TO_THING",
"ev_PSEUDO_ACTION",
"ev_PSEUDO_KEY",
"ev_DISP_PNT",
"ev_FLAGS",
"ev_MOVE_ACT",
"ev_RAND_ACT",
"ev_RAND_INFO",
"ev_ROTATE_THING",
"ev_MOVE_THING",
"ev_START_POSITION",
"ev_THING_FLAGS",
"ev_SCRIPT_MOVE",
"ev_SCRIPT_TURN",
"ev_SPAWN_ACTION",
"ev_PSEUDO_SCENE",
"ev_PSEUDO_SCRIPT",
"ev_NEXT_SCENE",
"ev_ANCHOR_PART",
"ev_LOOSEN_JOINT",
"ev_UNLOOSEN_JOINT",
"ev_POSITION",
"ev_2_PART_LIMB",
"ev_FIX_PART",
"ev_UNFIX_PART",
"ev_UNMAKE_LIMB",
"ev_REORIENT_THING",
"ev_PSEUDO_ADJUNCT",
"ev_PSEUDO_ADJUNCT_2",
"ev_ABSOLUTE_POS",                   
"ev_ABSOLUTE_ROT",
"ev_ADD_POINT",
"ev_OFFSET_POINT",
"ev_ADD_TRIANGLE",
"ev_COLOUR_TRIANGLE",
"ev_TRIANGLE_FLAGS",                        
"ev_INTERACT",                        
"ev_PSEUDO_ACTION_2",
"ev_POINT_TO_POINT",
"ev_HELD_OFFSET",
"ev_HELD_ROTATE",                        
"ev_BACKGROUND",
"ev_PSEUDO_SCENE_2",
"ev_PSEUDO_REP",
"ev_REP_ENTRY",
"ev_ACTOR_REP",
"ev_DEF_ROTATE",
"ev_DEF_OFFSET",
"ev_DEF_VECTOR1",
"ev_DEF_VECTOR2",
"ev_DEF_COLOUR",
"ev_DEF_FLAGS",
"ev_DEF_POSITION",
"ev_CUT_PART",
"ev_HELD_OFF_LEFT",
"ev_HELD_ROT_LEFT",
"ev_THING_CODE"
]

ev_NO_EVENT=0
ev_ROTATE=1
ev_OFFSET=2
ev_COLOUR=3
ev_VECTOR1=4
ev_VECTOR2=5
ev_VECTOR3=6
ev_ADD_PART=7
ev_ADD_THING=8
ev_TYPE=9
ev_ADD_PART_TO_THING=10
ev_PSEUDO_ACTION=11
ev_PSEUDO_KEY=12
ev_DISP_PNT=13
ev_FLAGS=14
ev_MOVE_ACT=15
ev_RAND_ACT=16
ev_RAND_INFO=17
ev_ROTATE_THING=18
ev_MOVE_THING=19
ev_START_POSITION=20
ev_THING_FLAGS=21
ev_SCRIPT_MOVE=22
ev_SCRIPT_TURN=23
ev_SPAWN_ACTION=24
ev_PSEUDO_SCENE=25
ev_PSEUDO_SCRIPT=26
ev_NEXT_SCENE=27
ev_ANCHOR_PART=28
ev_LOOSEN_JOINT=29
ev_UNLOOSEN_JOINT=30
ev_POSITION=31
ev_2_PART_LIMB=32
ev_FIX_PART=33
ev_UNFIX_PART=34
ev_UNMAKE_LIMB=35
ev_REORIENT_THING=36
ev_PSEUDO_ADJUNCT=37
ev_PSEUDO_ADJUNCT_2=38
ev_ABSOLUTE_POS=39
ev_ABSOLUTE_ROT=40
ev_ADD_POINT=41
ev_OFFSET_POINT=42
ev_ADD_TRIANGLE=43
ev_COLOUR_TRIANGLE=44
ev_TRIANGLE_FLAGS=45
ev_INTERACT=46
ev_PSEUDO_ACTION_2=47
ev_POINT_TO_POINT=48
ev_HELD_OFFSET=49
ev_HELD_ROTATE=50
ev_BACKGROUND=51
ev_PSEUDO_SCENE_2=52
ev_PSEUDO_REP=53
ev_REP_ENTRY=54
ev_ACTOR_REP=55
ev_DEF_ROTATE=56
ev_DEF_OFFSET=57
ev_DEF_VECTOR1=58
ev_DEF_VECTOR2=59
ev_DEF_COLOUR=60
ev_DEF_FLAGS=61
ev_DEF_POSITION=62
ev_CUT_PART=63
ev_HELD_OFF_LEFT=64
ev_HELD_ROT_LEFT=65
ev_THING_CODE=66

avaible_eventtypes = range(67)

#the following lists contain all the event types having
#a specific index type for their index value
have_partidx = []
have_triangleidx = []
have_actoridx = []
have_sceneidx = []

ActionEvents = [    ev_PSEUDO_ACTION,
                    ev_PSEUDO_ACTION_2,
                    ev_PSEUDO_KEY
                    ]

ActorEvents = [     ev_ACTOR_REP,
                    ev_ADD_THING,
                    ev_FLAGS,
                    ev_THING_FLAGS
                    ]

SceneEvents = [
                    ev_PSEUDO_SCENE,
                    ev_PSEUDO_SCENE_2,
                    ev_NEXT_SCENE,
                    ev_PSEUDO_SCRIPT,
                    ev_PSEUDO_KEY,
                    ev_PSEUDO_ADJUNCT,
                    ev_PSEUDO_ADJUNCT_2]

RepertoireEvents = [
                    ev_PSEUDO_REP,
                    ev_REP_ENTRY,
                    ]

EventPriority = {   
                     0:-0,
                     1:0,
                     2:0,
                     3:0,
                     4:0,
                     5:0,
                     6:0,
                     7:0,
                     8:-1,
                     9:0,
                    10:-0,
                    11:-0,
                    12:-0,
                    13:0,
                    14:0,
                    15:0,
                    16:0,
                    17:0,
                    18:0,
                    19:0,
                    20:0,
                    21:0,
                    22:1,
                    23:1,
                    24:0,
                    25:0,
                    26:0,
                    27:0,
                    28:-1,
                    29:-1,
                    30:-1,
                    31:0,
                    32:-1,
                    33:-1,
                    34:-1,
                    35:-1,
                    36:-1,
                    37:0,
                    38:0,
                    39:0,
                    40:0,
                    41:0,
                    42:0,
                    43:0,
                    44:0,
                    45:0,
                    46:-1,
                    47:0,
                    48:0,
                    49:0,
                    50:0,
                    51:-1,
                    52:0,
                    53:0,
                    54:0,
                    55:0,
                    56:-1,
                    57:-1,
                    58:-1,
                    59:-1,
                    60:-1,
                    61:-1,
                    62:-1,
                    63:2,
                    64:0,
                    65:0,
                    66:0
                 }

EventValueType_Index = 1
EventValueType_Float = 2
EventValueType_Flags = 3
EventValueType_Int   = 4

def createEventFromTextData(index_text, event_type_name, value1_text, value2_text, value3_text):
    assert event_type_name in EventTypeName.keys()
    
    event_type = EventTypeName[event_type_name]
    
    index = None
    if event_type.index_type != None:
        index = int(index_text)
        assert index >= 0
        
    values_text = [value1_text, value2_text, value3_text]
    values_type= [event_type.value1_type, event_type.value2_type, event_type.value3_type]
    values = []
    for value_type, value_text in itertools.izip(values_type, values_text):
        if value_type == EventValueType_Index:
            values.append(int(value_text))
        elif value_type == EventValueType_Float:
            values.append(float(value_text))
        elif value_type == EventValueType_Flags:
            values.append(int(value_text))
        elif value_type == EventValueType_Int:
            values.append(int(value_text))
        else:
            values.append(None)
    
    return Event(index, event_type, values[0], values[1], values[2])
        
class Event(object):
    def __init__(self, index, event_type, value1, value2, value3):
        self.index = index
        self.event_type = event_type
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        
    def __str__(self):
        if self.event_type == 0:
            return "NO_EVENT"
        strdict = {"index":self.index, "value1":self.value1, "value2":self.value2, "value3":self.value3}
        genstr = 'index=%(index)i, value1=%(value1)i, value2=%(value2)i, value3=%(value3)i' % strdict
        return event_names[self.event_type] + " " + genstr
        
    def __eq__(self, other):
        if self.index != other.index:
            return False
        if self.event_type != other.event_type:
            return False
        if self.value1 != other.value1:
            return False
        if self.value2 != other.value2:
            return False
        if self.value3 != other.value3:
            return False
        
        return True
    
    def __ne__(self, other):
        return not self.__eq__(other)
        
class NextSceneEvent(Event):
    '''
    The ev_NEXT_SCENE-event is a special case.
    It has additional data attached to it.
    That's why we introduced a new class for that purpose
    '''
    def __init__(self, index, value1, value2, value3, uk_data):
        Event.__init__(self, index, ev_NEXT_SCENE, value1, value2, value3)
        self.uk_data = uk_data
        
    def __str__(self):
        return Event.__str__(self) + ", extra data:\"" + self.uk_data + "\""

from . import Fixpoint

def extractEventVector3(event):
    '''
    returns a tuple consisting of 3 floats representing value1, value2, value3 of the event object
    converted to floating point numbers
    '''
    return (Fixpoint.tofloat(event.value1), Fixpoint.tofloat(event.value2), Fixpoint.tofloat(event.value3))

def extractEventAngles3(event):
    '''
    returns a tuple consisting of 3 floats representing value1, value2, value3 of the event object
    converted from fixed-point angles to floating point numbers
    '''
    return (Fixpoint.angletorad(event.value1), Fixpoint.angletorad(event.value2), Fixpoint.angletorad(event.value3))
