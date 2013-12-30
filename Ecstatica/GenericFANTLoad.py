# coding: utf-8

#Created on 12.04.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import types

from . import Sound

#*********************************************************************************************************************************
#Note: This class could be interesting for performance aspects in the future, but atm we don't really need it...
#*********************************************************************************************************************************
class GenericFANTLoad(object):
    '''
    This class generalizes the FANTLoad-Procedure. It does not process FANTFile objects but instead manages
    a set of callback routines to handle the loading of the different object types in a FANT file. 
    
    The user has to provide a callback for sound objects, for example. Upon stumbling across a sound object,
    the object of this class then calls the user's callback handing over a sound object
    
    We could - in a future step - generalize this even more by handing over to the user's callback a file object
    and delegating the actual loading procedure to that. If we do this depends on whether we need this general
    access to binary FANT data...
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.handlers = {}
    
    def addHandler(self, handle_class, callback):
        '''
        Adds a handler for a specific type (Sound for instance)
        
        @param handle_class: The type to handle (Sound for instance)
        @param callback: The callback to call in the form callback(loaded_object)
        '''
        if not issubclass(handle_class, object):
            raise TypeError("Expect valid new-style python class for handle class but instead got: " + str(handle_class))
        if not type(callback) is types.FunctionType:
            raise TypeError("Expect valid python callable for handle callback")
        if handle_class in self.handlers.keys(): #the user has added a handler for that type already. We disallow that!
            raise ValueError("There's already a handler for type " + str(handle_class) + " present")
        
        self.handlers[handle_class] = callback
        
    def readFile(self, fileobj):
        '''
        Starts reading the FANT (or XML) file
        
        @param fileobj: The fileobj to read the FANT data from
        '''
        pass
    
import unittest

class TestGenericFANTLoad(unittest.TestCase):
    def setUp(self):
        self.loader = GenericFANTLoad()
        
    def tearDown(self):
        del self.loader
    
    def test_instantiation(self):
        pass
        
    def test_addHandler(self):
        '''
        The handler routine has to be a valid python function and the handler class has to be a valid python new-style class
        '''
        self.assertRaises(TypeError, self.loader.addHandler)
        self.assertRaises(TypeError, self.loader.addHandler, None)
        self.assertRaises(TypeError, self.loader.addHandler, 454)
        
        def dummy_callback(sound_obj):
            pass
        self.assertRaises(TypeError, self.loader.addHandler, dummy_callback)
        self.assertRaises(TypeError, self.loader.addHandler, None, dummy_callback)        
        self.assertRaises(TypeError, self.loader.addHandler, Sound.Sound, None)
        self.loader.addHandler(Sound.Sound, dummy_callback)
        self.assertEqual(self.loader.handlers, {Sound.Sound: dummy_callback}, "we check whether the handler was actually added")
        #trying to add the callback a 2nd time should fail!
        self.assertRaises(ValueError, self.loader.addHandler, Sound.Sound, dummy_callback) 
