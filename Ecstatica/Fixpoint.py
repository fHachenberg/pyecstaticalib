# coding: utf-8

#Created on 19.01.2012

#Copyright (C) 2013 Fabian Hachenberg
#This file is part of EcstaticaLib. 
#EcstaticaLib is free software: you can redistribute it and/or modify 
#it under the terms of the GNU General Public License as published by 
#the Free Software Foundation, either version 3 of the License, or 
#(at your option) any later version. 
#More information about the license is provided in the LICENSE file.

import math

def tofloat(fpnumber, shiftwidth=14):
    if fpnumber < -32768 or fpnumber > 65535: 
        raise OverflowError("fix point number is out of valid range (-32768, 32767)")
    return float(fpnumber) / float(1 << (shiftwidth))

def tofixpoint(input, shiftwidth=14):
    value = int(input * float(1 << shiftwidth))
    return value

def fpangletorad(fpangle):
    '''
    Converts fixed point angle value into floating-point radian value
    '''
    if abs(fpangle) > 0xffff:
        raise OverflowError("fix point angle is out of valid range (0, 65535)")
    return 2.0 * math.pi * float(fpangle) / 65535.0

def radtofpangle(radangle):
    while radangle > math.pi:
        radangle -= math.pi
    while radangle < -math.pi:
        radangle += math.pi        
    return int((radangle / math.pi) * 0x8000)  

import unittest

class TestMappings(unittest.TestCase):
    def test_to_float_and_back(self):
        for i in range(-32768, 32767):
            self.assertEqual(i, tofixpoint(tofloat(i)), "identify mapping")
            
    def test_to_fixpoint_and_back(self):
        print("step size is", repr(1.0/16768.0))
        val = -2.0
        while val <= 2.0:#
            diff = abs(val - tofloat(tofixpoint(val)))
            self.assert_(diff <= 1.0/16768.0, repr(val) + " is actually mapped to " + repr(tofloat(tofixpoint(val))))
            val += 1.0/16768.0
            
    def test_rad_to_angle_and_back(self):
        print("step size is", repr(math.pi*2.0/65636.0))
        val = 0.0
        while val <= math.pi*2.0:
            diff = abs(val - fpangletorad(radtofpangle(val)))
            self.assert_(diff <= math.pi*2.0/65636.0, repr(val) + " is actually mapped to " + repr(fpangletorad(radtofpangle(val))))
            val += math.pi*2.0/65636.0
            
    def test_angle_to_rad_and_back(self):
        for i in range(65536):
            self.assertEqual(i, radtofpangle(fpangletorad(i)), repr(i) + " is actually mapped to " + repr(radtofpangle(fpangletorad(i))))
