# coding: utf-8

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

from __future__ import absolute_import

from . import Event
from . import FANTLoad
from . import Actor
from . import Colour
from . import Part
from . import Flags

import types

import sqlite3

#Helper-Routines for SQL-Access
def add_vector(db_access, values):
    '''
    Adds a vector x y z to the database, returns its index
    '''
    #print('''insert into vectors (x,y,z) values (%(x)d, %(y)d, %(z)d)''' % {"x":values[0], "y":values[1], "z":values[2]})
    db_access.execute('''insert into vectors (x,y,z) values (%(x)d, %(y)d, %(z)d)''' % {"x":values[0], "y":values[1], "z":values[2]})    
    return db_access.lastrowid

def createDatabase(conn):
    db_access = conn.cursor()

    # Create table
    db_access.execute('''create table vectors (    id integer PRIMARY KEY, x real default 0.0, y real default 0.0, z real default 0.0)''')        
    db_access.execute('''create table actors (     id integer PRIMARY KEY, name text, flags integer, 
                                                   position integer, rotation integer)''')        
    db_access.execute('''create table parts (      actor integer, id integer, parent integer, 
                                                   offset integer, centre integer, origin integer, halfaxes integer, rotation integer, 
                                                   flags integer, color integer, PRIMARY KEY (actor, id))''')
    db_access.execute('''create table points (     actor integer, id integer,  part integer,     
                                                   offset integer, PRIMARY KEY (part, id))''')
    db_access.execute('''create table triangles (  actor integer, id integer,  
                                                   a integer, b integer, c integer,
                                                   flags integer, color_front integer, color_back integer, PRIMARY KEY (actor, id))''')                                  
    return db_access

'''
This file contains handlers to interpret Ecstatica Events for the definition of an actor (ellipses, triangles, points, etc.)

This is NOT the general handling routine for Ecstatica events
'''

class Handler(object):
    '''
    base class for all handlers. Provides the handle-Routine, which should NOT be overloaded by subclasses.
    '''
    def __init__(self, parent, db_access):
        self.parenthandler = parent
        self.db_access = db_access
    
    def handle(self, event):
        '''
        handles an event. It tries to find a matching handling routine. If there none, the unhandhled-Routine is
        called (which could be overloaded by subclasses)
        @param event: the event object to handle
        '''        
        if hasattr(self, "handle_" + Event.event_names[event.event_type]):
            #print("calling handle_" + Event.event_names[event.event_type])
            return self.__getattribute__("handle_" + Event.event_names[event.event_type])(event)
        else:
            return self.unhandled(event)
        
    def leaveScope(self):
        '''
        Is called in the case that an unhandled event occurs in the current wrapper and
        control returns to the parent wrapper
        '''
        pass
            
    def unhandled(self, event):
        '''
        is called if there's no routine present in the handler to deal with the given event type.
        The handler routines have to be named following the pattern handle_<full event name>
        
        The default behaviour implemented here is to return to the parent handler upon receiving an unhandled event.
        This continues until a handler is reached which has no parent. In this case an exception is raised!
        
        The important part is: A handler regularly handles only the NON-opening events (the part handler is NOT handling ADD_PART)
        That way the arrival of a NEW part is elegantly reacted on: The part handler does not handle ADD_PART nor ADD_TRIANGLE or
        ADD_POINT, so it returns control to its parent.
        In order to get all necessary information out of the opening events (ev_ADD_THING, ev_ADD_PART_TO_THING, ev_ADD_PART, ev_ADD_TRIANGLE,
        ev_ADD_POINT), the handlers receive the opening event in their constructor call.
        '''        
        #we have to be careful that we don't provoke an infinite loop here
        #if the parent's handle routine is just creating another instance of this class,
        #we will end up here again, returning to the parent again, creating another instance,...etc.
        if self.parenthandler != None: #if there's a parent handler, we return control to it 
            self.leaveScope()
            return self.parenthandler.handle(event)
        else: #if there's no parent, we have no choice but to throw an exception
            raise Exception("Unexpected event: " + str(event))
        
class IgnoreHandler(Handler):
    '''
    This handler ignores all events until it reaches an unexpected event. It then returns to its parent handler
    '''
    def ignore(self, event):
        return self
    
    def __init__(self, parent, ignorelist):
        '''
        @param ignorelist: a list of event-ids which shall be ignored
        '''
        Handler.__init__(self, parent, None)
        #for all ignored events, we create a respective method entry following the pattern handle_<event name>
        for eventid in ignorelist: 
            self.__setattr__('handle_' + Event.event_names[eventid], types.MethodType(IgnoreHandler.ignore, self))
    
class ActorHandler(Handler):
    '''
    Handles actor events like ADD_THING, ADD_PART_TO_THING
    '''
    def __init__(self, globalhandler, event, db_access):
        Handler.__init__(self, globalhandler, db_access)
        self.actor_idx = event.value1
                 
    #def handle_ev_ADD_THING(self, event):
    #    '''
    #    This event initializes a new actor. The actor's index is remembered and compared to the actor index of each of the following events
    #    to ensure.
    #    '''
    #    self.actor_idx = event.value1
    #    return self
    
    def handle_ev_START_POSITION(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        
        #print(event)
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])
        self.db_access.execute('''update actors set position = %(vector_idx)d where id == %(actor_idx)d''' 
                               % {"actor_idx":self.actor_idx, "vector_idx":lastrowid})
        
        return self
    
    def handle_ev_THING_FLAGS(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
                
        self.db_access.execute('''select flags from actors where (id == %(actor_idx)d)''' % {"actor_idx":self.actor_idx})
        result = self.db_access.fetchall()
        #print(result)
        assert len(result) == 1 and len(result[0]) == 1        
        flags = Flags.Flags(result[0][0])
        flags.clearSelected(event.value2)
        flags.setSelected(event.value1)                           
                
        self.db_access.execute('''update actors set flags = %(flags)d where id == %(actor_idx)d''' 
                               % {"actor_idx":self.actor_idx, "flags":flags.value})
        
        return self
    
    def handle_ev_HELD_OFFSET(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    def handle_ev_HELD_ROTATE(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    def handle_ev_HELD_OFF_LEFT(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    def handle_ev_HELD_ROT_LEFT(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    def handle_ev_ACTOR_REP(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    def handle_ev_THING_CODE(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        return self
    
    #-----------------------------------------------------------------------------------------------------------------_

    def handle_ev_ADD_PART_TO_THING(self, event):
        if event.index != self.actor_idx:
            raise ValueError("inconsistent actor index")
        
        part_idx = event.value1
        self.db_access.execute('''insert into parts (actor, id) values (%(actor_idx)d, %(part_idx)d)''' % {"actor_idx":self.actor_idx, "part_idx":part_idx})
                        
        return self
    
    def handle_ev_ADD_PART(self, event):
        '''
        Concerning the question whether we should create the bone here
        or in the PartHandler:
        -     if we handle it here, we can simply pass the bone object to the
            PartHandler
        -    if we handle it in the PartHandler, we have to pass the whole
            ActorHandler object to the Part Handler
        In the first case we are passing around less information. So I'll
        do it that way!
        '''
        #We query all known part indices
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        parent_idx = event.index
        part_idx = event.value1
        self.db_access.execute('''insert into parts (actor, id, parent) values (%(actor_idx)d, %(part_idx)d, %(parent_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "parent_idx":parent_idx})
        
        return self    
    
    def handle_ev_OFFSET(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])        
        self.db_access.execute('''update parts set offset = %(vector_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)'''  
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "vector_idx":lastrowid})
        
        return self
    
    def handle_ev_POSITION(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])        
        self.db_access.execute('''update parts set origin = %(vector_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)'''  
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "vector_idx":lastrowid})

        return self
    
    def handle_ev_ROTATE(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])        
        self.db_access.execute('''update parts set rotation = %(vector_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "vector_idx":lastrowid})   
        
        return self
    
    def handle_ev_DISP_PNT(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        #dunno what disp_pnt does. Seems to be nothing important!
        
        return self
    
    def handle_ev_VECTOR1(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])        
        self.db_access.execute('''update parts set halfaxes = %(vector_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "vector_idx":lastrowid})
        
        return self
    
    def handle_ev_VECTOR2(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])        
        self.db_access.execute('''update parts set centre = %(vector_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "vector_idx":lastrowid})        
        
        return self
    
    def handle_ev_VECTOR3(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        #dunno what vector3 does. Seems to be nothing important!        
        return self
    
    def handle_ev_COLOUR(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        mappalette = event.value1
        assert mappalette >= 0 and mappalette < 16
                
        part_idx = event.index    
        self.db_access.execute('''update parts set color = %(color_idx)d where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "color_idx":mappalette})
        
        return self
    
    def handle_ev_TYPE(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        return self
    
    def handle_ev_FLAGS(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))            
        if not event.index in indices:
            raise ValueError("unknown part index")
        
        part_idx = event.index
        self.db_access.execute('''select flags from parts where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx})
        result = self.db_access.fetchall()
        assert len(result) == 1 and len(result[0]) == 1        
        flags = Flags.Flags(result[0][0])
        flags.clearSelected(event.value2)
        flags.setSelected(event.value1)
                
        self.db_access.execute('''update parts set flags = %(flags)d where (actor == %(actor_idx)d and id == %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "part_idx":part_idx, "flags":flags.value})
        return self
    
    #-----------------------------------------------------------------------------------------------------------------_
    
    def handle_ev_ADD_POINT(self, event):
        #We query all known part indices
        indices = map(lambda x: x[0], self.db_access.execute('select id from parts where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))    
        if not event.index in indices:
            raise ValueError("unknown part index")
                
        part_idx = event.index
        self.db_access.execute('''insert into points (actor, id, part) values (%(actor_idx)d, %(point_idx)d, %(part_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "point_idx":event.value1, "part_idx":part_idx})
        
        return self
    
    def handle_ev_OFFSET_POINT(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from points where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))    
        if not event.index in indices:
            raise ValueError("unknown point index")
        
        point_idx = event.index
        lastrowid = add_vector(self.db_access, [event.value1, event.value2, event.value3])
        self.db_access.execute('''update points set offset = %(vector_idx)d where (actor == %(actor_idx)d and id == %(point_idx)d)'''  
                               % {"actor_idx":self.actor_idx, "point_idx":point_idx, "vector_idx":lastrowid})
        
        return self
    
    #-----------------------------------------------------------------------------------------------------------------_      
    
    def handle_ev_ADD_TRIANGLE(self, event):       
        #in the case of ADD_TRIANGLE, the index field does not
        #contain the actor's index but the triangle's index!                    
        
        tri_idx = event.index
        a = event.value1
        b = event.value2
        c = event.value3
        self.db_access.execute('''insert into triangles (actor, id, a, b, c) values (%(actor_idx)d, %(tri_idx)d, %(a)d, %(b)d, %(c)d)'''
                               % {"actor_idx":self.actor_idx, "tri_idx":tri_idx, "a":a, "b":b, "c":c})
           
        return self
    
    def handle_ev_COLOUR_TRIANGLE(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from triangles where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))    
        if not event.index in indices:
            raise ValueError("unknown triangle index")
        
        color_front = event.value1
        #print(color_front)
        assert color_front >= 0 and color_front < 32
        color_back = event.value2
        #print(color_back)
        assert color_back >= 0 and color_back < 32
                    
        tri_idx = event.index
        self.db_access.execute('''update triangles set color_front = %(color_front)d, color_back = %(color_back)d where (actor == %(actor_idx)d and id == %(tri_idx)d)'''  
                               % {"actor_idx":self.actor_idx, "tri_idx":tri_idx, "color_front":color_front, "color_back":color_back})
        
        return self
    
    def handle_ev_TRIANGLE_FLAGS(self, event):
        indices = map(lambda x: x[0], self.db_access.execute('select id from triangles where (actor == %(actor_idx)d)' % {"actor_idx":self.actor_idx}))    
        if not event.index in indices:
            raise ValueError("unknown triangle index")
        
        tri_idx = event.index
        self.db_access.execute('''select flags from triangles where (actor == %(actor_idx)d and id == %(tri_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "tri_idx":tri_idx})
        result = self.db_access.fetchall()
        assert len(result) == 1 and len(result[0]) == 1
        #print(result)
        flags = Flags.Flags(result[0][0])
        flags.clearSelected(event.value2)
        flags.setSelected(event.value1)                        
                
        tri_idx = event.index
        self.db_access.execute('''update triangles set flags = %(flags)d where (actor == %(actor_idx)d and id == %(tri_idx)d)''' 
                               % {"actor_idx":self.actor_idx, "tri_idx":tri_idx, "flags":flags.value})
        
        return self
        
class IgnoreActorHandler(IgnoreHandler):
    def __init__(self, parent):
        #Event.ev_ADD_THING, 
        IgnoreHandler.__init__(self, parent, [    Event.ev_START_POSITION, Event.ev_THING_FLAGS,
                                                Event.ev_HELD_OFFSET, Event.ev_HELD_ROTATE,    Event.ev_HELD_OFF_LEFT,
                                                Event.ev_HELD_ROT_LEFT,    Event.ev_ACTOR_REP,    Event.ev_THING_CODE,
                                                Event.ev_ADD_PART, Event.ev_ADD_PART_TO_THING, Event.ev_ADD_TRIANGLE,
                                                Event.ev_ADD_POINT])    
    
class GlobalHandler(Handler):
    '''
    Expects a ADD_THING-Event
    '''
    def handle_ev_ADD_THING(self, event):
        if self.specific_index != None: #if not None, the handler ought to filter for the given actor index!
            if event.value1 != self.specific_index:
                return IgnoreActorHandler(self)
            
        actor_idx = event.value1
        self.db_access.execute('''insert into actors (id) values (%(actor_idx)d)''' % {"actor_idx":actor_idx})
            
        return ActorHandler(self, event, self.db_access)
    
    def __init__(self, specific_index=None, conn= None):
        '''
        @param specific_index: Allows to narrow down the handling to a specific actor index. All other actors are ignored!
        '''            
        self.specific_index = specific_index
        
        if conn == None:
            self.conn = sqlite3.connect(':memory:')
        else:
            self.conn = conn
        db_access = createDatabase(self.conn)
        
        Handler.__init__(self, None, db_access)     

    def __del__(self):
        # Save (commit) the changes    
        self.conn.commit()
        self.db_access.close()

    
def createSpecificActor(fileobj, index, db=None):
    '''
    Loads specific Actor in the FANT file
    '''
    if db == None:
        db = sqlite3.connect(':memory:')
    doc = FANTLoad.FANTFileLoader(fileobj, save_terminal_events=False).fantfile
    glob = GlobalHandler(index, db)
    handler = glob    
    for event in doc.actorevents:
        handler = handler.handle(event)
    return db

#-------------------------------------------------  T E S T -----------------------------------------------------------
        
import unittest

class Test_Handler(unittest.TestCase):
    def test_HandleCall(self):
        '''
        The handler should find the handler routine and call it
        '''
        class Dummy(Handler):
            def __init__(self):
                Handler.__init__(self, None, None)
            
            def handle_ev_ADD_THING(self, event):
                return 666.666 #this is a test code to identify the correct behaviour                
            
        dummy = Dummy()
        self.assertEqual(dummy.handle(Event.Event(0, Event.ev_ADD_THING, 0, 0, 0)), 666.666, "")
        
    def test_ReturnToParent(self):
        '''
        If a handler with a parent receives an unknown event, it forwards it to its parent
        '''
        class Dummy(Handler):
            def __init__(self):
                Handler.__init__(self, None, None)
            
            def handle_ev_ADD_THING(self, event):
                return 666.666 #this is a test code to identify the correct behaviour                
                    
        class SubDummy(Handler):
            def __init__(self, parent):
                Handler.__init__(self, parent, None)
                
        dummy = Dummy()
        subdummy = SubDummy(dummy)
        self.assertEqual(subdummy.handle(Event.Event(0, Event.ev_ADD_THING, 0, 0, 0)), 666.666, "")
        
    def test_ParentlessHandlerRaisesException(self):
        '''
        If a parentless handler receives an unknown event, it raises an exception
        '''
        class Dummy(Handler):
            def __init__(self):
                Handler.__init__(self, None, None)
            
            def handle_ev_ADD_THING(self, event):
                return 666.666 #this is a test code to identify the correct behaviour                
                    
        class SubDummy(Handler):
            def __init__(self, parent):
                Handler.__init__(self, parent, None)
                
        dummy = Dummy()
        subdummy = SubDummy(dummy)
        self.assertRaises(Exception, subdummy.handle, Event.Event(0, Event.ev_ADD_PART, 0, 0, 0))
        
class Test_GlobalHandler(unittest.TestCase):
    def test_HandleActorCreationEvent(self):
        '''
        upon receiving an ev_ADD_THING event, the global handler should return an actor handler
        '''        
        globhandler = GlobalHandler()
        self.assertEqual(type(globhandler.handle(Event.Event(0, Event.ev_ADD_THING, 0, 0, 0))), ActorHandler, "")
        
    def test_HandleSpecificActorCreationEvent(self):
        '''
        If we require the global handler to filter the actors for a specific on, it should only enter the actor handler
        if the correct actor index appears. For incorrect actor indices, an ignoreactor handler must be entered
        '''
        globhandler = GlobalHandler(1) #we require the global handler to exclusively import actor of index 1
        #(the actor index is transported in event value1)
        self.assertEqual(type(globhandler.handle(Event.Event(0, Event.ev_ADD_THING, 0, 0, 0))), IgnoreActorHandler, "")
        self.assertEqual(type(globhandler.handle(Event.Event(0, Event.ev_ADD_THING, 1, 0, 0))), ActorHandler, "")
        
class Test_ActorHandler(unittest.TestCase):
    def setUp(self):#
        self.conn = sqlite3.connect(':memory:')
        self.db_access = createDatabase(self.conn)
    
    def test_InconsistentActorIdx(self):
        '''
        After the initial ADD_THING event, all events up to the next ADD_THING event have to reference the actor's index.
        It is not allowed to have within that sequence an event referencing a different actor index
        '''
        acthandler = ActorHandler(None, Event.Event(-1, Event.ev_ADD_THING, 4734, 0, 0), self.db_access)            
        self.assertRaises(ValueError, acthandler.handle, Event.Event(234, Event.ev_START_POSITION, 0, 0, 0))
        #now it should work!
        self.assertEqual(acthandler.handle(Event.Event(4734, Event.ev_START_POSITION, 0, 0, 0)), acthandler, "")
        
    def test_AnotherActor(self):
        '''
        The actor handler shall return to the global parent as soon as it runs across an ADD_THING event
        '''
        glob = GlobalHandler()
        acthandler = glob.handle(Event.Event(0, Event.ev_ADD_THING, 23, 0, 0))
        self.assertEqual(type(acthandler), ActorHandler, "actor handler is entered")
        another_acthandler = acthandler.handle(Event.Event(0, Event.ev_ADD_THING, 24, 0, 0))
        self.assertNotEqual(another_acthandler, acthandler, "_another_ actor handler is entered")
    
class Test_IgnoreActorHandler(unittest.TestCase):
    def setUp(self):#
        self.conn = sqlite3.connect(':memory:')
        self.db_access = createDatabase(self.conn)
    
    def test_IgnorePerpetuation(self):
        '''
        In order to ignore the actor, the ignore actor handler has react to all events
        '''
        actorhandler = IgnoreActorHandler(None)
        self.assertEqual(type(actorhandler.handle(Event.Event(0, Event.ev_ADD_PART, 0, 0, 0))), IgnoreActorHandler, "")
        self.assertEqual(type(actorhandler.handle(Event.Event(0, Event.ev_ADD_TRIANGLE, 0, 0, 0))), IgnoreActorHandler, "")
        self.assertEqual(type(actorhandler.handle(Event.Event(0, Event.ev_ADD_POINT, 0, 0, 0))), IgnoreActorHandler, "")
    
def test_RealData():    
    file = open("/home/fabian/Projekte/ecstatica_remake/workspace/Ecstatica/test/ecst2.", "rb")
    file.seek(2233776) #0ter Actor
    actor = createSpecificActor(file, 0)
    
#def test_toFile():
def toFile():
    file = open("/home/fabian/Projekte/ecstatica_remake/workspace/Ecstatica/test/ecst2.", "rb")
    file.seek(2233776) #0ter Actor    
    doc = FANTLoad.FANTFileLoader(file, save_terminal_events=False).fantfile
    comm = sqlite3.connect('character_0.sql')
    glob = GlobalHandler(0, comm)
    handler = glob    
    for event in doc.actorevents:
        handler = handler.handle(event)
    return None    
        
def dummyEvent(id, index=0, value=0):
    '''
    creates a dummy Event instance. Convenience routine
    '''
    return Event.Event(index, id, value, 0, 0)

def runEvSeqTest(start_handler_class, db_access, start_event, events):
    '''
        1. a handler of class start_handler_class is created with start_event as event
        2. the list of events is handled by - starting with start_handler - the respective current handler
        3. all handlers traversed are noted in a list, which is return in the end
        
        This routine is meant as a convenience routine to create test like test_AnotherTriangle
        
        NOTE: The start_handler instance itself is NOT included in the output list!
    '''
    start_handler = start_handler_class(None, start_event, db_access)
    next = start_handler
    output = []
    for event in events:    
        next = next.handle(event)
        output.append(next)
    return output
    
if __name__ == "__test__":
    unittest.main()
